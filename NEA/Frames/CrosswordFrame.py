from tkinter import *
from tkinter import ttk
import requests
import json



class crosswordFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

    def displayData(self):
        afile = open('/Users/jake/main/NEA/Frames/Code.txt', 'r')
        data = json.load(afile)

        for key, value in data.items():
            text = value.get('text')
            print(text)
