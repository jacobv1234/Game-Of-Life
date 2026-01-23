from tkinter import *
from tkinter import PhotoImage
from tkinter import messagebox

from lib.gridlines import GridLines
from lib.hexgrid import HexGrid
from lib.gridGPU import Grid
from lib.viewfinder import ViewFinder
from lib.ruleModifier import getNewRule

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
            'delete': PhotoImage(file='images/delete.png'),
            'zoomIn': PhotoImage(file='images/zoomIn.png'),
            'zoomOut': PhotoImage(file='images/zoomOut.png'),
            'gear': PhotoImage(file='images/gear.png'),
            'next': PhotoImage(file='images/next.png')
        }


        # visible area tracking
        self.t = 0
        self.b = self.height
        self.l = 0
        self.r = self.width
        self.cellSize = 20
        self.scrollSpeed = 30
        self.screenLimit = (self.grid.gridsize // 2) * self.cellSize
        self.scLimitBox = self.c.create_rectangle(-self.screenLimit+2, -self.screenLimit+2,
                                                  self.screenLimit-2,self.screenLimit-2,
                                                  fill='',outline='red')
        self.zoomLevels = [5,10,15,20,30,40]
        self.viewFinder = ViewFinder(self.w,self.screenLimit,self.l,self.r,self.t,self.b)

        # gridlines
        self.gridlines = GridLines(self.c, self.l,self.r,self.t,self.b, self.cellSize)

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
        self.playButton = Button(self.w, border=5, command=self.toggle_play, image=self.images['play'])
        self.playButton.place(width=70, height=70, relx=0, rely=1, anchor='sw')
        self.nextButton = Button(self.w, border=3, command=self.grid.next, image=self.images['next'])
        self.nextButton.place(width=40, height=40, x=67, y=self.height-24, anchor='sw')
        self.clearButton = Button(self.w, border=3, command=self.clear_screen, image=self.images['delete'])
        self.clearButton.place(width=40, height=40, x=107, y=self.height-24, anchor='sw')
        self.ruleButton = Button(self.w, border=3, command=self.change_rules, image=self.images['gear'])
        self.ruleButton.place(width=40, height=40, x=147, y=self.height-24, anchor='sw')
        self.zoomOutButton = Button(self.w, border=5, command=self.zoomOut, image=self.images['zoomOut'])
        self.zoomOutButton.place(x=self.width-140,y=self.height+4,width=40,height=40,anchor='se')
        self.zoomInButton = Button(self.w, border=5, command=self.zoomIn, image=self.images['zoomIn'])
        self.zoomInButton.place(x=self.width-140,y=self.height-36,width=40,height=40,anchor='se')

        # generation counter
        self.genCountC = Canvas(self.w, bg='black')
        self.genCountC.place(x=70,y=self.height+4, width = 230, height=30, anchor='sw')
        self.genCountC.create_rectangle(0,3,227,30,fill='#f0f0f0', outline='')
        self.genText = self.genCountC.create_text(10,10,fill='black', font='Arial 10', text='Generation: 0', anchor='nw')
        self.popText = self.genCountC.create_text(120,10,fill='black', font='Arial 10', text='Population: 0', anchor='nw')

    # move highlighted square
    def move_cursor(self, event: Event):
        sx, sy = event.x, event.y

        # check mouse is on main grid
        if event.widget != self.c:
            # hide cursor
            self.mouseOnButton = True
            self.c.itemconfig(self.cursor, state='hidden')
            return
        
        self.c.itemconfig(self.cursor, state='normal')
        x, y = self.c.canvasx(sx), self.c.canvasy(sy)
        # skip if offscreen
        if x < -self.screenLimit or x >= self.screenLimit or y < -self.screenLimit or y >= self.screenLimit:
                    return
        
        # truncate to find cell
        if self.grid.rule.hex == True:
            self.curx = (x // self.cellSize) * self.cellSize
            if self.curx / self.cellSize % 2 == 1:
                self.cury = ((y - (self.cellSize//2)) // self.cellSize + 0.5) * self.cellSize
            else:
                self.cury = (y // self.cellSize) * self.cellSize
        else:
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
        # skip if offscreen
        if x < -self.screenLimit or x >= self.screenLimit or y < -self.screenLimit or y >= self.screenLimit:
                    return
        if self.grid.rule.hex == True:
            xo, yo = x + self.screenLimit, (y + self.screenLimit + (x-x%self.cellSize)//2)
        else:
            xo, yo = x + self.screenLimit, y + self.screenLimit
        xi = int(xo // self.cellSize) % self.grid.gridsize
        yi = int(yo // self.cellSize) % self.grid.gridsize
        self.dragState = self.grid.toggle(xi,yi)
    
    # click and drag to draw
    def drag_draw(self,event):
        sx, sy = event.x, event.y

        # check mouse is not hovering on a button
        if self.mouseOnButton:
            return
        
        x, y = self.c.canvasx(sx), self.c.canvasy(sy)
        if self.grid.rule.hex == True:
            xo, yo = x + self.screenLimit, (y + self.screenLimit + (x-x%self.cellSize)//2)
        else:
            xo, yo = x + self.screenLimit, y + self.screenLimit
        xi = int(xo // self.cellSize) % self.grid.gridsize
        yi = int(yo // self.cellSize) % self.grid.gridsize
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
            self.simulationOn = False
            self.playButton.config(image = self.images['play'])
        return clear
    
    # rule modification button pressed
    def change_rules(self):
        screen_cleared = self.clear_screen()
        if screen_cleared == False:
            return
        self.update()
        rule = getNewRule(self.w, self.grid.rule)
        self.grid.changeRule(rule) #type:ignore
        self.gridlines.remove()
        if self.grid.rule.hex == True:
            self.gridlines = HexGrid(self.c,self.l,self.r,self.t,self.b,self.cellSize)
        else:    
            self.gridlines = GridLines(self.c,self.l,self.r,self.t,self.b,self.cellSize)

    
    # scroll the screen when arrow keys are pressed
    def scroll_screen(self, event: Event):
        match event.keysym:
            case 'Up':
                prevEdge = self.t
                self.t -= self.scrollSpeed
                self.b -= self.scrollSpeed

                # check if moved offscreen
                scrolloffset = 0
                if self.t < -self.screenLimit:
                    scrolloffset = -self.screenLimit - self.t
                    self.t += scrolloffset
                    self.b += scrolloffset

                self.gridlines.update_scroll_vertical(self.t,self.b,self.l,self.r,
                                                        -self.scrollSpeed + scrolloffset, prevEdge, self.cellSize)
                self.c.yview_scroll(int(-self.scrollSpeed + scrolloffset),'units')

            case 'Down':
                prevEdge = self.b
                self.t += self.scrollSpeed
                self.b += self.scrollSpeed

                # check if moved offscreen
                scrolloffset = 0
                if self.b > self.screenLimit:
                    scrolloffset = self.screenLimit - self.b
                    self.t += scrolloffset
                    self.b += scrolloffset

                self.gridlines.update_scroll_vertical(self.t,self.b,self.l,self.r,
                                                        self.scrollSpeed + scrolloffset, prevEdge, self.cellSize)
                self.c.yview_scroll(int(self.scrollSpeed + scrolloffset),'units')
                

            case 'Left':
                prevEdge = self.l
                self.l -= self.scrollSpeed
                self.r -= self.scrollSpeed

                # check if moved offscreen
                scrolloffset = 0
                if self.l < -self.screenLimit:
                    scrolloffset = -self.screenLimit - self.l
                    self.l += scrolloffset
                    self.r += scrolloffset

                self.gridlines.update_scroll_horizontal(self.t,self.b,self.l,self.r,
                                                        -self.scrollSpeed + scrolloffset, prevEdge, self.cellSize)
                self.c.xview_scroll(int(-self.scrollSpeed + scrolloffset),'units')

            case 'Right':
                prevEdge = self.r
                self.l += self.scrollSpeed
                self.r += self.scrollSpeed

                # check if moved offscreen
                scrolloffset = 0
                if self.r > self.screenLimit:
                    scrolloffset = self.screenLimit - self.r
                    self.l += scrolloffset
                    self.r += scrolloffset

                self.gridlines.update_scroll_horizontal(self.t,self.b,self.l,self.r,
                                                        self.scrollSpeed + scrolloffset, prevEdge, self.cellSize)
                self.c.xview_scroll(int(self.scrollSpeed + scrolloffset),'units')
        
        self.viewFinder.update(self.screenLimit, self.l,self.r,self.t,self.b)
    

    def zoomIn(self):
        # get new zoom values
        zoomIndex = self.zoomLevels.index(self.cellSize)
        zoomIndex += 1
        if zoomIndex >= len(self.zoomLevels):
            return
        newZoom = self.zoomLevels[zoomIndex]
        zMult = newZoom / self.cellSize

        # adjust screen edges
        oldxc = (self.r + self.l)/2
        oldyc = (self.b + self.t)/2
        xc = oldxc*zMult
        yc = oldyc*zMult
        self.l = int(xc - self.width/2)
        self.r = int(xc + self.width/2)
        self.t = int(yc - self.height/2)
        self.b = int(yc + self.height/2)

        # physically move the screen
        self.c.xview_scroll(int(xc-oldxc),'units')
        self.c.yview_scroll(int(yc-oldyc),'units')

        # recreate the grid
        self.gridlines.remove()
        if self.grid.rule.hex == True:
            self.gridlines = HexGrid(self.c,self.l,self.r,self.t,self.b,newZoom)
        else:    
            self.gridlines = GridLines(self.c,self.l,self.r,self.t,self.b,newZoom)

        # update self parameters
        self.cellSize = newZoom
        self.screenLimit = (self.grid.gridsize // 2) * self.cellSize
        self.c.delete(self.scLimitBox)
        self.scLimitBox = self.c.create_rectangle(-self.screenLimit+2, -self.screenLimit+2,
                                                  self.screenLimit-2,self.screenLimit-2,
                                                  fill='',outline='red')
        
        self.viewFinder.update(self.screenLimit, self.l,self.r,self.t,self.b)
    

    def zoomOut(self):
        # get new zoom values
        zoomIndex = self.zoomLevels.index(self.cellSize)
        zoomIndex -= 1
        if zoomIndex < 0:
            return
        newZoom = self.zoomLevels[zoomIndex]
        zMult = newZoom / self.cellSize

        # adjust screen edges
        oldxc = (self.r + self.l)/2
        oldyc = (self.b + self.t)/2
        xc = oldxc*zMult
        yc = oldyc*zMult
        self.l = int(xc - self.width/2)
        self.r = int(xc + self.width/2)
        self.t = int(yc - self.height/2)
        self.b = int(yc + self.height/2)

        # physically move the screen
        self.c.xview_scroll(int(xc-oldxc),'units')
        self.c.yview_scroll(int(yc-oldyc),'units')

        # recreate the grid
        self.gridlines.remove()
        if self.grid.rule.hex == True:
            self.gridlines = HexGrid(self.c,self.l,self.r,self.t,self.b,newZoom)
        else:    
            self.gridlines = GridLines(self.c,self.l,self.r,self.t,self.b,newZoom)

        # update self parameters
        self.cellSize = newZoom
        self.screenLimit = (self.grid.gridsize // 2) * self.cellSize
        self.c.delete(self.scLimitBox)
        self.scLimitBox = self.c.create_rectangle(-self.screenLimit+2, -self.screenLimit+2,
                                                  self.screenLimit-2,self.screenLimit-2,
                                                  fill='',outline='red')
        
        self.viewFinder.update(self.screenLimit, self.l,self.r,self.t,self.b)

    
    def close_program(self):
        self.running = False

    
    def update(self):
        # remove non-static features from last frame (cells)
        for cell in self.cells:
            self.c.delete(cell)
        
        # update generation counter
        self.genCountC.itemconfig(self.genText, text=f'Generation: {self.grid.gens}')
        self.genCountC.itemconfig(self.popText, text=f'Population: {self.grid.population}')

        # draw cells
        # only in visible range
        lGrid = self.l - self.l%self.cellSize
        rGrid = self.r - self.r%self.cellSize + self.cellSize
        tGrid = self.t - self.t%self.cellSize
        bGrid = self.b - self.b%self.cellSize + self.cellSize

        for x in range(lGrid, rGrid, self.cellSize):
            for y in range(tGrid, bGrid, self.cellSize):
                # skip if offscreen
                if x < -self.screenLimit or x >= self.screenLimit or y < -self.screenLimit or y >= self.screenLimit:
                    continue
                # xo, yo hold the x and y coordinates offset to always be positive
                if self.grid.rule.hex == True:
                    xo, yo = x + self.screenLimit, (y + self.screenLimit + (x-x%self.cellSize)//2)
                else:
                    xo, yo = x + self.screenLimit, y + self.screenLimit
                xi = int(xo // self.cellSize) % self.grid.gridsize
                yi = int(yo // self.cellSize) % self.grid.gridsize
                if self.grid.grid[xi][yi] == 1:
                    if self.grid.rule.hex == True and xi%2 == 1:
                        self.cells.append(
                            self.c.create_rectangle(x,y-self.cellSize//2, x+self.cellSize, y+self.cellSize-self.cellSize//2, fill='black')
                        )
                    else:
                        self.cells.append(
                            self.c.create_rectangle(x,y, x+self.cellSize, y+self.cellSize, fill='black')
                        )
        # layering
        self.c.tag_raise(self.scLimitBox)
        self.c.tag_raise(self.cursor)
        self.w.update()