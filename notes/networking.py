# Echo server program
import socket
import json

HOST = '127.0.0.1'  # IP Address of the computer hosting.
# #For local machines you can use 127.0.0.1
PORT = 50007  # Arbitrary non-privileged port


def create_socket(THEPORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # s = variable name
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, THEPORT))
        s.listen(1)  # Listen for 1 connection only
        return s.accept()


while True:
    conn, addr = create_socket(PORT)
    print('Connected by', addr)

    data = conn.recv(1024)  # Receive 1024 bytes from the client
    if data:
        print('Data:', data)
        try:
            data = json.loads(data.decode())
            print(data, type(data))
            conn.sendall("{} has connected!".format(data['Name']).encode())
        except json.decoder.JSONDecodeError:
            conn.sendall(data)

