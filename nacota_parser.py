import ply.lex as lex
import ply.yacc as yacc
import func as fc


TESTING = True

symtab = {}

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
    'turtleup': 'TURTLEUP',
    'turtledown': 'TURTLEDOWN'
}



tokens = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'NUMBER', 'ID',
          'PLACE', 'NOTSMALLER', 'NOTBIGGER', 'EQUAL', 'SMALLER', 'BIGGER'] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_PLACE = r'\:='
t_EQUAL = r'\='
t_SMALLER = r'\<'
t_NOTSMALLER = r'\>='
t_NOTBIGGER = r'\<='
t_BIGGER = r'\>'

t_ignore = ' \t'


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_ID(t):
    r"[a-zA-Z_]\w*"
    t.type = reserved.get(t.value, 'ID')
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
    executor(p[0])


def executor(output):
    for instr in output:
        args = instr[1]
        if args[0] == None:
            instr[0]()
        elif len(args) == 3:
            instr[0](args[0], args[2], args[1])
        elif len(args) == 2:
            instr[0](args[0], args[1])
        else:
            instr[0](args[0])


def p_ciag_instr(p):
    """ciag_instr : instrukcja ciag_instr
                    | empty"""
    if len(p) == 3:
        if p[2] is not None:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]


def p_empty(p):
    'empty :'


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
    if p[1] == 'forward':
        p[1] = fc.t_FORWARD
    elif p[1] == 'backward':
        p[1] = fc.t_BACKWARD
    elif p[1] == 'left':
        p[1] = fc.t_LEFT
    elif p[1] == 'right':
        p[1] = fc.t_RIGHT
    elif p[1] == 'background':
        p[1] = fc.t_BACKGROUND_COLOR
    elif p[1] == 'pencolor':
        p[1] = fc.t_PEN_COLOR
    p[0] = (p[1], [p[2],symtab])


def p_color(p):
    """color : ID"""
    if not p[1] in ["red","yellow","blue","green","purple","pink","brown","white","black","orange"]: p_error(p)
    p[0] = p[1]


def p_exp(p):
    """exp : NUMBER
            | ID """
    p[0] = p[1]


def p_instr_zwykla(p):
    """instr_zwykla : CLEARSCREEN
                    | HOME
                    | PENUP
                    | PENDOWN
                    | TURTLEUP
                    | TURTLEDOWN"""
    if p[1] == "clearscreen":
        p[0] = (fc.t_CLEAR_SCREEN, [None])
    elif p[1] == "home":
        p[0] = (fc.t_HOME, [None])
    elif p[1] == "penup":
        p[0] = (fc.t_PEN_UP, [None])
    elif p[1] == "pendown":
        p[0] = (fc.t_PEN_DOWN, [None])
    elif p[1] == "turtleup":
        p[0] = (fc.t_TURTLE_UP, [None])
    elif p[1] == "turtledown":
        p[0] = (fc.t_TURTLE_DOWN, [None])


def p_instr_assign(p):
    """instr_assign : ID PLACE exp
                    | ID PLACE instr_mat"""

    def func(a, b):
        global symtab
        if not isinstance(b, int):
            func2, args = b
            x, y, sign = args[0], args[1], args[2]
            b = func2(x, y, sign)
        symtab[a] = b

    p[0] = (func, [p[1], p[3]])


def p_instr_mat(p):
    """instr_mat : exp PLUS exp
            | exp MINUS exp
            | exp TIMES exp
            | exp DIVIDE exp"""

    def func(x, y, sign):
        global symtab
        x = symtab[x] if isinstance(x, str) else x
        y = symtab[y] if isinstance(y, str) else y
        func2 = lambda a, b: a + b
        if sign == '-':
            func2 = lambda a, b: a - b
        elif sign == '*':
            func2 = lambda a, b: a * b
        elif sign == '/':
            func2 = lambda a, b: a / b

        return func2(x, y)

    p[0] = (func, [p[1], p[3], p[2]])


def p_instr_war(p):
    """instr_war : exp SMALLER exp
            | exp NOTSMALLER exp
            | exp BIGGER exp
            | exp NOTBIGGER exp
            | exp EQUAL exp"""

    def func(x, y, sign):
        global symtab
        x = symtab[x] if isinstance(x, str) else x
        y = symtab[y] if isinstance(y, str) else y
        func2 = lambda a, b: a == b
        if sign == '<':
            func2 = lambda a, b: a < b
        elif sign == '>=':
            func2 = lambda a, b: a >= b
        elif sign == '>':
            func2 = lambda a, b: a > b
        elif sign == '<=':
            func2 = lambda a, b: a <= b
        elif sign == '==':
            func2 = lambda a, b: a == b

        return func2(x, y)

    p[0] = (func, [p[1], p[3], p[2]])


def p_instr_spec(p):
    """instr_spec : instr_while
                | instr_if"""
    tmp = p[1]
    warunek = tmp[1]
    ciag = tmp[3]

    def funcWHILE(warunek, ciag):
        while warunek[0](warunek[1][0], warunek[1][1], warunek[1][2]):
            for instr in ciag:
                args = instr[1]
                if args[0] == None:
                    instr[0]()
                elif len(args) == 3:
                    instr[0](args[0], args[2], args[1])
                elif len(args) == 2:
                    instr[0](args[0], args[1])
                else:
                    instr[0](args[0])

    def funcIF(warunek, ciag):
        if warunek[0](warunek[1][0], warunek[1][1], warunek[1][2]):
            for instr in ciag:
                args = instr[1]
                if args[0] == None:
                    instr[0]()
                elif len(args) == 3:
                    instr[0](args[0], args[2], args[1])
                elif len(args) == 2:
                    instr[0](args[0], args[1])
                else:
                    instr[0](args[0])

    if tmp[0] == 'while':
        p[0] = (funcWHILE, [warunek, ciag])
    elif tmp[0] == 'if':
        p[0] = (funcIF, [warunek, ciag])


def p_instr_while(p):
    """instr_while : WHILE instr_war DO ciag_instr END """

    p[0] = [p[1], p[2], p[3], p[4], p[5]]


def p_instr_if(p):
    """instr_if : IF instr_war THEN ciag_instr END """

    p[0] = [p[1], p[2], p[3], p[4], p[5]]

def p_error(p):
   if p:
      print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
   else:
      print("Unexpected end of input")


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


def create_parser():
    global symtab
    lexer = lex.lex()
    parser = yacc.yacc()
    return lexer, parser

