import tkinter as tk
import Crosswordview
from LoginFrame import loginPage
from TestFrame2 import testpage2
from LoginEntryWindow import LoginEntryWindow
class MainApp(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self)
        container.pack()
        self.geometry('600x600')
        self.username = ''
        self.frames = {}
        for F in [loginPage,testpage2,LoginEntryWindow]:
            frame = F(container,self)       #Instancing each frame !
            self.frames[F.__name__] = frame
            frame.grid(row=0,column=0,sticky='nsew')

        self.show_frame('loginPage')
    def show_frame(self,nextframe):
        frame = self.frames[nextframe]
        frame.tkraise()
    def SwitchUser(self,name):
        self.username = name



app = MainApp()
app.mainloop()
app.SwitchUser('Joe Crawley !')