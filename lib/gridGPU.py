import numpy as np
import numba as nb
import numba.cuda as cuda

from lib.ruleGPU import Rule
from lib.nextState import nextGPU

class Grid:
    def __init__(self, rule: Rule):
        self.gridsize = 512
        self.grid = np.zeros(self.gridsize**2, dtype='byte')
        self.grid = self.grid.reshape((self.gridsize,self.gridsize))
        self.rule = rule
        self.gens = 0
        self.population = 0
    
    def toggle(self, x: int, y: int):
        self.grid[x][y] = 1 - self.grid[x][y]
        self.gens = 0
        self.population = np.sum(self.grid)
        return self.grid[x][y]

    def set(self,x:int,y:int,s:int):
        self.gens = 0
        self.population = np.sum(self.grid)
        self.grid[x][y] = s
    
    def reset(self):
        self.grid = np.zeros(self.gridsize**2, dtype='byte')
        self.grid = self.grid.reshape((self.gridsize,self.gridsize))
        self.gens = 0
        self.population = 0
    
    # NEXT GENERATION - GPU EDITION
    def next(self):
        blocks = (self.gridsize,self.gridsize)
        threads = 1
        newState = np.zeros(shape=(self.gridsize,self.gridsize))
        nextGPU[blocks,threads](self.grid,   # type: ignore
                                np.asarray(self.rule.b),
                                np.asarray(self.rule.s),
                                np.asarray(self.rule.n),
                                int(self.rule.edge=='wrap'),
                                self.gridsize, newState)
        self.grid = newState
        self.gens += 1
        self.population = np.sum(self.grid)

    


    
    def changeRule(self, rule: Rule):
        self.rule = rule
        