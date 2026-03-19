from tkinter import *
from time import sleep

class QSimWindow:
    def __init__(self, master: Tk):
        self.w = Toplevel(master)
        self.w.title('Quick Sim Setup')
        self.w.protocol('WM_DELETE_WINDOW', self.cancel)
        self.create_widgets()
        self.output = -1    # result after clicking Apply or Cancel
    
    def create_widgets(self):
        text = Label(self.w, text = 'Simulation cutoff:', font='Arial 10')
        text.grid(row=0, column=0, padx=20,pady=10,sticky=E)
        self.cutoff = Entry(self.w, font='Arial 10')
        self.cutoff.grid(row=0, column=1, columnspan=2, padx=20,pady=10,sticky=E+W)
        self.acceptButton = Button(self.w, font='Arial 10', text='Begin', border = 3, command = self.accept, anchor='e')
        self.acceptButton.grid(row=1,column=0,padx=20, pady=10, sticky=E)
        self.cancelButton = Button(self.w, font='Arial 10', text='Cancel', border = 3, command = self.cancel, anchor='center')
        self.cancelButton.grid(row=1,column=1,padx=20, pady=10, sticky=W)
        self.multipleButton = Button(self.w, font='Arial 10', text='Multiple Simulations', border = 3, command = self.multiple, anchor='w')
        self.multipleButton.grid(row=1,column=2,padx=20, pady=10, sticky=E)
    
    def accept(self):
        self.output = self.cutoff.get()
    def multiple(self):
        self.output = 'multiple'
    def cancel(self):
        self.output = 'cancel'

def getQSimCutoff(window):
    UI = QSimWindow(window)
    while UI.output == -1:
        window.update()
        sleep(0.01)
    
    UI.w.destroy()

    return UI.output