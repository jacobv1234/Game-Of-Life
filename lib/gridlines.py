from tkinter import *

class GridLines:
    def __init__(self, c: Canvas, w:int, h:int):
        self.c = c
        self.hlines = []
        self.vlines = []

        for i in range(0, h, 20):
            self.hlines.append(
                c.create_line(0,i,w,i,fill='#999999')
            )

        for i in range(0, w, 20):
            self.vlines.append(
                c.create_line(i,0,i,h,fill='#999999')
            )
    
    def remove(self):
        [self.c.delete(line) for line in self.hlines]
        [self.c.delete(line) for line in self.vlines]
        self.hlines = []
        self.vlines = []