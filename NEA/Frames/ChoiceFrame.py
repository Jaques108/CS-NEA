from tkinter import *

#Need to do this to call functions inside of crosswordFrame and sudokuFrame
from NEA.Frames.CrosswordFrame import crosswordFrame
from NEA.Frames.SudokuFrame import sudokuFrame

#Create the class
class choiceFrame(Frame):
    #Initialise the class
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.parent = parent
        self.controller = controller

        #Make it so that buttons are placed correctly and the formatting doesn't mess up
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #Function to call the sudokuFrame instance
        def sudokuFrame():
            self.controller.showFrame('sudokuFrame', '', 'Sudoku')
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)


            #Create varible to hold sudokuFrame
            sudokuFrameInstance = self.controller.frames['sudokuFrame']

            #Run the createGrid function inside of sudokuFrame
            sudokuFrameInstance.createGrid()



        #Widgets
        sudokuButton = Button(self, text="Sudoku", command=sudokuFrame,width = 20,height = 20)
        sudokuButton.grid(row=0,column=0,sticky = 'news')

        crosswordsButton = Button(self, text="Crossword",command=lambda:self.controller.showFrame('crosswordFrame','','Crossword'),width=20, height=20)
        crosswordsButton.grid(row = 0,column=1,sticky = 'news')


