from tkinter import *


class sudokuFrame(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.parent = parent
        self.controller = controller


        valid = (self.register(validate_entry), '%P')
        for row in range(9):
            for col in range(9):
                entry = Entry(self, width=2, validate='key', validatecommand=valid, justify='center')
                entry.grid(row=row, column=col, padx=4, pady=4)




#To make it so that the only thing a user can input is a number and only 1 number max
def validate_entry(char_input):
    if len(char_input) <= 1 and char_input.isdigit() or char_input == "":
        return True
    else:
        return False
