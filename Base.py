import Server


BUFFER = 1024 * 4
EOS = "--||--"
Port = 13579

IP = input("Enter the server local ip: ")
PORT = int(input("Enter the port number: "))
Mount = input("Enter the Parent directory to store data: ")
Max = int(input("Enter maximum number of connections permitted "))

Server.SERVER_HOST = IP
Server.SERVER_PORT = PORT
Server.BASE = Mount
Server.Max = Max

Server.Start()
