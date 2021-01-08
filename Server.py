import socket
import os
import re

from os import name
from _thread import start_new_thread


def UserRefresh():
    global Users, Passwords, Storages
    for i in ReadUserFile.readlines():
        i = i.split(',')
        Users.append(i[0])
        Passwords.append(i[1])
        Storages.append(i[2])


def ReceiveFile(Client, Path, User, FileName, FileSize):
    if os == 'nt':
        File = open(BASE + '\\' + User + '\\' + Path + '\\' + FileName, "wb")
    else:
        File = open(BASE + '/' + User + '/' + Path + '/' + FileName, "wb")
    Buf = BUFFER_SIZE
    while FileSize > 0:
        if FileSize < BUFFER_SIZE:
            Buf = FileSize
        Bytes = Client.recv(Buf)
        File.write(Bytes)
        FileSize = FileSize - len(Bytes)

    Client.send(f"bool{SEPARATOR}true".encode())


def SendFile(Client, Path, User,FileName):
    FileSize = 0
    File = None
    if os == 'nt':
        try:
            Available = True
            File = open(BASE + '\\' + User + '\\' + Path.rstrip() + '\\' + FileName.rstrip(), "rb")
            FileSize = os.path.getsize(BASE + '\\' + User + '\\' + Path.rstrip() + '\\' + FileName.rstrip())
        except FileNotFoundError:
            Available = False
    else:
        try:
            Available = True
            File = open(BASE + '/' + User + '/' + Path.rstrip() + '/' + FileName.rstrip(), "rb")
            FileSize = os.path.getsize(BASE + '/' + User + '/' + Path.rstrip() + '/' + FileName.rstrip())
        except FileNotFoundError:
            Available = False
    Buf = BUFFER_SIZE
    print(BASE + '/' + User + '/' + Path.rstrip() + '/' + FileName.rstrip())
    if Available:
        Client.send(f"bool{SEPARATOR}true{SEPARATOR}{FileSize}".encode())
        while True:
            Bytes = File.read(Buf)
            if not Bytes:
                File.close()
                break
            Client.send(Bytes)

    else:
        Client.send(f"bool{SEPARATOR}false".encode())


def SendFiles(Client,Path,User):
    lis = []
    for p, d, f in os.walk(BASE + '/' + User + '/' + Path):
        for f1 in f:
            fp = os.path.join(p, f1)
            st = BASE + '/' + User + '/' + Path
            lis.append(re.sub(st, '', fp))
    print(lis)
    for i in lis:
        Client.send(f"{i}{SEPARATOR}".encode())

    Client.send(EOS.encode())


def Dir(Client,Path,User):
    if OS == 'nt':
        List = os.listdir(BASE + '\\' + User + '\\' + Path)
    else:
        List = os.listdir(BASE + '/' + User + '/' + Path)

    for i in List:
        if os == 'nt':
            if os.path.isdir(BASE + '\\' + User + '\\' + Path + '\\' + i):
                Client.send(f"[Dir]  {i}{SEPARATOR}".encode())
            else:
                Client.send(f"[File] {i}{SEPARATOR}".encode())
        else:
            if os.path.isdir(BASE + '/' + User + '/' + Path + '/' + i):
                Client.send(f"[Dir]  {i}{SEPARATOR}".encode())
            else:
                Client.send(f"[File] {i}{SEPARATOR}".encode())
    Client.send(EOS.encode())


def Stat(Client,User):
    Client.send()


# Constant
OS = name
SERVER_HOST = ""
SERVER_PORT = 24680
BUFFER_SIZE = 1024 * 4
SEPARATOR = "-|+0+|-"
EOS = "++--++"
BASE = "/media/home/Data"

# Initialize
Users = []
Passwords = []
Storages = []

