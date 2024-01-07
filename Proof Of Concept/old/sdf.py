print([34, 5, 2].replace(34, 2))

# print(not 0)
# print(' ' in ' dsfdf')

# a = [23, 45, 3]
# b = [45]
# print(a - b)

# a = 'dfsdfsd'
# for letter in a:
#     for i in range(9):
#         if letter == 's':
#             break
#         print(i, letter)


# print('fsdfsd'.count('f'))
# for i in range(6):
#     for b in range(3):
#         if b == 2:
#             break
#         print(i, b)

# To change value of 5th index:
# a = 'fdsfsdgfdh'
# print(len(a))
# a = a[:4] + '5' + a[5:]
# print(a, len(a))

# a = ['f'*8, 'g'*8, 'c'*8]
# b = [x[:] for x in a]
# b[0] = b[0][:5] + '6' + b[0][5:-1]
# print(a)
# print(b)

# l = 'f'*8
# a = l[:5] + '4' + l[5:-1]
# print(l)
# print(a)

#
# i[0]='f'
# possible_goals = [(0, 4, 8), (2, 4, 6)]
# possible_goals += [(i, i+3, i+6) for i in range(3)]
# possible_goals += [(3*i, 3*i+1, 3*i+2) for i in range(3)]
# print(possible_goals)

# a = [[[['hi', ' ', 'hey'], ['whys ', ' ', ' '], [' ', ' ', ' ']],
#                [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#                [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]],
#
#                [[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#                 [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#                 [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]],
#
#                [[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#                 [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#                 [[' ', ' ', ' '], [' ', 'hjh', ' '], [' ', ' ', ' ']]]]


# class Bye:
#     def __init__(self, a):
#         self.a = a
#
# a = Bye([[[['hi', ' ', 'hey'], ['whys ', ' ', ' '], [' ', ' ', ' ']],
#                [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#                [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]],
#
#                [[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#                 [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#                 [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]],
#
#                [[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#                 [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#                 [[' ', ' ', ' '], [' ', 'hjh', ' '], [' ', ' ', ' ']]]])
# # a = [[[[['he', 'p'], ['k', 2], [5]]]]]
# b = a
# a.a[0][0][0][0] = 'ehfsdfdsf'
# print(a.a)
# print(b.a)
# # b = [z for w in a for x in w for y in x for z in y]
# print(b)
# row = []
# grid = []


# def seperate(alist):
#     new_list = []
#     for i in range(len(alist)):
#         if i % 3 == 0:
#             print(i)
#             seperations = [a[:] for a in alist[i:i+3]]
#             new_list.append(seperations)
#     return new_list
#
# b = seperate(seperate(seperate(b)))
# for i in b:
#     print(i)

# a[0][0][0][0] = 'ehllo'
#
# print(a)
# print(b)
# print(a == b)
# print(['W'] * 3)

# a = [['O'] * 3 for x in range(3)]
# print(any('O' or 'X' in e for e in a))
# a[0][1] = 'DE'
# print(a)


# a = 'fdsf'
# for i in a:
#     print(i)

# a = [[[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#       [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#       [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]],
#
#      [[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#       [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#       [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]],
#
#      [[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#       [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
#       [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]]]
# a[0][0][0][0] = 'HELLO'
# for i in a:
#     print(i)

# b = [[' '] * 9] * 9
# print(b)

# a_state = [23, 342, 45]
# b_state = a_state[:1]
# b_state.append('he')
# print(a_state)
# print(b_state)

# hello = {'ab': 233, 'fsdsddf': [4234, 4352342466765875]}
# print(233 in hello)



# state = [['X', 'X', 'O'], ['O', 'O', 'X'], ['', 'X', 'O']]
# a_state = [x[:] for x in state]
# a_state[1][1] = 'sdfdsfsd'
# print(state)
# print(a_state)
# print(['O', 'X', 'O'].count('O'))
#

# When simulating, never miss out on a win and always miss out on a loss


# node_children = self.get_children(selected_node, get_turn(selected_node.state, self.symbols))
# current_node = selected_node
#
# while len(node_children) > 0:
#     current_node = random.choice(node_children)
#
#     for node in node_children:
#         if self.check_win(node.state) == (1, 1):
#             current_node = node
#             break
#         elif self.check_win(node.state) == (0, 1):
#             node_children.remove(node)
#             current_node = random.choice(node_children)
#
#     node_children = self.get_children(current_node, get_turn(current_node.state, self.symbols))
#
# W1, n1 = selected_node.value
# W2, n2 = self.check_win(current_node.state)  # last edited here...
# selected_node.value = (W1 + W2, n1 + n2)
