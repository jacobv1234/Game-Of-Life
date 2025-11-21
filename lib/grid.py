import numpy as np
from scipy.signal import convolve2d
from time import perf_counter

from lib.rule import Rule

class Grid:
    def __init__(self, rule: Rule):
        self.gridsize = 512
        self.grid = np.zeros(self.gridsize**2, dtype='byte')
        self.grid = self.grid.reshape((self.gridsize,self.gridsize))
        self.rule = rule
        self.gens = 0
    
    def toggle(self, x: int, y: int):
        self.grid[x][y] = 1 - self.grid[x][y]
        self.gens = 0
        return self.grid[x][y]

    def set(self,x:int,y:int,s:int):
        self.gens = 0
        self.grid[x][y] = s
    
    def reset(self):
        self.grid = np.zeros(self.gridsize**2, dtype='byte')
        self.grid = self.grid.reshape((self.gridsize,self.gridsize))
        self.gens = 0
    
    def next(self):
        # this version can't be better until using cupy
        neighbour_counts = convolve2d(self.grid, self.rule.n, mode='same', boundary=self.rule.edge, fillvalue=0)
        interleaved_state = np.stack([self.grid, neighbour_counts], axis=2)
        newState = np.apply_along_axis(self.rule.newState, 2, interleaved_state)
        self.grid = newState
        self.gens += 1
    
    
        