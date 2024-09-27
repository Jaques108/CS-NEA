import tkinter as tk
import Crosswordview


class MainApp(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self)
        container.pack()
        self.username = ''
        self.frames = {}
        for F in [Crosswordview.Crossword]:
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column=0,sticky='nsew')
    def show_frame(self,nextframe):
        frame = self.frames[nextframe]
        frame.tkraise()
    def SwitchUser(self,name):
        self.username = name

app = MainApp()
app.mainloop()
app.SwitchUser('Joe Crawley !')