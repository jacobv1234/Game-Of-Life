from tkinter import *

class HexGridCell:
    def __init__(self, c: Canvas, x1,y1,x2,y2):
        self.c = c
        self.x = (x1+x2)/2
        self.y = (y1+y2)/2
        #self.shape = c.create_rectangle(x1,y1,x2,y2,fill='',outline='#999999')
        h = (x2-x1)/6
        self.shape = c.create_polygon(
            x1+h,y1,
            x2-h,y1,
            x2+h,self.y,
            x2-h,y2,
            x1+h,y2,
            x1-h,self.y,
            fill='', outline='#999999'
        )
    
    def remove(self):
        self.c.delete(self.shape)