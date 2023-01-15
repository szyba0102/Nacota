import ply.lex as lex
from tkinter import Tk, Canvas, Frame, BOTH
from parser import *
import math
import ply.yacc as yacc

coord = [300, 300]
# angle = 0
color = ["black"]

def t_FORWARD(dist, angle, canvas, pointer):
    canvas.delete(pointer)
    radians = math.radians(angle)
    x = math.sin(radians) * dist
    y = math.cos(radians) * dist
    # print(math.sin(radians))
    # print(math.cos(radians))
    canvas.create_line(coord, coord[0] + x, coord[1] - y, fill=color[0])
    coord[0] += x
    coord[1] -= y
    canvas.pack(fill=BOTH, expand=1)
    return CREATE_POINTER(angle, canvas)

def t_BACKWARD(dist, angle, canvas, pointer):
    canvas.delete(pointer)
    x = math.sin(math.radians(angle)) * dist
    y = math.cos(math.radians(angle)) * dist
    canvas.create_line(coord, coord[0] - x, coord[1] + y, fill=color[0])
    coord[0] -= x
    coord[1] += y
    canvas.pack(fill=BOTH, expand=1)
    return CREATE_POINTER(angle, canvas)


def t_LEFT(angle, val,pointer, canvas):
    canvas.delete(pointer)
    new_angle = (angle - val) % 360
    return new_angle, CREATE_POINTER(new_angle,canvas)


def t_RIGHT(angle, val,pointer, canvas):
    canvas.delete(pointer)
    new_angle = (angle + val) % 360
    return new_angle, CREATE_POINTER(new_angle, canvas)

def t_HOME():
    coord[0] = 300
    coord[1] = 300

def t_CLEARSCREEN(canvas):
    canvas.delete("all")

def CREATE_POINTER(angle,canvas):
    x1 = coord[0] + math.sin(math.radians((angle + 90 ) % 360)) * 4
    y1 = coord[1] - math.cos(math.radians((angle + 90) % 360)) * 4
    x2 = coord[0] + math.sin(math.radians(angle)) * 15
    y2 = coord[1] - math.cos(math.radians(angle)) * 15
    x3 = coord[0] + math.sin(math.radians((angle - 90) % 360)) * 4
    y3 = coord[1] - math.cos(math.radians((angle - 90) % 360)) * 4
    points = [x1, y1, x2, y2, x3, y3]
    pointer = canvas.create_polygon(points)
    return pointer

def t_COLOR(new_color):
    color[0] = new_color

def t_BACKGROUND_COLOR(new_color, canvas):
    canvas.configure(bg=new_color)

def init():
    root = Tk()
    root.geometry("300x150")
    canvas = Canvas(root)
    canvas.pack()
    root.mainloop()


if __name__ == '__main__':

    root = Tk()
    root.geometry("600x600")
    canvas = Canvas(root)

    angle = 60
    pointer = CREATE_POINTER(angle, canvas)
    pointer = t_FORWARD(200, angle, canvas, pointer)
    angle, pointer = t_RIGHT(angle, 30, pointer, canvas)
    t_COLOR('red')
    t_BACKGROUND_COLOR('yellow', canvas)
    pointer = t_FORWARD(200, angle, canvas, pointer)
    angle, pointer = t_RIGHT(angle, 30, pointer, canvas)
    # angle = t_LEFT(angle, 250)
    # print(angle)
    # t_FORWARD(200, angle, canvas)
    # t_CLEARSCREEN(canvas)
    # canvas.create_polygon(300,300,300,310,310,300)


    root.mainloop()
    # lexer = lex.lex()
    # parser = yacc.yacc()
    # text = 'a := 5'
    # parser.parse(text, lexer=lexer)
