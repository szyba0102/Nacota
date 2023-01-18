from tkinter import Tk, Canvas, BOTH
import math

coord = [400, 300]
angle = 0
pen_color = "black"
pointer = None
pen_down = True
turtle_down = True
root = Tk()
root.geometry("800x800")
canvas = Canvas(root)


def t_FORWARD(dist):
    global angle, canvas, pointer, pen_color, turtle_down
    canvas.delete(pointer)
    radians = math.radians(angle)
    x = math.sin(radians) * dist
    y = math.cos(radians) * dist
    if pen_down:
        canvas.create_line(coord, coord[0] + x, coord[1] - y, fill=pen_color)
        canvas.pack(fill=BOTH, expand=1)

    coord[0] += x
    coord[1] -= y
    print(coord)
    if coord[0] > 800:
        coord[0] -= 800
        print("zmiana",coord)

    elif coord[0] < 0:
        coord[0] += 800
        print("zmiana", coord)
    if coord[1] > 800:
        coord[1] -= 800
        print("zmiana", coord)

    elif coord[1] < 0:
        coord[1] += 800
        print("zmiana", coord)

    if turtle_down:
        t_CREATE_POINTER()


def t_BACKWARD(dist):
    global angle, canvas, pointer, pen_color, turtle_down
    canvas.delete(pointer)
    x = math.sin(math.radians(angle)) * dist
    y = math.cos(math.radians(angle)) * dist
    if pen_down:
        canvas.create_line(coord, coord[0] - x, coord[1] + y, fill=pen_color)
        canvas.pack(fill=BOTH, expand=1)

    coord[0] -= x
    coord[1] += y
    if turtle_down:
        t_CREATE_POINTER()


def t_LEFT(val):
    global angle, canvas, pointer, turtle_down
    canvas.delete(pointer)
    angle = (angle - val) % 360
    if turtle_down:
        t_CREATE_POINTER()


def t_RIGHT(val):
    global angle, canvas, pointer, turtle_down
    canvas.delete(pointer)
    angle = (angle + val) % 360
    if turtle_down:
        t_CREATE_POINTER()


def t_HOME():
    coord[0] = 400
    coord[1] = 300


def t_CLEAR_SCREEN():
    global canvas
    canvas.delete("all")
    if turtle_down:
        t_CREATE_POINTER()


def t_CREATE_POINTER():
    global angle, canvas, pointer
    x1 = coord[0] + math.sin(math.radians((angle + 90) % 360)) * 4
    y1 = coord[1] - math.cos(math.radians((angle + 90) % 360)) * 4
    x2 = coord[0] + math.sin(math.radians(angle)) * 15
    y2 = coord[1] - math.cos(math.radians(angle)) * 15
    x3 = coord[0] + math.sin(math.radians((angle - 90) % 360)) * 4
    y3 = coord[1] - math.cos(math.radians((angle - 90) % 360)) * 4
    points = [x1, y1, x2, y2, x3, y3]
    pointer = canvas.create_polygon(points)


def t_PEN_COLOR(new_color):
    global pen_color
    pen_color = new_color


def t_BACKGROUND_COLOR(new_color):
    global canvas
    canvas.configure(bg=new_color)


def t_TURTLE_UP():
    global turtle_down
    turtle_down = False


def t_TURTLE_DOWN():
    global turtle_down
    turtle_down = True


def t_PEN_UP():
    global pen_down
    pen_down = False


def t_PEN_DOWN():
    global pen_down
    pen_down = True



