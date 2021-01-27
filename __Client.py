<<<<<<<< HEAD:__Client.py
import getopt
import hashlib
import os
import socket
import sys
import tqdm
import inspect

from os import name, system

OS = name

PORT = None
HOST = None
BUFFER = 1024 * 4
SEPARATOR = "-|+0+|-"
EOS = "++--++"
CD = ""

User = None
UserVar = None


def Clean():
    dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    file = os.path.basename(__file__)
    if OS == 'nt':
        os.remove(f"{dir}\\{file}")
    else:
        os.remove(f"{dir}/{file}")


def ErrorHandler(data):
    if data[0] == 'error':
        if data[1] == '1':
            print("Server busy")
        elif data[1] == '2':
            print("Request denied")
        elif data[1] == '3':
            print("Access Denied")
        elif data[1] == '4':
            print("Protocol violated")
        elif data[1] == '5':
            print("Server update is in progress... Try after some time")
    else:
        print("Unexpected error occurred")


def Create():
    UserVar = None
    PasswordVar = None
    StorageVar = None
    userid = None

    def Username():
        nonlocal UserVar, userid
        user = input("Username: ")
        userid = user
        user = user.encode(encoding='utf-8')
        user = hashlib.sha512(user).hexdigest()
        Socket.send(f"c_username{SEPARATOR}{user}".encode())
        data = Socket.recv(BUFFER).decode()
        lis = data.split(SEPARATOR)
        if lis[0] == 'bool' and lis[1] == 'true':
            UserVar = user
        elif lis[0] == 'bool' and lis[1] == 'false':
            print("Username not available")
        else:
            ErrorHandler(lis)

    def Password():
        nonlocal PasswordVar
        password = input("Password: ")
        password = password.encode('utf-8')
        password = hashlib.sha512(password).hexdigest()
        ReTypePassword = input("Retype Password: ")
        ReTypePassword = ReTypePassword.encode('utf-8')
        ReTypePassword = hashlib.sha512(ReTypePassword).hexdigest()
        if ReTypePassword == password:
            PasswordVar = password
        else:
            print("Passwords are not same")

    def Storage():
        nonlocal StorageVar
        storage = input("Storage: ")
        storage = int(storage)
        storage = str(storage)
        StorageVar = storage

    def Status():
        if UserVar is not None:
            print(f"Username: {userid}")
        else:
            print("Username: ")

        if PasswordVar is not None:
            print("Password: *******")
        else:
            print("Password:  ")
        if StorageVar is not None:
            print(f"Storage: {StorageVar}GB")
        else:
            print("Storage: ")

    print("""Commands \n\tSet Username (U)\n\tSet Password(P) \n\tSet Storage(S) \n\tStatus (T) \n\tCreate (C) 
    Back (B)  \n\tExit (E)""")
    while True:
        cmd = input("> ")
        cmd = cmd.lower()
        if cmd == 'u':
            print("""Username can have (a-z,A-Z,0-9,_)""")
            Username()
        elif cmd == 'p':
            print("""Password should have minimum 8 character""")
            Password()
        elif cmd == 's':
            print("Storage should be in terms of GB")
            Storage()
        elif cmd == 't':
            Status()
        elif cmd == 'b':
            break
        elif cmd == 'c':
            if UserVar is not None and PasswordVar is not None and StorageVar is not None:
                Socket.send(f"create{SEPARATOR}{UserVar}{SEPARATOR}{PasswordVar}{SEPARATOR}{StorageVar}".encode())
                ret = Socket.recv(BUFFER).decode()
                lis = ret.split(SEPARATOR)
                if lis[0] == 'false' and lis[1] == 'true':
                    print("User created successfully")
                    break
                elif lis[0] == 'false' and lis[1] == 'false':
                    print("Unable to create user ")
                else:
                    ErrorHandler(lis)
            else:
                Status()
                print("Fields are empty !!!")
        elif cmd == 'e':
            exit(0)
        else:
            print("Invalid Command")


def Login():
    PasswordVar = None
    user_var = None
    user = None

    print("Commands \n\tUsername (U)\n\tPassword (P) \n\tStatus (S) \n\tLogin (L) \n\tBack (B) \n\tExit (E)")

    def Username():
        nonlocal user, user_var
        user_var = input("Username: ")
        user = user_var
        user_var = user_var.encode(encoding="utf-8")
        user_var = hashlib.sha512(user_var).hexdigest()

    def Password():
        nonlocal PasswordVar
        PasswordVar = input("Password: ")
        PasswordVar = PasswordVar.encode(encoding="utf-8")
        PasswordVar = hashlib.sha512(PasswordVar).hexdigest()

    def Status():
        global User
        if user_var is not None:
            print(f"Username: {user}")
        else:
            print("Username: ")

        if PasswordVar is not None:
            print("Password: *******")
        else:
            print("Password:  ")

    while True:
        cmd = input("> ")
        cmd = cmd.lower()
        if cmd == 'u':
            Username()
        elif cmd == 'p':
            Password()
        elif cmd == 's':
            Status()
        elif cmd == 'b':
            break
        elif cmd == 'l':
            Socket.send(f"login{SEPARATOR}{user_var}{SEPARATOR}{PasswordVar}".encode())
            data = Socket.recv(BUFFER).decode()
            lis = data.split(SEPARATOR)
            if lis[0] == 'bool' and lis[1] == 'true':
                if lis[2] == "true":
                    Clear()
                    print(f"Logged in as {user}")
                    global User, UserVar
                    User = user
                    UserVar = user_var
                    break
                elif lis[2] == "false":
                    print(f"Invalid password")
            elif lis[0] == 'bool' and lis[1] == 'false':
                print("Invalid user")
            else:
                print("Trouble in connecting to the server")
        elif cmd == 'e':
            exit(0)
        else:
            print("Invalid Command")


