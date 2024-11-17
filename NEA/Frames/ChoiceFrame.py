from tkinter import *


class choiceFrame(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.parent = parent
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)  # Column 0 has weight
        self.grid_columnconfigure(1, weight=1)


        sudokuButton = Button(self, text="Sudoku", command=lambda:self.controller.show_frame('sudokuFrame','350x335','Sudoku'),width = 20,height = 20)
        sudokuButton.grid(row=0,column=0,sticky = 'news')

        crosswordsButton = Button(self, text="Crossword",command=lambda:self.controller.show_frame('crosswordFrame','','Crossword'),width=20, height=20)
        crosswordsButton.grid(row = 0,column=1,sticky = 'news')
