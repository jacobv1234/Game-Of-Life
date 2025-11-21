from tkinter import *
from lib.gridline import GridLine

class GridLines:
    def __init__(self, c: Canvas, l,r,t,b, size:int = 20):
        self.c = c
        self.hlines = []
        self.vlines = []

        # draw every 5th gridline if too dense
        if size <= 10:
            size *= 5
        
        # next / last mutiples of sides
        lm = l-l%size
        rm = r-r%size+size
        tm = t-t%size
        bm = b-b%size+size

        for i in range(tm, bm, size):
            self.hlines.append(
                GridLine(c,i,lm,rm,'h')
            )

        for i in range(l-l%size, r-r%size+size, size):
            self.vlines.append(
                GridLine(c,i,tm,bm,'v')
            )
    
    # fix the gridlines to still make sense when scrolling horizontally
    def update_scroll_horizontal(self,t,b,l,r, scrollSpeed, prevEdge, size):
        # draw every 5th gridline if too dense
        if size <= 10:
            size *= 5
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
        # draw every 5th gridline if too dense
        if size <= 10:
            size *= 5
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