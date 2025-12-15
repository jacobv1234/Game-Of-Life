from tkinter import *

from lib.rule import Rule

class RuleModifier:
    def __init__(self, master: Tk, rule: Rule):
        self.w = Toplevel(master)
        self.w.title('Rule Modification')

        text = Label(self.w, text='Rule Modifier', font='Arial 20 bold')
        text.grid(row=0,column=0, padx=10, pady=5)
        c = Canvas(self.w, width=150,height=150, bg='white')
        c.grid(row=3,rowspan=6,column=0)
        text = Label(self.w, text='Neighbourhood', font='Arial 10')
        text.grid(row=2,column=0)
        text = Label(self.w, text='Load Preset', font='Arial 10', anchor='se')
        text.grid(row=1,column=1,sticky=W)
        entry = Entry(self.w,font='Arial 10')
        entry.grid(row=2,column=1, columnspan=2,sticky=E+W)
        button = Button(self.w,font='Arial 10',text='Load',border=3)
        button.grid(row=1,rowspan=2,column=3)
        text = Label(self.w, text='Birth values (comma separated)', font='Arial 10', anchor='se')
        text.grid(row=4,column=1,sticky=W)
        entry = Entry(self.w,font='Arial 10')
        entry.grid(row=5,column=1, columnspan=2,sticky=E+W)
        text = Label(self.w, text='Survival values (comma separated)', font='Arial 10', anchor='se')
        text.grid(row=6,column=1,sticky=W)
        entry = Entry(self.w,font='Arial 10')
        entry.grid(row=7,column=1, columnspan=2,sticky=E+W)
        checkbox = Checkbutton(self.w,text='Wrap-around grid',font='Arial 10',compound='left')
        checkbox.grid(row=9, column=0)
        checkbox = Checkbutton(self.w,text='Hexagonal grid',font='Arial 10')
        checkbox.grid(row=9, column=1)
        button = Button(self.w,font='Arial 10',text='Apply',border=3)
        button.grid(row=10,column=2, padx=5,pady=5)
        button = Button(self.w,font='Arial 10',text='Cancel',border=3)
        button.grid(row=10,column=3, padx=5,pady=5)


# create an instance of RuleModifier and return the new rule
def getNewRule(window, rule):
    ruleWindow = RuleModifier(window, rule)