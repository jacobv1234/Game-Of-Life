from tkinter import *
from time import sleep
from pathlib import Path
from json import loads

from lib.rule import Rule

class RuleModifier:
    def __init__(self, master: Tk, rule: Rule):
        self.w = Toplevel(master)
        self.w.title('Rule Modification')
        self.w.protocol('WM_DELETE_WINDOW', self.cancel)
        self.load_presets()
        self.create_widgets()
        self.load_values_from_Rule(rule)
        self.output = -1    # result after clicking Apply or Cancel

    def load_presets(self):
        folder = Path('./assets/rules')
        ruleFileNames = [value.name for value in list(folder.glob('*.json'))]
        self.presets = dict()
        for filename in ruleFileNames:
            with open(f'./assets/rules/{filename}','r') as f:
                data = loads(f.read())
                self.presets[data['name']] = data
        self.presetOptions = tuple(self.presets.keys())

    def create_widgets(self):
        # title
        text = Label(self.w, text='Rule Modifier', font='Arial 20 bold')
        text.grid(row=0,column=0, padx=10, pady=5)

        # neighbour selector
        self.c = Canvas(self.w, width=150,height=150, bg='white')
        self.c.grid(row=3,rowspan=6,column=0)
        self.cSquares = [[
            self.c.create_rectangle(0,0,50,50,fill='', outline='black'),
            self.c.create_rectangle(50,0,100,50,fill='', outline='black'),
            self.c.create_rectangle(100,0,150,50,fill='', outline='black')
        ],
        [
            self.c.create_rectangle(0,50,50,100,fill='', outline='black'),
            self.c.create_rectangle(50,50,100,100,fill='', outline='black'),
            self.c.create_rectangle(100,50,150,100,fill='', outline='black')
        ],
        [
            self.c.create_rectangle(0,100,50,150,fill='', outline='black'),
            self.c.create_rectangle(50,100,100,150,fill='', outline='black'),
            self.c.create_rectangle(100,100,150,150,fill='', outline='black')
        ]]
        self.neighbours = [[0,0,0],[0,0,0],[0,0,0]]

        self.c.bind_all('<Button-1>', self.update_neighbours,add=True)

        text = Label(self.w, text='Neighbourhood', font='Arial 10')
        text.grid(row=2,column=0)

        # preset loading
        text = Label(self.w, text='Load Preset', font='Arial 10', anchor='se')
        text.grid(row=1,column=1,sticky=W)

        self.presetValue = StringVar(self.w)
        self.presetValue.set("Conway's Game of Life (default)")
        self.preset = OptionMenu(self.w,self.presetValue, *self.presetOptions)
        self.preset.grid(row=2,column=1, columnspan=2,sticky=E+W)
        self.preset.config(font='Arial 10')

        self.presetLoad = Button(self.w,font='Arial 10',text='Load',border=3,command=self.load_preset)
        self.presetLoad.grid(row=1,rowspan=2,column=3)

        # birth values
        text = Label(self.w, text='Birth values (comma separated)', font='Arial 10', anchor='se')
        text.grid(row=4,column=1,sticky=W)
        self.birthValues = Entry(self.w,font='Arial 10')
        self.birthValues.grid(row=5,column=1, columnspan=2,sticky=E+W)

        # survival values
        text = Label(self.w, text='Survival values (comma separated)', font='Arial 10', anchor='se')
        text.grid(row=6,column=1,sticky=W)
        self.survivalValues = Entry(self.w,font='Arial 10')
        self.survivalValues.grid(row=7,column=1, columnspan=2,sticky=E+W)

        # checkboxes
        self.wrapValue = StringVar(self.w)
        self.wrapCheckBox = Checkbutton(self.w,text='Wrap-around grid',font='Arial 10', 
                                        variable=self.wrapValue, onvalue='wrap',offvalue='fill')
        self.wrapCheckBox.grid(row=9, column=0)
        self.hexValue = BooleanVar(self.w)
        self.hexCheckBox = Checkbutton(self.w,text='Hexagonal grid',font='Arial 10',
                                       variable=self.hexValue, onvalue=True, offvalue=False)
        self.hexCheckBox.grid(row=9, column=1)

        # apply / cancel
        self.applyButton = Button(self.w,font='Arial 10',text='Apply',border=3,command=self.package_values_as_Rule)
        self.applyButton.grid(row=10,column=2, padx=5,pady=5)
        self.cancelButton = Button(self.w,font='Arial 10',text='Cancel',border=3, command=self.cancel)
        self.cancelButton.grid(row=10,column=3, padx=5,pady=5)
    
    def update_neighbours(self,event:Event):
        if event.widget != self.c:
            return
        x,y = event.x, event.y
        xi,yi = x//50, y//50

        # self.neighbours is updated upside down because of the convolution
        current_state = self.neighbours[xi][yi]
        if current_state == 0:
            self.neighbours[xi][yi] = 1
            self.c.itemconfig(self.cSquares[yi][xi], fill='#aaaaaa')
        else:
            self.neighbours[xi][yi] = 0
            self.c.itemconfig(self.cSquares[yi][xi], fill='')

    def load_values_from_Rule(self, rule: Rule):
        bstring = str(rule.b).strip('[]')
        self.birthValues.delete(0,'end')
        self.birthValues.insert(0, bstring)
        sstring = str(rule.s).strip('[]')
        self.survivalValues.delete(0,'end')
        self.survivalValues.insert(0, sstring)
        self.neighbours = rule.n
        for y in range(3):
            for x in range(3):
                if rule.n[x][y] == 0:
                    self.c.itemconfig(self.cSquares[y][x], fill='')
                else:
                    self.c.itemconfig(self.cSquares[y][x], fill='#aaaaaa')
        if rule.edge == 'wrap':
            self.wrapCheckBox.select()
        else:
            self.wrapCheckBox.deselect()
        if rule.hex:
            self.hexCheckBox.select()
        else:
            self.hexCheckBox.deselect()

    def load_preset(self):
        self.load_values_from_json(self.presets[self.presetValue.get()])

    def load_values_from_json(self, json: dict):
        bstring = str(json['born']).strip('[]')
        self.birthValues.delete(0,'end')
        self.birthValues.insert(0, bstring)
        sstring = str(json['survive']).strip('[]')
        self.survivalValues.delete(0,'end')
        self.survivalValues.insert(0, sstring)
        self.neighbours = json['neighbourhood']
        for y in range(3):
            for x in range(3):
                if json['neighbourhood'][x][y] == 0:
                    self.c.itemconfig(self.cSquares[x][y], fill='')
                else:
                    self.c.itemconfig(self.cSquares[x][y], fill='#aaaaaa')
        if json['edge'] == 'wrap':
            self.wrapCheckBox.select()
        else:
            self.wrapCheckBox.deselect()
        if json['hexagonal']:
            self.hexCheckBox.select()
        else:
            self.hexCheckBox.deselect()
    
    def package_values_as_Rule(self):
        b = [int(val) for val in self.birthValues.get().split(',')]
        s = [int(val) for val in self.survivalValues.get().split(',')]
        self.output = Rule(b,s,self.neighbours, self.wrapValue.get(), self.hexValue.get())

    def cancel(self):
        self.output = 'cancel'


# create an instance of RuleModifier and return the new rule
def getNewRule(window, rule):
    ruleWindow = RuleModifier(window, rule)
    while ruleWindow.output == -1:
        # force wraparound state to be on if hexagonal is on
        if ruleWindow.hexValue.get() == True:
            ruleWindow.wrapCheckBox.config(state='disabled')
            ruleWindow.wrapValue.set('wrap')
        else:
            ruleWindow.wrapCheckBox.config(state='normal')
        window.update()
        sleep(0.01)
    
    ruleWindow.w.destroy()

    if ruleWindow.output == 'cancel':
        return rule # do not change if cancelled
    return ruleWindow.output