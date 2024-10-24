from tkinter import *


class choiceFrame(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.parent = parent
        self.controller = controller

        #self.geometry("400x150")
        #self.title("What to play")

        sudokuButton = Button(self, text="Sudoku", command=lambda:self.controller.show_frame('sudokuFrame','350x335','Sudoku'),width = 20,height = 20)
        sudokuButton.place(relx=0.25, rely=0.5, anchor=CENTER)

        crosswordsButton = Button(self, text="Crossword", width=20, height=20)
        crosswordsButton.place(relx=0.75, rely=0.5, anchor=CENTER)
