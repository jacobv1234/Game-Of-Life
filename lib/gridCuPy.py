import numpy as np
import cupy as cp
from cupyx.scipy.signal import convolve2d
from time import perf_counter

from lib.ruleCuPy import Rule

class Grid:
    def __init__(self, rule: Rule):
        self.gridsize = 500
        self.grid = cp.zeros(self.gridsize**2, dtype='byte')
        self.grid = self.grid.reshape((self.gridsize,self.gridsize))
        self.rule = rule
    
    def toggle(self, x: int, y: int):
        self.grid[x][y] = 1 - self.grid[x][y]
        return self.grid[x][y]

    def set(self,x:int,y:int,s:int):
        self.grid[x][y] = s


    def next(self):
        neighbour_counts = convolve2d(self.grid, self.rule.n, mode='same', boundary=self.rule.edge, fillvalue=0)
        interleaved_state = cp.stack([self.grid, neighbour_counts], axis=2)
        newState = cp.apply_along_axis(self.rule.newState, 2, interleaved_state)
        self.grid = newState
    
        