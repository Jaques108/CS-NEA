import tkinter as tk
from NEA.Frames.LoginFrame import loginFrame
from NEA.Frames.LoginEntryFrame import loginEntryFrame
from NEA.Frames.ChoiceFrame import choiceFrame
from NEA.Frames.SudokuFrame import sudokuFrame



class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.username = None
        container = tk.Frame(self)
        container.pack()
        self.frames = {}


        for F in [loginFrame, loginEntryFrame,choiceFrame,sudokuFrame]:
            frame = F(container, self)  #Instancing each frame!
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('loginFrame', '600x600', 'Welcome')




    def show_frame(self, nextframe,size,title):
        frame = self.frames[nextframe]
        self.geometry('')
        self.resizable(width = False,height = False)
        
        #Have the option for the application to auto-set the geometry
        if size == '':
            pass
        else:
            self.geometry(size)
        
        self.title(title)
        frame.tkraise()

    def SwitchUser(self, name):
        self.username = name


app = MainApp()
app.mainloop()
