import numpy as np
import numba as nb
import numba.cuda as cuda
from time import perf_counter

from lib.ruleGPU import Rule
from lib.nextState import GPUInterFace

class Grid:
    def __init__(self, rule: Rule):
        self.gridsize = 512
        self.grid = np.zeros(self.gridsize**2, dtype='byte')
        self.grid = self.grid.reshape((self.gridsize,self.gridsize))
        self.rule = rule
        self.gens = 0
        self.processingTime = 0
        self.population = 0
        self.population_history = [0]

        self.GPUInterface = GPUInterFace(self.gridsize)
    
    def toggle(self, x: int, y: int):
        self.grid[x][y] = 1 - self.grid[x][y]
        self.gens = 0
        self.population = int(np.sum(self.grid))
        self.population_history = [self.population]
        return self.grid[x][y]

    def set(self,x:int,y:int,s:int):
        self.gens = 0
        self.grid[x][y] = s
        self.population = int(np.sum(self.grid))
        self.population_history = [self.population]
    
    def reset(self):
        self.grid = np.zeros(self.gridsize**2, dtype='byte')
        self.grid = self.grid.reshape((self.gridsize,self.gridsize))
        self.gens = 0
        self.population = 0
        del self.population_history # force memory cleanup
        self.population_history = [0]
    
    # NEXT GENERATION - GPU EDITION
    def next(self):
        oldState = self.grid
        start = perf_counter()
        self.GPUInterface.nextState(self.grid, self.rule)
        end = perf_counter()
        del oldState # force memory cleanup
        self.processingTime = end - start
        self.gens += 1
        self.population = int(np.sum(self.grid))
        self.population_history.append(self.population)

    
    def changeRule(self, rule: Rule):
        self.rule = rule
        