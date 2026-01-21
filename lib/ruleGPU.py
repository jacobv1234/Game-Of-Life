import numpy as np
import numba as nb
import numba.cuda as cuda

class Rule:
    def __init__(self, b=[3],s=[2,3], n=[[1,1,1],[1,0,1],[1,1,1]], edge='fill', hex=False): # default values correspond to standard Life
        self.b = b         # born on these neighbour counts
        self.s = s         # survive on these ones
        self.n = np.asarray(n)         # neighbours: convolution kernel
        self.edge = edge   # 'fill': edge is all 0, 'wrap': edge wraps around
        self.hex = hex     # denotes if the grid is hexagonal
    
    # newState function is moved into gridGPU