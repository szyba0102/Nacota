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

tokens = ['PLUS',  'MINUS',  'TIMES',  'DIVIDE',  'LPAREN',  'RPAREN',  'NUMBER', 'ID', 'LBRACE', 'RBRACE', 'ASSIGN'] + list(reserved.values())
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
t_ASSIGN = r'\='

t_ignore = ' \t'

def t_ID(t):
    r"[a-zA-Z_]\w*"
    return t

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



def p_ciag_instr(p):
    '''ciag_instr : instrukcja ciag_instr
                  | instrukcja'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_instrukcja(p):
    """instrukcja : instr_podst | intr_spec | inst_assign"""
    p[0] = p[1]

def p_instr_podst(p):
    """instr_podst : intr_zmienna | inst_zwykla"""
    p[0] = p[1]

def p_instr_zmienna(p):
    """instr_zmienna : FORWARD exp | BACKWARD exp | LEFT exp | RIGHT exp | BACKGROUND exp | PENCOLOR exp"""
    p[0] = (p[1], p[2])

def p_color(p):
    """color : NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"""
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]

def p_exp(p):   #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! def t_IDENT(t):
    '''exp : NUMBER | NUMBER exp | ID '''
    if len(p) == 2:
        p[0]=p[1]
    elif len(p) == 3:
        p[0] = [p[1],p[2]]

def p_instr_zwykla(p):
    '''instr_zwykla : CLEARSCREEN | HOME | PENUP | PENDOWN'''
    p[0] = p[1]

def p_instr_assign(p):
    '''instr_assign : ID ASSIGN exp
                    | ID ASSIGN instr_mat'''
    if p[2] == 'exp':
        p[0] = p[3]
    elif p[2] == 'instr_mat':
        p[0] = p[3]

def p_instr_mat(p):
    '''instr_mat : exp PLUS exp
            | exp MINUS exp
            | exp TIMES exp
            | exp DIVIDE exp'''
    if p[2] == 'PLUS':
        p[0] = p[1] + p[3]
    elif p[2] == 'MINUS':
        p[0] = p[1] - p[3]
    elif p[2] == 'TIMES':
        p[0] = p[1] * p[2]
    elif p[2] == 'DIVIDE':
        p[0] = p[1] / p[3]

def p_instr_war(p):
    '''instr_war : exp SMALLER exp
            | exp NOTSMALLER exp
            | exp BIGEER exp
            | exp NOTBIGGER exp'''
    if p[2] == 'SMALLER':
        p[0] = p[1] < p[3]
    elif p[2] == 'NOTSMALLER':
        p[0] = p[1] >= p[3]
    elif p[2] == 'BIGGER':
        p[0] = p[1] > p[2]
    elif p[2] == 'NOTBIGGER':
        p[0] = p[1] <= p[3]

def p_instr_spec(p):
    '''instr_spec : instr_while | instr_if'''
    # if p[1] == 'instr_while' :
    #     p[0] = 'instr_while'
    # elif p[1] == 'instr_if':
    #     p[0] = 'instr_if'
    p[0] = [1]

def p_instr_while(p):
    '''instr_while : WHILE instr_war DO ciag_instr END '''
    # if p[2] == 'instr_war' and p[4] == 'ciag_instr':
    #     while p[2]: p[4]
    p[0] = [p[1], p[2], p[3], p[4], p[5]]

def p_instr_if(p):
    '''instr_if : IF instr_war THEN ciag_instr END '''
    # if p[2] == 'instr_war' and p[4] == 'ciag_instr':
    #     if p[2]: p[4]
    p[0] = [p[1], p[2], p[3], p[4], p[5]]






