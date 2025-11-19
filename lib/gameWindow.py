from tkinter import *
from tkinter import PhotoImage
from tkinter import messagebox

from lib.gridlines import GridLines
from lib.grid import Grid

class GameWindow:
    def __init__(self, grid: Grid):
        self.grid = grid # get a pointer to the grid
        self.running = True
        self.dragState = 0
        self.mouseOnButton = False
        self.simulationOn = False


        self.w = Tk()
        
        self.w.protocol("WM_DELETE_WINDOW", self.close_program)

        self.w.title('Game of Life')

        self.width = self.w.winfo_screenwidth() - 10
        self.height = self.w.winfo_screenheight() - 75

        self.w.state('zoomed')
        self.c = Canvas(self.w, width = self.width, height = self.height,
                        xscrollincrement = 1, yscrollincrement = 1,
                        bg = 'white')
        self.c.place(x=0,y=0,anchor='nw')

        # load images
        self.images = {
            'play': PhotoImage(file='images/play.png'),
            'pause': PhotoImage(file='images/pause.png'),
            'delete': PhotoImage(file='images/delete.png')
        }


        # visible area tracking
        self.t = 0
        self.b = self.height
        self.l = 0
        self.r = self.width
        self.cellSize = 20
        self.scrollSpeed = 30

        # gridlines
        self.gridlines = GridLines(self.c, self.width, self.height, self.cellSize)

        # cells
        self.cells = []

        # mouse cursor tracking
        self.cursor = self.c.create_rectangle(0,0,self.cellSize,self.cellSize, fill='', outline="#0000bd")
        self.curx = 0
        self.cury = 0

        # bind controls
        self.c.bind_all('<Motion>', self.move_cursor)
        self.c.bind_all('<Button-1>', self.toggle_cell)
        self.c.bind_all('<B1-Motion>', self.drag_draw)
        self.c.bind_all('<Up>', self.scroll_screen)
        self.c.bind_all('<Down>', self.scroll_screen)
        self.c.bind_all('<Left>', self.scroll_screen)
        self.c.bind_all('<Right>', self.scroll_screen)


        # buttons
        self.playButton = Button(self.w,border=5, command=self.toggle_play, image=self.images['play'])
        self.playButton.place(width=70, height=70, relx=0, rely=1, anchor='sw')
        self.clearButton = Button(self.w, border=3, command=self.clear_screen, image=self.images['delete'])
        self.clearButton.place(width=40, height=40, x=67, y=self.height-24, anchor='sw')

        # generation counter
        self.genCountC = Canvas(self.w, bg='black')
        self.genCountC.place(x=70,y=self.height, width = 160, height=30, anchor='sw')
        self.genCountC.create_rectangle(0,3,157,30,fill='#f0f0f0', outline='')
        self.genText = self.genCountC.create_text(10,10,fill='black', font='Arial 10', text='Generation: 0', anchor='nw')

    # move highlighted square
    def move_cursor(self, event: Event):
        sx, sy = event.x, event.y

        # check mouse is not hovering on a button
        if event.widget in [self.playButton, self.genCountC, self.clearButton]:
            # move blue cursor offscreen and shrink it
            self.mouseOnButton = True
            self.c.coords(-10,-10,-10,-10)
            return
        
        x, y = self.c.canvasx(sx), self.c.canvasy(sy)
        # truncate to find cell
        self.curx = (x // self.cellSize) * self.cellSize
        self.cury = (y // self.cellSize) * self.cellSize
        # move cursor
        self.c.coords(self.cursor, self.curx, self.cury, self.curx+self.cellSize, self.cury+self.cellSize)
        self.mouseOnButton = False

    
    # click to draw
    def toggle_cell(self,event):
        sx, sy = event.x, event.y

        # check mouse is not hovering on a button
        if self.mouseOnButton:
            return

        x, y = self.c.canvasx(sx), self.c.canvasy(sy)
        xi = int(x // self.cellSize)
        yi = int(y // self.cellSize)
        self.dragState = self.grid.toggle(xi,yi)
    
    # click and drag to draw
    def drag_draw(self,event):
        sx, sy = event.x, event.y

        # check mouse is not hovering on a button
        if self.mouseOnButton:
            return
        
        x, y = self.c.canvasx(sx), self.c.canvasy(sy)
        xi = int(x // self.cellSize)
        yi = int(y // self.cellSize)
        self.grid.set(xi,yi,self.dragState)
    

    # play / pause button clicked
    def toggle_play(self):
        if self.simulationOn:
            self.simulationOn = False
            self.playButton.config(image = self.images['play'])
        else:
            self.simulationOn = True
            self.playButton.config(image = self.images['pause'])
    
    # clear button clicked
    def clear_screen(self):
        clear = messagebox.askokcancel('Clear screen', 'Are you sure you want to clear the screen?')
        if clear:
            self.grid.reset()
    
    # scroll the screen when arrow keys are pressed
    def scroll_screen(self, event: Event):
        match event.keysym:
            case 'Up':
                self.c.yview_scroll(-self.scrollSpeed,'units')
                prevEdge = self.t
                self.t -= self.scrollSpeed
                self.b -= self.scrollSpeed
                self.gridlines.update_scroll_vertical(self.t,self.b,self.l,self.r,
                                                        -self.scrollSpeed, prevEdge, self.cellSize)
                self.c.tag_raise(self.cursor)

            case 'Down':
                self.c.yview_scroll(self.scrollSpeed,'units')
                prevEdge = self.b
                self.t += self.scrollSpeed
                self.b += self.scrollSpeed
                self.gridlines.update_scroll_vertical(self.t,self.b,self.l,self.r,
                                                        self.scrollSpeed, prevEdge, self.cellSize)
                self.c.tag_raise(self.cursor)
                

            case 'Left':
                self.c.xview_scroll(-self.scrollSpeed,'units')
                prevEdge = self.l
                self.l -= self.scrollSpeed
                self.r -= self.scrollSpeed
                self.gridlines.update_scroll_horizontal(self.t,self.b,self.l,self.r,
                                                        -self.scrollSpeed, prevEdge, self.cellSize)
                self.c.tag_raise(self.cursor)

            case 'Right':
                self.c.xview_scroll(self.scrollSpeed,'units')
                prevEdge = self.r
                self.l += self.scrollSpeed
                self.r += self.scrollSpeed
                self.gridlines.update_scroll_horizontal(self.t,self.b,self.l,self.r,
                                                        self.scrollSpeed, prevEdge, self.cellSize)
                self.c.tag_raise(self.cursor)
    

    
    def close_program(self):
        self.running = False

    
    def update(self):
        # remove non-static features from last frame (cells)
        for cell in self.cells:
            self.c.delete(cell)
        
        # update generation counter
        self.genCountC.itemconfig(self.genText, text=f'Generation: {self.grid.gens}')

        # draw cells
        # only in visible range
        lGrid = self.l - self.l%self.cellSize
        rGrid = self.r - self.r%self.cellSize + self.cellSize
        tGrid = self.t - self.t%self.cellSize
        bGrid = self.b - self.b%self.cellSize + self.cellSize

        for x in range(lGrid, rGrid, self.cellSize):
            for y in range(tGrid, bGrid, self.cellSize):
                xi = int(x // self.cellSize)
                yi = int(y // self.cellSize)
                if self.grid.grid[xi][yi] == 1:
                    self.cells.append(
                        self.c.create_rectangle(x,y, x+self.cellSize, y+self.cellSize, fill='black')
                    )

        self.w.update()