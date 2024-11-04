from tkinter import *
from tkinter import ttk
import requests
import json


class crosswordFrameNew(ttk.Frame):
    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent)
        self.parent = parent
        self.controller = controller

        self.tiles = []


        self.clueFrame = Frame(self,bd=0,relief = 'solid')
        self.clueFrame.pack(side=LEFT,fill = Y,padx=20,pady=50)


        self.puzzle_frame = Frame(self,bd=0,relief='solid')
        self.puzzle_frame.pack(side=RIGHT,fill=BOTH,expand=True,padx=0,pady=50)

        self.AcrossLabel = Label(self.clueFrame, text="Across", font='Arial 16 bold').grid(row=0, column=0, sticky="nw")

        self.DownLabel = Label(self.clueFrame, text="Down", font='Arial 16 bold').grid(row=0, column=1, sticky="nw")