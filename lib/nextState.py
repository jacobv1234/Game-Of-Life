# GPU function that calculates the next state of a grid
import numpy as np
import numba as nb
import numba.cuda as cuda


# Rule cant be passed in directly
@cuda.jit
def nextGPU(state: np.ndarray, b: list, s: list, n: np.ndarray, edge: str, gridSize: int):
    x, y = int(cuda.threadIdx.x), int(cuda.threadIdx.y) #type:ignore

    cellState = state[y, x]

    # convolution - getting neighbourhood
    neighbourhood = np.zeros_like(n)
    for yo in range(-1,2,1):
        for xo in range(-1,2,1):
            y1,x1 = y+yo, x+xo

            # edge behaviour
            if y1 < 0 or y1 >= gridSize or x1 < 0 or x1 >= gridSize:
                if edge == 'wrap':
                    y1 %= gridSize
                    x1 %= gridSize
                else:
                    neighbourhood[yo+1, xo+1] = 0
                    continue

            neighbourhood[yo+1, xo+1] = state[y1, x1]
    
    # convolution - counting neighbours
    count = np.sum(neighbourhood * n)

    # game of life stuff
    if (cellState == 0 and count in b) or (cellState == 1 and count in s):
        state[y][x] = 1
    else:
        state[y][x] = 0

# testing
if __name__ == '__main__':
    state = np.asarray([
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,0,0,0]
    ])

    blocks = 1
    threads = (5,5)
    nextGPU[blocks,threads](state, [3], [2,3], [[1,1,1],[1,0,1],[1,1,1]], 'wrap', 5) # type: ignore

    print(state)