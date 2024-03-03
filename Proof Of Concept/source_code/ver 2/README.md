# Notes

29.02.24

Lineage of selected node which is not in possible moves:
(equivalent to selection order of nodes in selection)

[(4, 1), (1, 2), (2, 8), (8, 2), (2, 0), (0, 2), (2, 7), (7, 8), (8, 5), (5, 4), (4, 5), (5, 1), (1, 5), (5, 7), (7, 1), (1, 3), (3, 3), (3, 6), (6, 7), (7, 7), (7, 6), (6, 6), (6, 1), (1, 0), (0, 7), (7, 4), (4, 3), (3, 8), (8, 1), (1, 4), (3, 7), (7, 5), (1, 1), (1, 8), (8, 7), (7, 2), (2, 2), (2, 4), (8, 3), (3, 4), (2, 1), (0, 4), (6, 3), (3, 1), (0, 5), (3, 0), (0, 8), (8, 8), (8, 4), (6, 2), (0, 6), (6, 4), (4, 6)]


The "current state" at 4 during the not in possible moves exception: (the exceptional move (4,6) not included)
[' ', 'O', ' ', 'O', 'O', 'O', ' ', ' ', ' ']

equivalent to:
\_O_
OOO
X__

((4,6) included as X)

What the actual current state should be at the node (4,6):
same as the above, except the player is swapped.
------------
|  O|OXO|XXX|
| OX|OOX| O |
|XXX|  O| XX|
------------
|OO | X | O |
|XO |XOX| O |
|OXO|X  | O |
------------
| XO| XO| XO|
|XO | OO|XXX|
|OX |XOO| XO|
------------


something is going wrong with the player

unsure about line 126:
self.player = Globals.swap(self.player)


01.03.24

finally fixed player problem

now check all the details and functions
correct
optimise


02.03.24
 i need to initialise the first child nodes with the UTC value
 whenever I generate a child node, i need to calculate its UTC
 otherwise UTC is only updated by selecting a node then backpropogating it
 it wont update its siblings.