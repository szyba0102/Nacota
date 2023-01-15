import ply.lex as lex
import ply.yacc as yacc

import main

TESTING = True

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'while': 'WHILE',
    'do': 'DO',
    'end': 'END',
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
}

symtab = {}

tokens = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'NUMBER', 'ID',
          'PLACE', 'NOTSMALLER', 'NOTBIGGER', 'EQUAL', 'SMALLER', 'BIGGER'] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
# t_LPAREN  = r'\('
# t_RPAREN  = r'\)'
# t_LBRACE = r'\{'
# t_RBRACE = r'\}'
t_PLACE = r'\:='
t_EQUAL = r'\='
t_SMALLER = r'\<'
t_NOTSMALLER = r'\>='
t_NOTBIGGER = r'\<='
t_BIGGER = r'\>'

t_ignore = ' \t'


def t_ID(t):
    r"[a-zA-Z_]\w*"
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)

def p_S(p):
    """S : ciag_instr """
    p[0] = p[1]

def p_ciag_instr(p):
    """ciag_instr : instrukcja ciag_instr
                    | empty"""
    if len(p) == 3:
        if p[2] is None: p[0] = p[1]
        else: p[0] = [p[1],p[2]]


def p_empty(p):
    'empty :'
    # pass


def p_instrukcja(p):
    """instrukcja : instr_podst
                    | instr_spec
                    | instr_assign"""
    p[0] = p[1]


def p_instr_podst(p):
    """instr_podst : instr_zmienna
                    | instr_zwykla"""
    p[0] = p[1]

def p_instr_zmienna(p):
    """instr_zmienna : FORWARD exp
                    | BACKWARD exp
                    | LEFT exp
                    | RIGHT exp
                    | BACKGROUND color
                    | PENCOLOR color"""
    if p[1] == 'forward': p[1] = main.t_FORWARD
    elif p[1] == 'backward': p[1] = main.t_BACKWARD
    elif p[1] == 'left': p[1] = main.t_LEFT
    elif p[1] == 'right': p[1] = main.t_RIGHT
    elif p[1] == 'background': p[1] = main.t_BACKWARD
    elif p[1] == 'pencolor': p[1] = main.t_PEN_COLOR
    p[0] = (p[1], p[2])


def p_color(p):
    """color : NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"""
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]


def p_exp(p):  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! def t_IDENT(t):
    """exp : numexp
            | ID """
    p[0] = p[1]

def p_numexp(p):
    """numexp : NUMBER
                | NUMBER numexp"""
    if len(p) == 3:
        # p[0] = [p[1],p[2]]
        p[0] = p[1]*10 + p[2]
    else:
        p[0] = p[1]


def p_instr_zwykla(p):
    """instr_zwykla : CLEARSCREEN
                    | HOME
                    | PENUP
                    | PENDOWN"""
    if p[1] == "clearscreen":
        p[0] = (main.t_CLEAR_SCREEN,None)
    elif p[1] == "home":
        p[0] = (main.t_HOME,None)
    elif p[1] == "penup":
        p[0] = (main.t_PEN_UP,None)
    elif p[1] == "pendown":
        p[0] = (main.t_PEN_DOWN,None)


def p_instr_assign(p):
    """instr_assign : ID PLACE exp
                    | ID PLACE instr_mat"""
    p[0] = p[3]
    symtab[p[1]] = p[3]
    print(p[1],p[3])

    # if p[2] == 'exp':
    #     p[0] = p[3]
    # elif p[2] == 'instr_mat':
    #     p[0] = p[3]


def p_instr_mat(p):
    """instr_mat : exp PLUS exp
            | exp MINUS exp
            | exp TIMES exp
            | exp DIVIDE exp"""

    x = symtab[p[1]] if isinstance(p[1],str) else p[1]
    y = symtab[p[3]] if isinstance(p[3],str) else p[3]

    if p[2] == '+':
        p[0] = x + y
    elif p[2] == '-':
        p[0] = x - y
    elif p[2] == '*':
        p[0] = x * y
    elif p[2] == '/':
        p[0] = x / y



def p_instr_war(p):
    """instr_war : exp SMALLER exp
            | exp NOTSMALLER exp
            | exp BIGGER exp
            | exp NOTBIGGER exp
            | exp EQUAL exp"""
    p[0] = (p[1],p[2],p[3])


def p_instr_spec(p):
    """instr_spec : instr_while
                | instr_if"""
    p = p[1]
    func = instr_war_to_func(p[1][1])

    if p[0] == 'while':
        global TESTING
        i = 0
        while func(
                    symtab[p[1][0]] if isinstance(p[1][0],str) else p[1][0],
                    symtab[p[1][2]] if isinstance(p[1][2],str) else p[1][2]
                ):

            for instr in p[3]:
                if instr[1] is None: instr[0]()
                else: instr[0](instr[1])

            if TESTING:
                i += 1
                if i > 10: break

    elif p[0] == 'if':
        if func(
                    symtab[p[1][0]] if isinstance(p[1][0],str) else p[1][0],
                    symtab[p[1][2]] if isinstance(p[1][2],str) else p[1][2]
                ):

            for instr in p[3]:
                if instr[1] is None: instr[0]()
                else: instr[0](instr[1])





def p_instr_while(p):
    """instr_while : WHILE instr_war DO ciag_instr END """
    # if p[2] == 'instr_war' and p[4] == 'ciag_instr':
    # while p[2]: p[4][0](p[4][1])
    # for i in range(len(p)): print(p[i])
    # while p[2]: print(p[4])

    p[0] = [p[1], p[2], p[3], p[4], p[5]]


def p_instr_if(p):
    """instr_if : IF instr_war THEN ciag_instr END """
    # if p[2] == 'instr_war' and p[4] == 'ciag_instr':
    #     if p[2]: p[4]

    p[0] = [p[1], p[2], p[3], p[4], p[5]]


def instr_war_to_func(sign):
    func = lambda a, b: a == b
    if sign == '<':
        func = lambda a, b: a < b
    elif sign == '>=':
        func = lambda a, b: a >= b
    elif sign == '>':
        func = lambda a, b: a > b
    elif sign == '<=':
        func = lambda a, b: a <= b
    elif sign == '==':
        func = lambda a, b: a == b
    return func

# def p_error(p):
#     print("parsing error\n")

if __name__ == '__main__':
    # root = Tk()
    # root.geometry("600x600")
    # canvas = Canvas(root)
    # angle = 60
    # t_FORAWRD(200, angle, canvas)
    # angle = RIGHT(angle,200)
    # t_FORAWRD(angle, 200, canvas)
    # root.mainloop()
    # print(math.cos(math.radians(90)))
    lexer = lex.lex()
    parser = yacc.yacc()
    # text = 'forward 1'
    # text = 'a:=1'
    # text = "i:=1 while i < 3 do home clearscreen i:=i+1 end forward 1"
    text = "i:=1 while i < 3 do backward 1 clearscreen end forward 1"
    # text = "i:=1 while i < 3 do home clearscreen i:=i+1 end i:=5 if i==5 then penup end"
    parser.parse(text, lexer=lexer)

