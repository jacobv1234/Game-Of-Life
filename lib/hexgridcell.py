from tkinter import *

class HexGridCell:
    def __init__(self, c: Canvas, x1,y1,x2,y2):
        self.c = c
        self.x = (x1+x2)/2
        self.y = (y1+y2)/2
        self.shape = c.create_rectangle(x1,y1,x2,y2,fill='',outline='#999999')
    
    def remove(self):
        self.c.delete(self.shape)