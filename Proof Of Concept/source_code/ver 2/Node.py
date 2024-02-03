from Globals import *

class Node:
    def __init__(self, prev_move, parent=None):
        self.prev_move = prev_move
        self.parent = parent
        self.children = []
        self.win = 0
        self.sim = 0
        self.UTC = 0
    # prev_move, UTC values