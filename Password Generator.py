import random


def generate_pass(x):
    for i in range(x):
        print(ord('a') + random.randint(0, 25))


