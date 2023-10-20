import node_old
import math
import random

class MonteCarlo:
    def __init__(self, iterate, grid, prev_move=None):
        self.root = Node(parent=None, children=[], state=grid, root=True, prev_move=prev_move)
        self.C = 2 ** 0.5
        self.iterate = iterate
        self.count = 0

    def get_UCT(self, node):
        # Parameters :- node:Node
        # Return Type :- float
        # Purpose :- Calculates a UCT value for a Node and returns it
        if node.parent:
            W = node.value[0]
            n = node.value[1]
            N = node.parent.value[1]
            if n == 0:
                return math.inf
            else:
                return W / n + (self.C * math.sqrt(math.log(N) / n))
        else:
            return math.inf

    def select(self, node):
        # Parameters :- node:Node
        # Return Type :- Node
        # Purpose :- Finds the leaf Node and the pathway to it which maximises the UCT equation
        while len(node.possible_moves) == 0:
            for child_node in node.children:
                child_node.UCT = self.get_UCT(child_node)

            children_sorted = sorted(node.children, reverse=True, key=lambda each_node: each_node.UCT)
            node = children_sorted[0]

            # Randomise equal nodes:
            equal_UCT_nodes = []

            for sorted_node in children_sorted:
                if sorted_node.UCT == node.UCT:
                    equal_UCT_nodes.append(sorted_node)

            if len(equal_UCT_nodes) > 0:
                node = random.choice(equal_UCT_nodes)
        return node

    def expand(self, node):
        # Parameters :- node:Node
        # Return Type :- Node
        # Purpose :- creates and returns a random child node of the node
        expansion_move = random.choice(node.possible_moves)
        new_child_node = self.create_child_node(parent=node, move=expansion_move)

        return new_child_node

    def simulation(self, selected_node):
        # Parameters :- selected_node:Node
        # Return Type :- tuple
        # Purpose :- Simulates a random game from selected_node and returns the terminal state: (W, L, D)
        current_player = selected_node.current_player
        current_state = selected_node.state[:]
        prev_move = selected_node.prev_move

        is_terminal = check_win(current_state)

        while is_terminal is None:
            possible_moves = get_valid_moves(current_state, prev_move)

            random_move = random.choice(possible_moves)

            ra, rb = random_move
            current_state[ra] = current_state[ra][:rb] + symbols[current_player] \
                                + current_state[ra][rb + 1:]
            is_terminal = check_win(current_state)
            prev_move = random_move
            current_player = opposite(current_player)

        return is_terminal

    def simulate(self, selected_node):
        # Parameters :- selected_node:Node
        # Return Type :- None
        # Purpose :- adds the correct values to the correct Nodes, calls the simulation and back_propagate methods
        sim_result = self.simulation(selected_node)

        W1, n1 = selected_node.value
        W2, n2 = sim_result
        selected_node.value = (W1 + W2, n1 + n2)
        self.back_propagate(selected_node, (W2, n2))

    def back_propagate(self, simulated_node, value):
        # Parameters :- simulate_node: Node, value:tuple
        # Return Type :- None
        # Purpose :- adds value to the Node.value of each parent of the simulated_node until root is reached
        W2, n2 = value
        while simulated_node.parent is not None:
            W1, n1 = simulated_node.parent.value
            simulated_node.parent.value = (W1 + W2, n1 + n2)
            simulated_node = simulated_node.parent

    def Monte_Carlo(self):
        # Parameters :- None
        # Return Type :- Node
        # Purpose :- Executes the MCTS algorithm and calls the make_move, returns the best move
        while self.count <= self.iterate:
            # select the node with the highest UCT value
            selected_leaf = self.select(self.root)

            # if Node hasn't been visited
            if selected_leaf.value[1] == 0:
                # simulate a game from the Node and back propagate it
                self.simulate(selected_leaf)

            else:  # if Node has been visited
                # expand the Node
                simulation_node = self.expand(selected_leaf)

                # and simulate the new Child Node
                self.simulate(simulation_node)

            self.count += 1

        # AI move is the immediate child node
        # of the root that has been visited most
        move_node = self.make_move()

        return move_node

    def make_move(self):
        # Parameters :- None
        # Return Type :- Node
        # Purpose :- Finds best move Node, returns it
        max_visits = 0
        move_node = None

        for node in self.root.children:
            if node.value[1] >= max_visits:
                max_visits = node.value[1]
                move_node = node

        return move_node

    def create_child_node(self, parent, move):
        # Parameters :- parent:Node, move:tuple
        # Return Type :- Node
        # Purpose :- Creates child_node such that parent+move=child_node
        child_node = Node(parent, [], prev_move=move, state=parent.state[:])

        a, b = move
        child_node.state[a] = child_node.state[a][:b] + symbols[parent.current_player] \
                              + child_node.state[a][b + 1:]

        parent.possible_moves.remove(move)
        child_node.parent.children.append(child_node)
        return child_node


