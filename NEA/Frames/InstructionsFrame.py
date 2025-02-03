from tkinter import *



#Create the class
class instructionsFrame(Frame):
    #Initialise the class
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.font = ('Georgia',28)

        self.crosswordInstructionsMessage = '\n'+'To play a crossword, start by looking at the clues, which are divided into “Across” and “Down.” Each clue corresponds to a number on the grid, and your task is to fill in words that fit both the clue and the length of the space available. As you solve some clues, you’ll fill in letters that intersect with other words, which will help you figure out the remaining answers. Sometimes, you might have to work through a few tricky spots by guessing letters based on what fits in other words.'
        self.sudokuInstructionsMessage = '\n'+'In Sudoku, the goal is to fill a 9x9 grid with the numbers 1 through 9. Each number must appear exactly once in each row, column, and 3x3 sub-grid. You start with a few numbers already filled in, and from there, use logic to figure out where the other numbers belong. It’s all about using the process of elimination, figuring out where a number can or can’t go based on the existing numbers in the grid.'


        self.crosswordInstructionsLabel = Label(self,text = self.crosswordInstructionsMessage,wraplength=650,font = self.font)

        self.sudokuInstructionsLabel = Label(self, text=self.sudokuInstructionsMessage,wraplength=650,font = self.font)


        self.crosswordInstructionsButton = Button(self,text = 'Instructions for Crossword'+'\n',command = self.showCrosswordInstructions)
        self.crosswordInstructionsButton.pack()

        self.sudokuInstructionsButton = Button(self,text = 'Instructions for Sudoku'+'\n',command = self.showSudokuInstructions)
        self.sudokuInstructionsButton.pack()



    def showCrosswordInstructions(self):
        self.sudokuInstructionsLabel.pack_forget()
        self.crosswordInstructionsLabel.pack()

    def showSudokuInstructions(self):
        self.crosswordInstructionsLabel.pack_forget()
        self.sudokuInstructionsLabel.pack()
