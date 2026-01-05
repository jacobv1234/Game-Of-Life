from tkinter import *
from lib.hexgridcell import HexGridCell

class HexGrid:
    def __init__(self, c: Canvas, l,r,t,b, size: int=20):
        self.c = c
        self.cells = []
        
        # next / last mutiples of sides
        lm = l-l%size
        rm = r-r%size+size
        tm = t-t%size
        bm = b-b%size+size

        for x1 in range(lm,rm,size):
            if (x1/size)%2 == 0:
                self.cells.extend([
                    HexGridCell(c,x1,y1,x1+size,y1+size)
                    for y1 in range(tm,bm,size)
                ])
            else:
                self.cells.extend([
                    HexGridCell(c,x1,y1,x1+size,y1+size)
                    for y1 in range(int(tm-size//2),int(bm+size//2),size)
                ])
    
    def update_scroll_horizontal(self,t,b,l,r, scrollSpeed, prevEdge, size):
        for i in range(len(self.cells)-1,-1,-1):
            cell = self.cells[i]
            if cell.x > r or cell.x < l:
                cell.remove()
                self.cells.pop(i)

        tm = t-t%size
        bm = b-b%size+size

        if scrollSpeed < 0:
            for x1 in range(prevEdge - prevEdge%size, l, -size):
                if (x1/size)%2 == 0:
                    self.cells.extend([
                        HexGridCell(self.c,x1,y1,x1+size,y1+size)
                        for y1 in range(tm,bm,size)
                    ])
                else:
                    self.cells.extend([
                        HexGridCell(self.c,x1,y1,x1+size,y1+size)
                        for y1 in range(int(tm-size//2),int(bm+size//2),size)
                    ])
        else:
            for x1 in range(r - r%size, prevEdge, -size):
                if (x1/size)%2 == 0:
                    self.cells.extend([
                        HexGridCell(self.c,x1,y1,x1+size,y1+size)
                        for y1 in range(tm,bm,size)
                    ])
                else:
                    self.cells.extend([
                        HexGridCell(self.c,x1,y1,x1+size,y1+size)
                        for y1 in range(int(tm-size//2),int(bm+size//2),size)
                    ])
    
    def update_scroll_vertical(self,t,b,l,r, scrollSpeed, prevEdge, size):
        for i in range(len(self.cells)-1,-1,-1):
            cell = self.cells[i]
            if cell.y > b or cell.y < t:
                cell.remove()
                self.cells.pop(i)

        lm = l-l%size
        rm = r-r%size+size

        if scrollSpeed < 0:
            for x1 in range(lm,rm,size):
                if (x1/size)%2 == 0:
                    self.cells.extend([
                        HexGridCell(self.c,x1,y1,x1+size,y1+size)
                        for y1 in range(prevEdge - prevEdge%size, t, -size)
                    ])
                else:
                    self.cells.extend([
                        HexGridCell(self.c,x1,y1,x1+size,y1+size)
                        for y1 in range(prevEdge - prevEdge%size + int(size//2), int(t-size//2), -size)
                    ])
        else:
            for x1 in range(lm,rm,size):
                if (x1/size)%2 == 0:
                    self.cells.extend([
                        HexGridCell(self.c,x1,y1,x1+size,y1+size)
                        for y1 in range(b - b%size, prevEdge, -size)
                    ])
                else:
                    self.cells.extend([
                        HexGridCell(self.c,x1,y1,x1+size,y1+size)
                        for y1 in range(b - b%size + int(size//2), prevEdge - int(size//2), -size)
                    ])

    def remove(self):
        [cell.remove() for cell in self.cells]
        self.cells = []