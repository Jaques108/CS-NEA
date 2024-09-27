from tkinter import *

#OOP !
##Crossword = 2d list of cells, where cell is an object


class cell():
    def __init__(self,currentLetter):
        self.currentLetter = currentLetter

    def setLetter(self,letter):  #setter
        self.currentLetter = letter
    def getLetter(self): #Getter
        print(self.currentLetter)
class Crossword(Frame):
    def __init__(self,parent,controller):
        self.controller = controller
        self.parent = parent
        Frame.__init__(self,parent)
        self.crosswordgrid = [[cell('0') for i in range(13)] for k in range(13)]
        self.clues = []
        self.answers = [[cell('0') for i in range(13)] for k in range(13)]

        self.label1 = Label(self,text=self.controller.username)
        self.label1.grid(row=0,column=0)
    def populate(self):
        self.label1.config(text=self.controller.username)

    def ShowClues(self):
        print(self.clues)
        ###Integrate into GUI at somepoint
    def printGrid(self):
        for item in self.grid:

            Temp = [k.currentLetter for k in item]
            print(Temp)
        #integrate into GUI
    def CheckIfCorrect(self):
        for i in range(len(self.crosswordgrid)):
            for k in range(len(self.crosswordgrid[i])):
                if self.crosswordgrid[i][k].currentLetter != self.answers[i][k].currentLetter:
                    return False
        return True
    def ChangeCell(self,x,y,value):
        self.grid[x][y].setLetter(value)


# crossword1 = Crossword()
#
#
# print(crossword1.CheckIfCorrect())
