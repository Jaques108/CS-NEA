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
        afile = open('Code.txt', 'r')
        data = json.load(afile)

        for cellID, cellData in data.items():
            posX = int(cellID[2:])
            posY = int(cellID[:2])

            obj = cellData.get("text")

            cell = ttk.Label(self,text =obj)
            cell.grid(column = posX,row = posY)

