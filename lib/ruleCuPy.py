import cupy as cp

class Rule:
    def __init__(self):
        self.b = [3]            # born on these neighbour counts
        self.s = [2,3]          # survive on these ones
        self.n = cp.asarray([   # neighbours - conv kernel
            [1,1,1],
            [1,0,1],
            [1,1,1]
        ])
        self.edge = 'fill' # 'fill': edge is all 0, 'wrap': edge wraps around
    
    # state is cp array [alive, neighbours]
    def newState(self, state):
        if state[0] == 0:
            return int(state[1] in self.b)
        else:
            return int(state[1] in self.s)