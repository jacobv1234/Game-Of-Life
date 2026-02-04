# GPU function that calculates the next state of a grid
import numpy as np
import numba as nb
import numba.cuda as cuda

from lib.ruleGPU import Rule

# Rule cant be passed in directly
# edge should be translated to int(rule.edge=='wrap') as cuda.jit functions don't like strings
@cuda.jit
def nextGPU(state: np.ndarray, b: np.ndarray, s: np.ndarray, n: np.ndarray, edge: int, gridSize: int, newState: np.ndarray):
    x, y = int(cuda.blockIdx.x), int(cuda.blockIdx.y) #type:ignore
    cellState = state[y, x]


    # convolution - getting neighbourhood
    #neighbourhood = np.zeros_like(n, dtype=np.int16)
    count = 0
    for yo in range(-1,2,1):
        for xo in range(-1,2,1):
            # skip if not a neighbour
            if n[yo+1,xo+1] == 0:
                continue

            y1,x1 = y+yo, x+xo

            # edge behaviour
            if y1 < 0 or y1 >= gridSize or x1 < 0 or x1 >= gridSize:
                if edge == 1:
                    y1 %= gridSize
                    x1 %= gridSize
                else:
                    continue
            #neighbourhood[y,x] += state[y1, x1]
            if state[y1,x1] == 1:
                count += 1

    # game of life stuff
    if cellState == 0:
        for i in range(len(b)):
            if b[i] == count:
                newState[y,x] = 1
                return
        newState[y,x] = 0
    else:
        for i in range(len(s)):
            if s[i] == count:
                newState[y,x] = 1
                return
        newState[y,x] = 0

class GPUInterFace:
    def __init__(self, gridsize:int):
        self.newState = cuda.device_array(shape=(gridsize, gridsize))
        self.stateOnGPU = cuda.device_array(shape=(gridsize, gridsize))
        self.gridsize = gridsize

    def nextState(self, currentState: np.ndarray, rule: Rule):
        blocks = (self.gridsize,self.gridsize)
        threads = 1
        self.stateOnGPU.copy_to_device(currentState)
        nextGPU[blocks,threads](self.stateOnGPU,   # type: ignore
                                np.asarray(rule.b),
                                np.asarray(rule.s),
                                np.asarray(rule.n),
                                int(rule.edge=='wrap'),
                                self.gridsize, self.newState)

        self.newState.copy_to_host(currentState)
