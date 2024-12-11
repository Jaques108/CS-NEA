from tkinter import *

#Need to do this to call functions inside of crosswordFrame and sudokuFrame
from NEA.Frames.CrosswordFrame import crosswordFrame
from NEA.Frames.SudokuFrame import sudokuFrame


#Create the class
class choiceFrame(Frame):
    #Initialise the class
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        #Make it so that buttons are placed correctly and the formatting doesn't mess up
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        try:
            self.sudokuButton.destroy()
            self.crosswordsButton.destroy()

        except:
            pass

        # Widgets
        self.sudokuButton = Button(self, text="Sudoku", command=self.sudokuFrameOpen, width=20, height=20)
        self.sudokuButton.grid(row=0, column=0, sticky='news')

        self.crosswordsButton = Button(self, text="Crossword",command=lambda: self.controller.showFrame('crosswordFrame', '', 'Crossword'),width=20, height=20)
        self.crosswordsButton.grid(row=0, column=1, sticky='news')

    #Function to call the sudokuFrame instance
    def sudokuFrameOpen(self):
        self.controller.showFrame('sudokuFrame', '', 'Sudoku')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #Create varible to hold sudokuFrame
        sudokuFrameInstance = self.controller.frames['sudokuFrame']

        #Run the createGrid function inside of sudokuFrame
        sudokuFrameInstance.createGrid()
