import socket

from protocol import *

def connect_to_server():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((CLIENT_HOST,PORT))
    while client is not None:
        msg = input("[Client] Enter message: ")
        client.send(msg.encode())


if __name__ == "__main__":
    connect_to_server()