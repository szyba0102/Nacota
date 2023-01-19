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

    # Output = Text(pr.fc.root, height=5,
    #               width=25,
    #               bg="light cyan")

    Display = Button(pr.fc.root, height=2,
                     width=20,
                     text="Execute",
                     command=lambda: Take_input())

    l.pack()
    input_txt.pack()
    Display.pack()
    # Output.pack()

    # parser.parse(text, lexer=lexer)
    # pr.fc.root.mainloop()
    execute(text)



def execute(text):
    global lexer, parser
    parser.parse(text, lexer=lexer)
    pr.fc.root.mainloop()


if __name__ == '__main__':

    # text = "i:=1 backward 2 forward 3 left 5 i:=i+5"
    # text = "i:=1 while i < 3 do home clearscreen i:=i+1 end i:=5 if i==5 then penup end"
    text = "i:=1 while i < 25 do backward 10 right 10 i:=i+1 end i:=1 while i < 25 do backward 10 left 10 i:=i+1 end"
    start("forward 1")