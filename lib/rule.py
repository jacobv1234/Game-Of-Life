class Rule:
    def __init__(self):
        self.b = [3]         # born on these neighbour counts
        self.s = [2,3]       # survive on these ones
        self.n = [           # neighbours - conv kernel
            [1,1,1],
            [1,0,1],
            [1,1,1]
        ]
        self.edge = 'fill' # 'fill': edge is all 0, 'wrap': edge wraps around
    
    def newState(self, state, neighbours):
        if state == 0:
            return int(neighbours in self.b)
        else:
            return int(neighbours in self.s)