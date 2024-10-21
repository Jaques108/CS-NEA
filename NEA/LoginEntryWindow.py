from tkinter import ttk
import tkinter as tk
class LoginEntryWindow(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent = parent

        userNameEntry = ttk.Entry(self)
        userNameEntry.grid(row=1,column=1)

        userLabel = ttk.Label(self, text='Username')
        userLabel.grid(row=1,column=0)

        passEntry = ttk.Entry(self)
        passEntry.grid(row=2,column=1)

        passLabel = ttk.Label(self, text='Password')
        passLabel.grid(row=2,column=0)

        playButton = ttk.Button(self, text='Play', command=lambda:print('PLay Clicked !'))
        playButton.grid(row=3, column=1)