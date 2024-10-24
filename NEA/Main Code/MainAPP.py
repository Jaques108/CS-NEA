import tkinter as tk
from NEA.Frames.LoginFrame import loginFrame
from NEA.Frames.TestFrame2 import testpage2
from NEA.Frames.LoginEntryFrame import loginEntryFrame
from NEA.Frames.ChoiceFrame import choiceFrame
from NEA.Frames.SudokuFrame import sudokuFrame



class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()
        self.geometry('600x600')
        self.username = ''
        self.frames = {}
        self.show_frame('loginPage','600x600','Welcome')

        for F in [loginPage, testpage2, loginEntryFrame,choiceFrame,sudokuFrame]:
            frame = F(container, self)  #Instancing each frame !
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky='nsew')




    def show_frame(self, nextframe,size,title):
        frame = self.frames[nextframe]
        frame.winfo_geometry(size)
        frame.title(title)
        frame.tkraise()

    def SwitchUser(self, name):
        self.username = name


app = MainApp()
app.mainloop()
