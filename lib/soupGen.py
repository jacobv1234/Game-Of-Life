from tkinter import *
from time import sleep

class SoupGenerator:
    def __init__(self, master: Tk):
        self.w = Toplevel(master)
        self.w.title('Seeder')
        self.w.protocol('WM_DELETE_WINDOW', self.cancel)
        self.create_widgets()
        self.output = -1    # result after clicking Apply or Cancel
    
    def create_widgets(self):
        text = Label(self.w,text='Generate Random Seed', font='Arial 15 bold')
        text.grid(row=0,column=0,columnspan=2,padx=10,pady=5)
        text = Label(self.w,text='Shape:',font='Arial 10')
        text.grid(row=1,column=0)
        text = Label(self.w,text='Radius:',font='Arial 10')
        text.grid(row=2,column=0)
        text = Label(self.w,text='Density:',font='Arial 10')
        text.grid(row=3,column=0)

        self.shapeOptions = ('Circle','Square','Hexagon')
        self.shape = StringVar(self.w)
        self.shape.set('Square')
        self.shapeMenu = OptionMenu(self.w,self.shape,*self.shapeOptions)
        self.shapeMenu.grid(row=1,column=1,sticky=E+W,pady=5)
        self.shapeMenu.config(font='Arial 10')

        self.radius = Entry(self.w,font='Arial 10')
        self.radius.grid(row=2,column=1,sticky=E+W,pady=5)
        self.density = Entry(self.w,font='Arial 10')
        self.density.grid(row=3,column=1,sticky=E+W,pady=5)

        self.generateButton = Button(self.w,font='Arial 10',text='Generate',border=3, command=self.generate)
        self.generateButton.grid(row=4,column=0,columnspan=2,padx=10,sticky=E+W,pady=5)
        self.cancelButton = Button(self.w,font='Arial 10',text='Cancel',border=3,command=self.cancel)
        self.cancelButton.grid(row=5,column=0,columnspan=2,padx=10,sticky=E+W,pady=5)
    
    def cancel(self):
        self.output = 'cancel'
    
    def generate(self):
        shape = self.shape.get()
        radius = self.radius.get()
        density = self.density.get()
        self.output = (shape,radius,density)

def getSoupParams(window):
    soupUI = SoupGenerator(window)
    while soupUI.output == -1:
        window.update()
        sleep(0.01)
    
    soupUI.w.destroy()

    if soupUI.output == 'cancel':
        return 'cancel',-1,-1
    else:
        return soupUI.output