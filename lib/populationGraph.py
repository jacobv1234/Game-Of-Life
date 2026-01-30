from tkinter import *
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk

# custom matplotlib toolbar with the configure subplots button removed
class NoConfigToolbar(NavigationToolbar2Tk):
    toolitems = tuple([tool for tool in NavigationToolbar2Tk.toolitems if tool[0] in
                       ['Home', 'Pan', 'Zoom', None, 'Save']])

class PopulationGraph:
    def __init__(self, master: Tk, history: list[int]):
        self.running = True

        self.w = Toplevel(master)

        self.w.protocol("WM_DELETE_WINDOW", self.close)

        # create figure
        self.fig = Figure()
        self.plot = self.fig.add_subplot(xlabel='Generation', ylabel='Population', title='Population History')

        # add history to graph
        self.plot.plot(history)

        # tkinter graph canvas object
        self.c = FigureCanvasTkAgg(self.fig, self.w)
        self.c.draw()
        self.c.get_tk_widget().pack()

        # toolbar
        self.toolbar = NoConfigToolbar(self.c,self.w)
        self.toolbar.update()
        self.c.get_tk_widget().pack()

    def close(self):
        self.running = False
        self.w.destroy()