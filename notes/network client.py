import socket
import json
import sqlite3

HOST = '10.90.78.31'
PORT = 49999
connection = True
initialised = False

tables = {}

def display_data(info, table):
    info = json.loads(info)
    if table == 'products':
        columns = ['ID', 'Name', 'StockLevel', 'Price']
    else:
        columns = ['ID', 'CustomerName', 'Item', 'AmountOrdered', 'DateOrdered']

    for column in columns:
        print(column, end='    ')
    print()

    for record in info:
        for i in range(len(record)):
            print(record[i], end='    ')
        print()


def explore(s):
    request = {'table': '', 'command': 'describe', 'clause': ''}

    s.sendall(json.dumps(request).encode())
    for x in s.recv(1024).decode().split('"')[1::2][1:]:
        tables[x] = {}

    for table in tables:
        request['table'] = table
        s.sendall(json.dumps(request).encode())
        data = s.recv(1024).decode().split('"')[1::2][1:]
        print(data)
        new_data = []
        for dat in data:
            new_data.append(data.split(' ')[0])  # here we go
        tables[table] = new_data
    print(tables)


while connection:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    explore(s)
    request = {"table": None, "command": None}

    table = input("Table: ").lower()
    request['table'] = table
    command = input("Command: ").lower()
    request['command'] = command

    if command == 'insert':
        request["values"] = {}
        for field in tables[table]:
            request['values'][field] = input(field)
    else:
        clause = input("Clause: ").lower()
        request["clause"] = clause

    command_str = json.dumps(request)

    s.sendall(command_str.encode())
    data = s.recv(1024)
    str_data = data.decode()
    print('Recieved', str_data)
        # if command == 'select':
        #     display_data(str_data, table)

    #command = input("SQL expression: ")
        # tables = str_data.split('"')[1::2][1:]







