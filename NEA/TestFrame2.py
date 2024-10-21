import tkinter as tk

class testpage2(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent = parent

        label = tk.Label(self,text='FRAME 2 HELLO !!!')
        label.grid()

        Button1 = tk.Button(self, text='switch frame', command=lambda: self.controller.show_frame('loginPage'))
        Button1.grid(row=1)
