import threading
import time


def alphabet():
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print(char)
        time.sleep(1)


def counter():
    for x in range(50):
        print(x,"")
        time.sleep(0.5)


my_thread = threading.Thread(target=alphabet)
my_thread.start()
counter()