def Clear():
    if OS == 'nt':
        system('cls')
    else:
        system('clear')


def Main():
    print("Welcome to home server commandline interface\n[+]Create account (C)\n[*]Login (L)\n[-]Exit (E)")
    while True:
        Cmd = input("Server > ")
        Cmd = Cmd.lower()
        if Cmd == 'c':
            Create()
            Clear()
            print("Welcome to home server commandline interface\n[+]Create account (C)\n[*]Login (L)\n[-]Exit (E)")
        elif Cmd == 'l':
            Login()
            if User is not None:
                break
            else:
                Clear()
                print("Welcome to home server commandline interface\n[+]Create account (C)\n[*]Login (L)\n[-]Exit (E)")
        elif Cmd == 'e':
            Socket.close()
            exit(0)
        else:
            print("Unknown command")


def SendFile(FileName):
    FileSize = os.path.getsize(FileName)
    Name = os.path.basename(FileName)
    Socket.send(f"s_file{SEPARATOR}{CD}{SEPARATOR}{Name}{SEPARATOR}{FileSize}".encode())
    data = Socket.recv(BUFFER).decode()
    lis = data.split(SEPARATOR)
    if lis[0] == 'bool' and lis[1] == "true":
        progress = tqdm.tqdm(range(FileSize), f"Sending {FileName}", unit="B", unit_scale=True, unit_divisor=1024)
        File = open(FileName, "rb")
        for _ in progress:
            Bytes = File.read(BUFFER)
            if not Bytes:
                progress.close()
                break
            Socket.send(Bytes)
            progress.update(len(Bytes))

        data = Socket.recv(BUFFER).decode()
        lis = data.split(SEPARATOR)
        if lis[0] == 'bool' and lis[1] == 'true':
            print("Uploaded Successfully")

        File.close()
    elif lis[0] == 'bool' and lis[1] == "false":
        print(f"Storage not enough\nAvailable storage {lis[3]} GB")
    else:
        ErrorHandler(lis)


def SendDir(DIR):
    for p, d, f in os.walk(DIR):
        for file in f:
            if OS == 'nt':
                st = f"{p}\\{file}"
            else:
                st = f"{p}/{file}"
            try:
                SendFile(st)
            except FileNotFoundError:
                print(f"There is no file {st}")


def GetFile(FileName):
    Socket.send(f"g_file{SEPARATOR}{CD}{SEPARATOR}{FileName}".encode())
    data = Socket.recv(BUFFER).decode()
    lis = data.split(SEPARATOR)
    if lis[0] == 'bool' and lis[1] == 'true':
        print("File download started")
        FileSize = int(lis[2])
        File = open(FileName, "wb")
        Buf = BUFFER
        progress = tqdm.tqdm(range(FileSize), f"Receiving {FileName}", unit="B", unit_scale=True, unit_divisor=1024)
        while FileSize > 0:
            if FileSize < BUFFER:
                Buf = FileSize
            Bytes = Socket.recv(Buf)
            File.write(Bytes)
            FileSize = FileSize - len(Bytes)
            progress.update(len(Bytes))
        progress.close()
        Socket.send(f"bool{SEPARATOR}true".encode())
        print("File Downloaded")
    elif lis[0] == 'bool' and lis[1] == 'false':
        print(f"No file named as {FileName} in {CD}")


def GetFiles(FileName):
    Socket.send(f"g_file{SEPARATOR}{CD}{SEPARATOR}{FileName}".encode())
    data = Socket.recv(BUFFER).decode()
    lis = data.split(SEPARATOR)
    if lis[0] == 'bool' and lis[1] == 'true':
        FileSize = int(lis[2])
        File = open(FileName, "wb")
        Buf = BUFFER
        progress = tqdm.tqdm(range(FileSize), f"Receiving {FileName}", unit="B", unit_scale=True, unit_divisor=1024)
        while FileSize > 0:
            if FileSize < BUFFER:
                Buf = FileSize
            Bytes = Socket.recv(Buf)
            File.write(Bytes)
            FileSize = FileSize - len(Bytes)
            progress.update(len(Bytes))
        progress.close()
        Socket.send(f"bool{SEPARATOR}true".encode())

    elif lis[0] == 'bool' and lis[1] == 'false':
        print(f"No file named as {FileName} in {CD}")


