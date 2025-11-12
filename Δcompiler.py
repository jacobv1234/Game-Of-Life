from os import system
# this file runs the nuitka command so it's not forgotten
system('python -m nuitka --onefile --output-filename="GameOfLife.exe" --enable-plugin=tk-inter --windows-console-mode=attach main.py')

# note:
# --standalone: compile Python into the file to make it portable
# --onefile: maximum portability
# omit both for faster compilation but dependent on Python installation