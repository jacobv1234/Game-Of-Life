from time import sleep, perf_counter

from lib.gameWindow import GameWindow
from lib.grid import Grid
from lib.rule import Rule

# create instances of classes
grid = Grid(Rule())
window = GameWindow(grid)



# mainloop
while window.running:
    start = perf_counter()

    if window.simulationOn:
        grid.next()

    window.update()

    # frame rate lock
    # fixed at almost 60 fps
    # if calculations take longer than 1/60s then run as fast as possible instead
    end = perf_counter()
    diff = end - start
    if diff < 1 / 60:
        sleep(1 / 60 - diff)