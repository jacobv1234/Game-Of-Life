from tkinter import *

class ViewFinder:
    def __init__(self, window, screenLimit,l,r,t,b):
        self.c = Canvas(window, width=150, height=150, bg='black')
        self.c.place(relx=1,rely=1,width=150,height=150,anchor='se')
        self.c.create_rectangle(2,2,148,148,fill='white')
        self.screen = self.c.create_rectangle(0,0,1,1,fill='',outline='blue')
        self.update(screenLimit,l,r,t,b)
    
    def update(self,sL,l,r,t,b):
        x1 = (l/(sL*2)) * 150 +75
        y1 = (t/(sL*2)) * 150 +75
        x2 = (r/(sL*2)) * 150 +75
        y2 = (b/(sL*2)) * 150 +75
        self.c.coords(self.screen,x1,y1,x2,y2)