from tkinter import *
from lib.gridline import GridLine

class GridLines:
    def __init__(self, c: Canvas, w:int, h:int, size:int = 20):
        self.c = c
        self.hlines = []
        self.vlines = []

        for i in range(0, h, size):
            self.hlines.append(
                GridLine(c,i,0,w,'h')
            )

        for i in range(0, w, size):
            self.vlines.append(
                GridLine(c,i,0,h,'v')
            )
    
    # fix the gridlines to still make sense when scrolling horizontally
    def update_scroll_horizontal(self,t,b,l,r, scrollSpeed, prevEdge, size):
        # remove offscreen vertical lines
        for i in range(len(self.vlines)-1,-1,-1):
            line = self.vlines[i]
            if line.coord > r or line.coord < l:
                line.remove()
                self.vlines.pop(i)
        
        # adjust horizontal lines to still be onscreen
        [line.fix(scrollSpeed) for line in self.hlines]

        # create new vertical lines
        if scrollSpeed < 0:
            for i in range(prevEdge - prevEdge%size, l, -size):
                self.vlines.append(
                    GridLine(self.c,i,t,b,'v')
                )
        else:
            for i in range(r - r%size, prevEdge, -size):
                self.vlines.append(
                    GridLine(self.c,i,t,b,'v')
                )
        
    # fix the gridlines to still make sense when scrolling vertically
    def update_scroll_vertical(self,t,b,l,r, scrollSpeed, prevEdge, size):
        # remove offscreen horizontal lines
        for i in range(len(self.hlines)-1,-1,-1):
            line = self.hlines[i]
            if line.coord > b or line.coord < t:
                line.remove()
                self.hlines.pop(i)
        
        # adjust vertical lines to still be onscreen
        [line.fix(scrollSpeed) for line in self.vlines]

        # create new horizontal lines
        if scrollSpeed < 0:
            for i in range(prevEdge - prevEdge%size, t, -size):
                self.hlines.append(
                    GridLine(self.c,i,l,r,'h')
                )
        else:
            for i in range(b - b%size, prevEdge, -size):
                self.hlines.append(
                    GridLine(self.c,i,l,r,'h')
                )

    
    def remove(self):
        [line.remove() for line in self.hlines]
        [line.remove() for line in self.vlines]
        self.hlines = []
        self.vlines = []