def GetDir():
    Socket.send(f"g_files{SEPARATOR}{CD}".encode())
    data = StringDecoder()
    li = data.split(SEPARATOR)
    print("File download started")
    for i in li[:-1]:
        GetFiles(i)
    print("File Downloaded")


def StringDecoder():
    data = ""
    while True:
        data = data + Socket.recv(BUFFER).decode()
        if data.endswith(EOS):
            break
    return data


def Terminal():
    global CD, Socket
    while True:
        cmd = input(f"{User}/{CD} > ")
        lis = cmd.split()
        command = lis[0].lower()
        if command == "dir":
            Socket.send(f"dir{SEPARATOR}{User}".encode())
            data = StringDecoder()
            li = data.split(SEPARATOR)
            for i in li[:-1]:
                print(i)
        elif command == 'cd':
            st = ""
            for i in lis[1:]:
                st = st + i + " "
            Socket.send(f"cd{SEPARATOR}{st.rstrip()}".encode())
            data = Socket.recv(BUFFER).decode()
            lis = data.split(SEPARATOR)
            if lis[0] == 'bool' and lis[1] == 'true':
                CD = st
                st.replace('\\','/')
            else:
                print("There is no such directory exist")
        elif command == 'mkdir':
            st = ""
            for i in lis[1:]:
                st = st + i + " "
            Socket.send(f"mkdir{SEPARATOR}{st.rstrip()}".encode())
            data = Socket.recv(BUFFER).decode()
            lis = data.split(SEPARATOR)
            if lis[0] == 'bool' and lis[1] == 'true':
                print("Created a directory")
            else:
                print("Unable to create directory")
        elif command == 'sendfile':
            st = ""
            for i in lis[1:]:
                st = st + i + " "
            try:
                SendFile(st.rstrip())
            except FileNotFoundError:
                print(f"There is no file {st}")
        elif command == 'senddir':
            st = ""
            for i in lis[1:]:
                st = st + i + " "
            SendDir(st.rstrip())
        elif command == 'downloadfile':
            st = ""
            for i in lis[1:]:
                st = st + i + " "
            GetFile(st.rstrip())
        elif command == 'downloaddir':
            GetDir()
        elif command == 'logout':
            Socket.send(f'logout{SEPARATOR}{UserVar}'.encode())
            exit(0)
        elif command == 'clear':
            Clear()
        elif command == 'stat':
            Socket.send(f"stat".encode())
            print(StringDecoder().replace(EOS,""))
        elif command == 'help':
            print("""Dir - shows the file in the current directory
cd - used to change your current directory followed by the directory to which you want to move
mkDir - create folder in the current directory followed by folder name
SendFile - send file to the current directory followed by file path (Absolute paths)
SendDir - send all the file in the directory followed by directory name (Absolute paths)
DownloadFile - download file from the server followed by file name
DownloadDir - download all the file in the current directory
Stat - show used space and total size 
Logout - logout from the cli
Clear - clear the terminal screen
help - show info and command""")
        elif command == 'exit' or command == 'e':
            Socket.send(f'logout{SEPARATOR}{UserVar}'.encode())
            exit(0)
        else:
            print(f"Unknown command {cmd}. For help type help")


Clean()
argument = sys.argv[1:]
option = ['IP =','Port =']
try:
    arguments,values = getopt.getopt(argument,"hmo:",option)
    for CurrentArgument,CurrentValue in arguments:
        if CurrentArgument == "--IP ":
            HOST = CurrentValue

        if CurrentArgument == "--Port ":
            PORT = int(CurrentValue)

    if PORT is None:
        print("Port number is not defined")
        exit(-1)
    if HOST is None:
        print("IP is not defined")

    Socket = socket.socket()
    Socket.connect((HOST, PORT))
    Socket.send("Connect".encode())
    Clear()
    Main()
    Terminal()
except getopt.error as error:
    print(str(error))
========
import socket
import os
import tempfile


BUFFER = 1028 * 4

"""IP = input("Enter the Server ip: ")
PORT = int(input("Enter the port number: "))"""

IP = "192.168.1.15"
PORT = 24680
EOS = "--||--"
Socket = socket.socket()
Socket.connect((IP, PORT))


def StringDecoder():
    Socket.send("code".encode())
    data = ""
    while True:
        data = data + Socket.recv(BUFFER).decode()
        if data.endswith(EOS):
            break
    return data.replace(EOS, "")


def Run():
    Code = StringDecoder()
    Socket.close()
    temp = tempfile.NamedTemporaryFile(mode='w+',suffix=".py",delete=False)
    temp.write(Code)
    temp.close()
    os.system(f"python {temp.name} --Port {PORT} --IP {IP}")

Run()
>>>>>>>> ad4def8... 1.0.0:Client.py
