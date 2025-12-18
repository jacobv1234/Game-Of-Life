import numpy as np

class Rule:
    def __init__(self, b=[3],s=[2,3], n=[[1,1,1],[1,0,1],[1,1,1]], edge='fill', hex=False): # default values correspond to standard Life
        self.b = b         # born on these neighbour counts
        self.s = s         # survive on these ones
        self.n = n         # neighbours: convolution kernel
        self.edge = edge   # 'fill': edge is all 0, 'wrap': edge wraps around
        self.hex = hex     # denotes if the grid is hexagonal
    
    # state is np array [alive, neighbours]
    def newState(self, state):
        if state[0] == 0:
            return int(state[1] in self.b)
        else:
            return int(state[1] in self.s)