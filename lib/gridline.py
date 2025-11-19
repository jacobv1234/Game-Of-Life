from tkinter import *
from typing import Literal

class GridLine:
    """
    Create a gridline on the canvas.\n
    c: the canvas to create on.\n
    coord: y coord for a horizontal line, x coord for vertical\n
    e1,e2: left/right edges for a horizontal line, top/bottom for vertical\n
    dir: 'h': horizontal line, 'v': vertical line
    """
    def __init__(self, c: Canvas, coord, e1,e2, dir: Literal['h','v']):
        self.c = c
        self.dir = dir
        self.coord = coord
        if dir == 'h':
            self.line = self.c.create_line(e1,coord,e2,coord,fill='#999999')
        else:
            self.line = self.c.create_line(coord,e1,coord,e2,fill='#999999')
    
    # move ending coords of line (to keep on screen)
    def fix(self,offset):
        if self.dir == 'h':
            self.c.move(self.line, offset, 0)
        else:
            self.c.move(self.line, 0, offset)
    
    def remove(self):
        self.c.delete(self.line)