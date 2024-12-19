from tkinter import *

#Create the class
class crosswordSuccessFrame(Frame):
    #Initialise the class
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.pack_propagate(False)  # Prevent resizing based on widgets


        self.successLabel = Label(self,text = 'Well Done my g')
        self.successLabel.place(relx = 0.5,rely = 0.5,anchor = 'center')
