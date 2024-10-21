import tkinter as tk
from tkinter import ttk
class loginPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent = parent

        # label = ttk.Label(self,text='TEST HELLO WORLD !!!!!')
        # label.grid(row=0)


        # Button1 = ttk.Button(self,text='switch frame',command=lambda:self.controller.show_frame('testpage2'))
        # Button1.grid(row=1)

        login_button = ttk.Button(self, text='Log in', command=lambda:self.controller.show_frame('LoginEntryWindow'))
        login_button.grid(row=2,column=1)

        guest_button = ttk.Button(self, text='Play as Guest', command=lambda:print('hello'))
        guest_button.grid(row=2,column=2)

        # for widget in app.winfo_children():
        #     widget.config(font=('Georgia', 30))

        welcome_label = ttk.Label(self, text='Welcome', font=('Georgia', 50))
        welcome_label.grid(row=1, column=1)
