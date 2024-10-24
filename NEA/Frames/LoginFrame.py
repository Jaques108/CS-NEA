import tkinter as tk
from tkinter import ttk

class loginFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent = parent


        login_button = ttk.Button(self, text='Log in', command=lambda:self.controller.show_frame('loginEntryWindow','300x400','Log in'))
        login_button.grid(row=2,column=1)

        guest_button = ttk.Button(self, text='Play as Guest', command=lambda:self.controller.show_frame('choiceFrame','','What to play'))
        guest_button.grid(row=2,column=2)


        welcome_label = ttk.Label(self, text='Welcome', font=('Georgia', 50))
        welcome_label.grid(row=1, column=1)
