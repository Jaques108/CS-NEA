from tkinter import *


class sudokuFrame(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.parent = parent
        self.controller = controller



    def createGrid(self):
        cellSize = 40
        canvasSize = 40 * 9

        canvas = Canvas(self, width=canvasSize, height=canvasSize)
        canvas.pack()
        canvas.focus_set()


        valid = (self.register(validate_entry), '%P')

        for row in range(9):
            for col in range(9):
                x1 = col * cellSize
                y1 = row * cellSize
                x2 = x1 + cellSize
                y2 = y1 + cellSize
                rectagleID = canvas.create_rectangle(x1,y1,x2,y2,fill="white", outline="black")



#To make it so that the only thing a user can input is a number and only 1 number max
def validate_entry(char_input):
    if len(char_input) <= 1 and char_input.isdigit() or char_input == "":
        return True
    else:
        return False
