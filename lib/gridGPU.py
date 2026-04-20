import numpy as np
import numba as nb
import numba.cuda as cuda

from math import floor

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
        self.population_history = [0]
        self.stable = -1
    
    def toggle(self, x: int, y: int):
        self.grid[x][y] = 1 - self.grid[x][y]
        self.gens = 0
        self.population = int(np.sum(self.grid))
        self.population_history = [self.population]
        self.stable = -1
        return self.grid[x][y]

    def set(self,x:int,y:int,s:int):
        self.gens = 0
        self.grid[x][y] = s
        self.stable = -1
        self.population = int(np.sum(self.grid))
        self.population_history = [self.population]
    
    def reset(self):
        self.grid = np.zeros(self.gridsize**2, dtype='byte')
        self.grid = self.grid.reshape((self.gridsize,self.gridsize))
        self.stable = -1
        self.gens = 0
        self.population = 0
        self.population_history = [0]
    
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
        self.population = int(np.sum(self.grid))
        self.population_history.append(self.population)

        if self.population == 0 and self.stable == -1:
            self.stable = self.gens
        
        if self.stable == -1 and self.gens >= 10:
            self.stable = self.isStabilised()

    
    def changeRule(self, rule: Rule):
        self.rule = rule
    
    def isStabilised(self):
        if self.gens < 200:
            maskSize = floor(self.gens/2)
        else:
            maskSize = 100
        mask = self.population_history[-maskSize:]

        if all([val == mask[0] for val in mask]):
            return self.gens - maskSize + 1
        
        # 2 values: first, last
        # first is the index of the first value of the first comparison
        # last is the index of the last value of the first comparison = first value of last comparison
        first = (maskSize * -2)
        last = -maskSize - 1
        comparisons = [self.population_history[i:i+maskSize] for i in range(first, last+1)]
        #comparisons.append(self.population_history[last:])

        for i in range(len(comparisons)):
            if all([mask[j]==comparisons[i][j] for j in range(len(mask))]):
                return first + i + self.gens + 1
        return -1


        