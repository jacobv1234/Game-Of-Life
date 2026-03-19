from tkinter import *
from time import sleep

class MSimWindow:
    def __init__(self, master: Tk):
        self.w = Toplevel(master)
        self.w.title('Quick Sim Setup')
        self.w.protocol('WM_DELETE_WINDOW', self.cancel)
        self.create_widgets()
        self.output = -1    # result after clicking Apply or Cancel
    
    def create_widgets(self):
        text = Label(self.w, text='Simulate Multiple Games', font = 'Arial 25 bold')
        text.grid(row = 0, column = 0, columnspan = 3, sticky = E+W)

        text = Label(self.w, text='Soup setup', font='Arial 18 bold')
        text.grid(row=1, column=0, columnspan=2, sticky = E+W)

        text = Label(self.w, text='Shape', font='Arial 10')
        text.grid(row=2, column=0, sticky = E+W)
        self.shapeOptions = ('Circle','Square','Hexagon')
        self.shape = StringVar(self.w)
        self.shape.set('Square')
        self.shapeMenu = OptionMenu(self.w,self.shape,*self.shapeOptions)
        self.shapeMenu.grid(row=2,column=1,columnspan=2,sticky=E+W, pady=5, padx=10)
        self.shapeMenu.config(font='Arial 10')

        text = Label(self.w, text='Radius', font='Arial 10')
        text.grid(row=3,column=0, sticky=E+W)
        self.radius = Entry(self.w,font='Arial 10')
        self.radius.grid(row=3,column=1,columnspan=2,sticky=E+W,pady=5,padx=10)

        text = Label(self.w, text='Density', font='Arial 10')
        text.grid(row=4,column=0, sticky=E+W)
        self.density = Entry(self.w,font='Arial 10')
        self.density.grid(row=4,column=1,columnspan=2,sticky=E+W,pady=5,padx=10)

        text = Label(self.w, text='Simulation setup', font='Arial 18 bold')
        text.grid(row=5, column=0, columnspan=2, sticky = E+W)

        text = Label(self.w, text='Games', font='Arial 10')
        text.grid(row=6,column=0, sticky=E+W)
        self.games = Entry(self.w,font='Arial 10')
        self.games.grid(row=6,column=1,columnspan=2,sticky=E+W,pady=5,padx=10)

        text = Label(self.w, text='Generation cutoff', font='Arial 10')
        text.grid(row=7,column=0, sticky=E+W)
        self.cutoff = Entry(self.w,font='Arial 10')
        self.cutoff.grid(row=7,column=1,columnspan=2,sticky=E+W,pady=5,padx=10)

        self.beginButton = Button(self.w, font='Arial 10', text='Begin', border = 3, command = self.begin, anchor='e')
        self.beginButton.grid(row=8,column=1,padx=20, pady=10, sticky=E)
        self.cancelButton = Button(self.w, font='Arial 10', text='Cancel', border = 3, command = self.cancel, anchor='w')
        self.cancelButton.grid(row=8,column=2,padx=20, pady=10, sticky=W)


    def cancel(self):
        self.output = 'cancel'
    
    def begin(self):
        self.output = {
            'shape': self.shape.get(),
            'radius': self.radius.get(),
            'density': self.density.get(),
            'games': self.games.get(),
            'cutoff': self.cutoff.get()
        }

def getMSimSettings(window):
    UI = MSimWindow(window)
    while UI.output == -1:
        window.update()
        sleep(0.01)
    
    UI.w.destroy()

    return UI.output