ReadUserFile = open('UserData.txt', 'r', encoding='utf-8')
WriteUserFile = open('UserData.txt', 'a', encoding='utf-8')
UserRefresh()

Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
Sock.bind((SERVER_HOST, SERVER_PORT))
Sock.listen(10)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def Command(Client, Address):
    User = None
    Storage = None
    CD = ""
    global ReadUserFile, WriteUserFile
    print(f"[+] {Address} is connected.")
    while True:
        data = Client.recv(BUFFER_SIZE)
        data = data.decode()
        if data != "":
            lis = data.split(SEPARATOR)
            if lis[0] == "c_username":
                if lis[1] in Users:
                    Client.send(f"bool{SEPARATOR}false".encode())
                else:
                    Client.send(f"bool{SEPARATOR}true".encode())
            elif lis[0] == "create" and lis[1] not in Users:
                WriteUserFile.write(f"{lis[1]},{lis[2]},{lis[3]},\n")
                WriteUserFile.close()
                WriteUserFile = open('UserData.txt', 'a', encoding='utf-8')
                ReadUserFile.close()
                ReadUserFile = open('UserData.txt', 'r', encoding='utf-8')
                UserRefresh()
                Client.send(f"bool{SEPARATOR}true".encode())
            elif lis[0] == "create" and lis[1] in Users:
                Client.send(f"bool{SEPARATOR}false".encode())
            elif lis[0] == "login":
                if lis[1] in Users:
                    Use = Users.index(lis[1])
                    if lis[2] == Passwords[Use]:
                        User = lis[1]
                        Storage = Storages[Use]
                        client.send(f"bool{SEPARATOR}true{SEPARATOR}true".encode())
                    else:
                        client.send(f"bool{SEPARATOR}true{SEPARATOR}false".encode())
                else:
                    client.send(f"bool{SEPARATOR}false".encode())
            elif lis[0] == "s_file" and User is not None:
                Path = lis[1].rstrip()
                FileName = lis[2]
                FileSize = int(lis[3])
                if not os.path.exists(BASE + '/' + User + '/' + Path):
                    os.mkdir(BASE + '/' + User + '/' + Path)
                CS = int(Storage) * 1024 * 1024 * 1024
                VS = 0
                for p, d, f in os.walk(BASE + '/' + User + '/'):
                    for f1 in f:
                        fp = os.path.join(p, f1)
                        VS = VS + os.path.getsize(fp)
                if int(CS) - int(VS) > int(FileSize):
                    Client.send(f"bool{SEPARATOR}true".encode())
                    ReceiveFile(Client, Path, User, FileName, FileSize)
                else:
                    Client.send(f"bool{SEPARATOR}false".encode())
            elif lis[0] == "g_file" and User is not None:
                Path = lis[1]
                FileName = lis[2]
                SendFile(Client,Path,User,FileName)
            elif lis[0] == "g_files" and User is not None:
                SendFiles(Client,CD,User)
            elif lis[0] == "dir" and User is not None:
                Dir(Client,CD,User)
            elif lis[0] == "cd" and User is not None:
                if OS == 'nt':
                    location = f"{BASE}\\{User}\\{lis[1]}"
                    st = location.replace('/','\\')
                else:
                    location = f"{BASE}/{User}/{lis[1]}"
                    st = location.replace('\\', '/')
                if os.path.isdir(st):
                    Client.send(f"bool{SEPARATOR}true".encode())
                else:
                    Client.send(f"bool{SEPARATOR}false".encode())
                CD = lis[1]
            elif lis[0] == 'mkdir' and User is not None:
                if OS == 'nt':
                    location = f"{BASE}\\{User}\\{lis[1]}"
                    st = location.replace('/', '\\')
                else:
                    location = f"{BASE}/{User}/{lis[1]}"
                    st = location.replace('\\', '/')
                try:
                    os.mkdir(st.strip())
                    Client.send(f"bool{SEPARATOR}true".encode())
                except FileExistsError:
                    Client.send(f"bool{SEPARATOR}false".encode())
            else:
                pass
        else:
            break


while True:
    client, address = Sock.accept()
    print(f"[+] {address} is connecting.")
    start_new_thread(Command, (client, address))
