import math
import ply.lex as lex
from tkinter import Tk, Canvas, Frame, BOTH

reserved = {
    'if': 'IF',
    # 'then': 'THEN',
    'forward': 'FORWARD',
    'backward': 'BACKWARD',
    'left': 'LEFT',
    'right': 'RIGHT',
    'clearscreen': 'CLEARSCREEN',
    'home': 'HOME',
    'penup': 'PENUP',
    'pendown': 'PENDOWN',
    'background': 'BACKGROUND',
    'pencolor': 'PENCOLOR',
    'while': 'WHILE',
    'do': 'DO',
    'end': 'END',
    'then': 'THEN'
}

tokens = ['PLUS',  'MINUS',  'TIMES',  'DIVIDE',  'LPAREN',  'RPAREN',  'NUMBER', 'ID', 'LBRACE', 'RBRACE'] + list(reserved.values())
coord = [300, 300]
# angle = 90

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_PLACE = r'\:='
t_EQUAL = r'\='
t_SMALLER = r'\<'
t_NOTSMALLER = r'\>='
t_NOTBIGGER = r'\<='
t_BIGGER = r'\>'



t_ignore = ' \t'

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


def t_LEFT(val):
    angle = math.abs()

def t_RIGHT(angle, val):
    angle = ((angle + val) % 360)
    return angle

# def FOR()
# def init():
#     root = Tk()
#     root.geometry("300x150")
#     canvas = Canvas(root)
#     canvas.pack()
#     root.mainloop()
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" %(t.lineno, t.value[0]) )
    t.lexer.skip(1)