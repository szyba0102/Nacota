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
# root.resizable(False,False)


def t_FORWARD(dist, symtab):
    global angle, canvas, pointer, pen_color, turtle_down
    checkY = False
    checkX = False
    if isinstance(dist, str): dist = symtab[dist]
    canvas.delete(pointer)
    radians = math.radians(angle)
    x = math.sin(radians) * dist
    y = math.cos(radians) * dist
    prev_coord = coord.copy()
    if pen_down:
        if not (coord[0] + x >= 800 or coord[0] + x <= 0 or coord[1] - y >= 650 or coord[1] + y <= 15):
            canvas.create_line(coord, coord[0] + x, coord[1] - y, fill=pen_color)
            coord[0] += x
            coord[1] -= y
        else:
            if coord[0] + x >= 800:
                tmp = 800 - coord[0]
                new_y = tmp * y / x
                coord[0] = 800
                coord[1] -= new_y
                canvas.create_line(prev_coord, coord[0], coord[1], fill=pen_color)
            elif coord[0] + x <= 0:
                tmp = coord[0]
                new_y = tmp * y / x
                coord[0] = 0
                coord[1] += new_y
                canvas.create_line(prev_coord, coord[0], coord[1], fill=pen_color)
            if coord[1] - y >= 650:
                tmp = 650 - coord[1]
                new_x = tmp * x / y
                coord[1] = 650
                coord[0] -= new_x
                canvas.create_line(prev_coord, coord[0], coord[1], fill=pen_color)
            elif coord[1] + y <= 15:
                tmp = coord[1] - 15
                new_x = tmp * x / y
                coord[1] = 15
                coord[0] += new_x
                canvas.create_line(prev_coord, coord[0], coord[1], fill=pen_color)
        canvas.pack(fill=BOTH, expand=1)

    # coord[0] += x
    # coord[1] -= y
    #
    # if coord[0] >= 800:
    #     coord[0] -= 800
    #     print("zmiana",coord)
    #
    # elif coord[0] <= 0:
    #     coord[0] += 800
    #     print("zmiana", coord)
    # if coord[1] >= 800:
    #     coord[1] -= 785
    #     print("zmiana", coord)
    #
    # elif coord[1] <= 15:
    #     coord[1] += 785
    #     print("zmiana", coord)

    if turtle_down:
        t_CREATE_POINTER()


def t_BACKWARD(dist, symtab):
    global angle, canvas, pointer, pen_color, turtle_down
    if isinstance(dist, str): dist = symtab[dist]
    canvas.delete(pointer)
    x = math.sin(math.radians(angle)) * dist
    y = math.cos(math.radians(angle)) * dist
    if pen_down:
        canvas.create_line(coord, coord[0] - x, coord[1] + y, fill=pen_color)
        canvas.pack(fill=BOTH, expand=1)

    coord[0] -= x
    coord[1] += y
    print(coord)
    if turtle_down:
        t_CREATE_POINTER()


def t_LEFT(val, symtab):
    global angle, canvas, pointer, turtle_down
    if isinstance(val, str): val = symtab[val]
    canvas.delete(pointer)
    angle = (angle - val) % 360
    if turtle_down:
        t_CREATE_POINTER()


def t_RIGHT(val, symtab):
    global angle, canvas, pointer, turtle_down
    if isinstance(val, str): val = symtab[val]
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
    radians = math.radians(angle)
    x = math.sin(radians) * 3
    y = math.cos(radians) * 3
    x1 = coord[0] + math.sin(math.radians((angle + 90) % 360)) * 4 - x
    y1 = coord[1] - math.cos(math.radians((angle + 90) % 360)) * 4 + y
    x2 = coord[0] + math.sin(math.radians(angle)) * 15 - x
    y2 = coord[1] - math.cos(math.radians(angle)) * 15 + y
    x3 = coord[0] + math.sin(math.radians((angle - 90) % 360)) * 4 - x
    y3 = coord[1] - math.cos(math.radians((angle - 90) % 360)) * 4 + y
    points = [x1, y1, x2, y2, x3, y3]
    pointer = canvas.create_polygon(points)


def t_PEN_COLOR(new_color, *args):
    global pen_color
    pen_color = new_color


def t_BACKGROUND_COLOR(new_color, *args):
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



