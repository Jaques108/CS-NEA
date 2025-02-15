import tkinter as tk

#Import our frames
from NEA.Frames.MainMenu import mainMenuFrame
from NEA.Frames.LoginEntryFrame import loginEntryFrame
from NEA.Frames.ChoiceFrame import choiceFrame
from NEA.Frames.SudokuFrame import sudokuFrame
from NEA.Frames.CrosswordFrame import crosswordFrame
from NEA.Frames.SuccessFrame import successFrame
from NEA.Frames.InstructionsFrame import instructionsFrame





#Create the class
class MainApp(tk.Tk):
    #Initialise the class
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #Use this for the login system
        self.username = None

        #Create the tkinter window
        container = tk.Frame(self)
        container.pack()

        #Dictionary to store each of the frames
        self.frames = {}


        #Iterating through the frames
        for F in [mainMenuFrame, loginEntryFrame, choiceFrame, sudokuFrame, crosswordFrame,instructionsFrame,successFrame]:

            #Instancing each frame!
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        #Show the main menu frame using the showFrame function
        self.showFrame('mainMenuFrame', '800x400', 'Main Menu')




    #Create a function which displays a specified frame
    def showFrame(self, nextframe,size,title):
        #Frame is a varible which stores the next frame to be displayed
        frame = self.frames[nextframe]

        #Set attributes
        self.geometry(size)
        self.title(title)
        self.resizable(width=False, height=False)
        frame.grid(row=0, column=0, sticky="nsew")

        #Raise the frame
        frame.tkraise()


#Run the whole thing
app = MainApp()
app.mainloop()