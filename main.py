import nacota_parser as pr
from tkinter import *

input_txt = None
lexer, parser = pr.create_parser()
def start(text):

    def Take_input():
        INPUT = input_txt.get("1.0", "end-1c")
        # print(input_txt)
        if INPUT == "":
            return
        execute(INPUT)

    l = Label(text="command")
    input_txt = Text(pr.fc.root, height=5,
                    width=80,
                    bg="light yellow")


    Display = Button(pr.fc.root, height=2,
                     width=20,
                     text="Execute",
                     command=lambda: Take_input())

    l.pack()
    input_txt.pack()
    Display.pack()

    execute(text)



def execute(text):
    global lexer, parser
    parser.parse(text, lexer=lexer)
    pr.fc.root.mainloop()


if __name__ == '__main__':

    text = "i:=1 while i < 25 do backward 10 right 10 i:=i+1 end i:=1 while i < 25 do backward 10 left 10 i:=i+1 end"
    start("forward 1")

    '''
    great example:
    c:=15
    while c>0 do
    a:=10
    b:=10
    while a>0 do while b>0 do forward 10 left 10 b:=b-1 end a:=a-1 forward a end
    c:=c-1
    end
    
    another one:
    a:=10
    while a>0 do
    b:=10
    while b>0 do forward 4 penup forward 4 pendown forward 4 left 10 b:=b-1 end
    a:=a-1
    end
    
    pencolor:
    pencolor blue forward 100 pencolor pink left 90 forward 100 
    
    kolorowa gwiazda:
    background pink pencolor white turtleup
    a:=20
    while a>0 do
    forward 100 left 170 forward 100
    a:=a-1
    end
    pencolor yellow
    a:=20
    while a>0 do
    forward 100 left 170 forward 100
    a:=a-1
    end
    '''
