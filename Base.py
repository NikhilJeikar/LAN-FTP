import socket
import Server

BUFFER = 1024 * 4
EOS = "--||--"
Port = 13579

IP = input("Enter the server local ip: ")
PORT = int(input("Enter the port number: "))
Mount = input(" Enter the Parent directory to store data: ")

