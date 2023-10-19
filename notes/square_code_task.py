max_length = 81

square_size = 9

allowed_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

square = []


def input_check(x):
    print(x)
    for char in x:
        if char not in allowed_chars and char not in [x.upper() for x in allowed_chars]:
            print("Error: Only Alphabet and Spaces are allowed")
            return False

    if len(x) > 81:
        print("Error: Maximum length is 81")
        return False
    return True


def create_square():
    divisor = len(plain_text) // square_size
    remainder = len(plain_text) % square_size

    for i in range(1, divisor + 1):
        square.append(plain_text[square_size * (i - 1): square_size * i])

    square.append(plain_text[-remainder:])


def encode():
    encoded = []
    for i in range(square_size):
        encoded_string = ""
        for row in square:
            if i < len(row):
                encoded_string += row[i]
        encoded.append(encoded_string)
    return encoded


plain_text = 'If man was meant to stay on the ground god would have given us roots'
plain_text = ''.join(plain_text.split(' '))

while not input_check(plain_text):
    plain_text = ''.join(input(": ").split(' '))

create_square()
print(square)

print(encode())

#change square length

