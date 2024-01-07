1.	import math
2.	import random
3.
4.	game_tree = {0: []}
5.
6.
7.	class Node:
8.	    def __init__(self, parent, children, state=None, UCT=None, root=False):
9.	        self.parent = parent
10.	        self.children = children
11.	        self.value = (0, 0)
12.	        self.state = state
13.	        self.root = root
14.	        if root:
15.	            self.depth = 0
16.	        else:
17.	            self.depth = self.parent.depth + 1
18.	        self.add_to_game_tree()
19.
20.	    def add_to_game_tree(self):
21.	        if not self.root:
22.	            if not len(game_tree) > self.depth:
23.	                game_tree[self.parent.depth + 1] = []
24.	        game_tree[self.depth].append(self)
25.
26.	    def __repr__(self):
27.	        return '{}, {}, {}'.format(self.state, self.value, self.depth)
28.
29.	    def display_node(self):
30.	        for row in self.state:
31.	            for pos in row:
32.	                if pos == ' ':
33.	                    print('☐', end='')
34.	                else:
35.	                    print(pos, end='')
36.	            print()
37.	        print(self)
38.
39.	    def print_lineage(self):
40.	        node = self
41.	        print(node)
42.	        while node.parent != None:
43.	            print(node.parent)
44.	            node = node.parent
45.	        else:
46.	            print(node)
47.
48.
49.	game_state = [[' ', ' ', ' '],
50.	              [' ', ' ', ' '],
51.	              [' ', ' ', ' ']]
52.
53.	results = []
54.
55.	root = Node(parent=None, children=[], state=game_state, root=True)
56.
57.
58.	class MonteCarlo:
59.	    def __init__(self, grid, turn=1):
60.	        self.local_grid = grid
61.	        self.symbols = ['X', 'O']
62.	        self.player = 1
63.	        self.C = 1
64.	        self.turn = turn
65.
66.	    def get_UCT(self, node):
67.	        if node.parent != None:
68.	            W = node.value[0]
69.	            n = node.value[1]
70.	            N = node.parent.value[1]
71.	            if n == 0:
72.	                return math.inf
73.	            else:
74.	                return W/n + (self.C * math.sqrt(math.log(N)/n))
75.	        else:
76.	            return math.inf
77.
78.	    def select(self, node):
79.	        UCT_maximum = 0
80.	        UCT_maximiser = None
81.	        if node.children:
82.	            for child_node in node.children:
83.	                if self.get_UCT(child_node) > UCT_maximum:
84.	                    UCT_maximum = self.get_UCT(child_node)
85.	                    UCT_maximiser = child_node
86.	            return UCT_maximiser
87.	        else:
88.	            return node
89.
90.	    def check_move(self, grid, coordinate):
91.	        x, y = coordinate
92.	        if grid[y][x] != ' ':
93.	            return False
94.	        else:
95.	            return True
96.
97.	    def get_children(self, node):
98.	        for x in range(3):
99.	            for y in range(3):
100.	                if self.check_move(node.state, (x, y)):
101.	                    new_child = Node(node, [])
102.	                    new_child.state = [x[:] for x in node.state]
103.	                    new_child.state[y][x] = self.symbols[self.turn % 2]
104.	                    node.children.append(new_child)
105.
106.	    def expand(self, node):
107.	        self.get_children(node)
108.	        return random.choice(node.children)
109.
110.	    def simulate(self, selected_node):
111.	        self.get_children(selected_node)
112.	        copy_node = selected_node
113.	        while len(copy_node.children) > 0:
114.	            copy_node = random.choice(copy_node.children)
115.	            self.get_children(copy_node)
116.	        W1, n1 = selected_node.value
117.	        W2, n2 = self.check_win(copy_node.state)
118.	        selected_node.value = (W1 + W2, n1 + n2)
119.
120.	    def back_propagate(self, simulated_node):
121.	        while simulated_node.parent != None:
122.	            W1, n1 = simulated_node.parent.value
123.	            W2, n2 = simulated_node.value
124.	            simulated_node.parent.value = (W1 + W2, n1 + n2)
125.	            simulated_node = simulated_node.parent
126.
127.	    def Monte_Carlo(self):
128.	        while self.turn <= 100:
129.	            selected_leaf = self.select(game_tree[0][0])
130.	            if selected_leaf.value[1] == 0:
131.	                self.simulate(selected_leaf)  # VALUE IS ADDED TO SELECTED LEAF
132.	                self.back_propagate(selected_leaf)
133.	            else:
134.	                simulation_node = self.expand(selected_leaf)
135.	                self.simulate(simulation_node)
136.	                self.back_propagate(simulation_node)
137.	            self.turn += 1
138.	        self.make_move().display_node()
139.
140.	    def make_move(self):
141.	        simulation_max = 0
142.	        move_node = None
143.	        for node in game_tree[1]:
144.	            if node.value[1] > simulation_max:
145.	                simulation_max = node.value[1]
146.	                move_node = node
147.	        return move_node
148.
149.	    def get_winners(self, grid):
150.	        winners = []
151.	        # horizontal
152.	        for x in range(len(grid)):
153.	            winners.append(grid[x])
154.
155.	        # vertical
156.	        for y in range(len(grid[0])):
157.	            col = []
158.	            for row in range(len(grid)):
159.	                col.append(grid[row][y])
160.	            winners.append(col)
161.
162.	        right_down = []
163.	        left_down = []
164.
165.	        for y in range(len(grid)):
166.	            for x in range(len(grid[y])):
167.	                if y == x:
168.	                    right_down.append(grid[y][x])
169.	                if y == -x + 2:
170.	                    left_down.append(grid[y][x])
171.	        winners.append(right_down)
172.	        winners.append(left_down)
173.	        return winners
174.
175.	    def board_filled(self, grid):
176.	        for row in grid:
177.	            if ' ' in row:
178.	                return False
179.	        return True
180.
181.	    def check_win(self, grid):
182.	        for row in self.get_winners(grid):
183.	            if row == [self.symbols[self.player - 1]] * 3:
184.	                return 1, 1  # WIN
185.	            elif row == [self.symbols[self.player - 2]] * 3:
186.	                return 0, 1  # LOSS
187.
188.	        if self.board_filled(grid):
189.	            return 0.5, 1  # DRAW
190.
191.
192.	mont = MonteCarlo(game_state)
193.
194.	mont.Monte_Carlo()
