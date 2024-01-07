yes = open('checking32.txt', encoding='utf-8')
i = 0
for line in yes.readlines():
    i += 1
    if i >= 100:
        print(line[5:], end='')
    elif i >= 10:
        print(line[4:], end='')
    elif i >= 1:
        print(line[3:], end='')
