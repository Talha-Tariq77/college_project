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
        
    def get_lineage(self):
        lineage = []
        current = self
        while current.parent is not None:
            lineage.append(current.prev_move)
            current = current.parent
        lineage.reverse()
        
        return lineage