import __Server


BUFFER = 1024 * 4
EOS = "--||--"
Port = 13579

IP = input("Enter the server local ip: ")
PORT = int(input("Enter the port number: "))
Mount = input("Enter the Parent directory to store data: ")
Max = int(input("Enter maximum number of connections permitted "))

__Server.SERVER_HOST = IP
__Server.SERVER_PORT = PORT
__Server.BASE = Mount
__Server.Max = Max

__Server.Start()
