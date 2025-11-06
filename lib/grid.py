import numpy as np
from scipy.signal import convolve2d
from time import perf_counter

from lib.rule import Rule

class Grid:
    def __init__(self, rule: Rule):
        self.gridsize = 500
        self.grid = np.zeros(self.gridsize**2, dtype='byte')
        self.grid = self.grid.reshape((self.gridsize,self.gridsize))
        self.rule = rule
    
    def toggle(self, x: int, y: int):
        self.grid[x][y] = 1 - self.grid[x][y]
        return self.grid[x][y]

    def set(self,x:int,y:int,s:int):
        self.grid[x][y] = s
    
    def nextSlow(self):
        newState = np.zeros(self.gridsize**2, dtype='byte').reshape((self.gridsize,self.gridsize))

        # original algorithm
        # VERY SLOW
        # iterate every cell
        for xi in range(self.gridsize):
            for yi in range(self.gridsize):
                # count neighbours
                n = 0
                for xo in range(-1,2,1):
                    for yo in range(-1,2,1):
                        # skip self
                        if xo==0 and yo==0:
                            continue
        
                        nx, ny = xi+xo, yi+yo
                        # edge behaviour
                        if nx < 0 or ny < 0 or nx >= self.gridsize or ny >= self.gridsize:
                            continue

                        n += self.grid[nx][ny]
                
                # change state
                newState[xi][yi] = self.rule.newState(self.grid[xi][yi], n)

        self.grid = newState


    def next(self):
        # this line can't be better until using cupy
        neighbour_counts = convolve2d(self.grid, self.rule.n, mode='same', boundary=self.rule.edge, fillvalue=0)

        # this line can still be better
        newState = np.asarray([[self.rule.newState(self.grid[x][y], neighbour_counts[x][y]) for y in range(self.gridsize)]
                                                                                            for x in range(self.gridsize)])

        self.grid = newState
        