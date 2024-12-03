import tkinter as tk
from tkinter import ttk

#Create the class
class mainMenuFrame(tk.Frame):
    #Initialise the class
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent = parent

        #Widgets
        login_button = ttk.Button(self, text='Log in', command=lambda:self.controller.showFrame('loginEntryFrame','300x400','Log in'))
        login_button.grid(row=2,column=0)

        guest_button = ttk.Button(self, text='Play as Guest', command=lambda:self.controller.showFrame('choiceFrame','','What to play'))
        guest_button.grid(row=2,column=2)


        welcome_label = ttk.Label(self, text='Welcome', font=('Georgia', 50))
        welcome_label.grid(row=1, column=1)