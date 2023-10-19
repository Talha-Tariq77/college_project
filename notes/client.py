import socket
import json
import threading
import sys

HOST = '127.0.0.1'  # IP Address of the computer hosting.
# #For local machines you can use 127.0.0.1
PORT = 50007  # Arbitrary non-privileged port


def user_connect(port1):

    name = input("Name: ")
    user = {'Name': name}
    user = json.dumps(user)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, port1))
        s.sendall(user.encode())
        while True:
            sender = threading.Thread(target=send())
            reciever = threading.Thread(target=recieve(s))
            sender.start()
            reciever.start()


def send():
    message = input(': ')
    return message


def recieve(s):
    while True:
        data = s.recv(1024)
        if not data:
            sys.exit(0)
        print(data.decode())

# my_thread = threading.Thread(target=user_connect(50007))
# my_thread.start()

user_connect(50007)
