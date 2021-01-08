import socket
import Server

BUFFER = 1024 * 4
EOS = "--||--"
Port = 13579

IP = input("Enter the server local ip: ")
PORT = int(input("Enter the port number: "))
Mount = input(" Enter the Parent directory to store data: ")

Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
Sock.bind((IP, Port))
Sock.listen(100)
