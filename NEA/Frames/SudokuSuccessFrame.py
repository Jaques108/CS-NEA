from tkinter import *

#Create the class
class sudokuSuccessFrame(Frame):
    #Initialise the class
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.pack_propagate(False)  # Prevent resizing based on widgets


        self.successLabel = Label(self,text = 'Well Done my g')
        self.successLabel.pack()






