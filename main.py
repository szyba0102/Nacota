import ply.lex as lex
from tkinter import Tk, Canvas, Frame, BOTH
import math
tokens = ['FORWARD', 'BACKWARD', 'LEFT', 'RIGHT', 'CLEARSCREEN', 'HOME']
coord = [300, 300]
# angle = 90

def t_FORAWRD(dist, angle, canvas):
    radians = math.radians(angle)
    x = math.sin(radians) * dist
    y = math.cos(radians) * dist
    # print(math.sin(radians))
    # print(math.cos(radians))
    canvas.create_line(coord, coord[0] + x, coord[1] - y)
    coord[0] += x
    coord[1] -= y
    canvas.pack(fill=BOTH, expand=1)

def t_BACKWARD(dist, angle, canvas):
    x = math.sin(math.radians(angle)) * dist
    y = math.cos(math.radians(angle)) * dist
    canvas.create_line(coord, coord[0] - x, coord[1] + y)
    coord[0] -= x
    coord[1] += y
    canvas.pack(fill=BOTH, expand=1)


def LEFT(val):
    angle = math.abs()

def RIGHT(angle, val):
    angle = ((angle + val) % 360)
    return angle

# def init():
#     root = Tk()
#     root.geometry("300x150")
#     canvas = Canvas(root)
#     canvas.pack()
#     root.mainloop()

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





