import ply.lex as lex
from tkinter import Tk, Canvas, Frame, BOTH
from parser import *
import math



if __name__ == '__main__':
    root = Tk()
    root.geometry("600x600")
    canvas = Canvas(root)
    angle = 60
    t_FORAWRD(200, angle, canvas)
    angle = RIGHT(angle,200)
    t_FORAWRD(angle, 200, canvas)
    root.mainloop()
    # print(math.cos(math.radians(90)))





