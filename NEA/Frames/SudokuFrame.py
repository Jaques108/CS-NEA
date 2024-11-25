from tkinter import *
from functools import partial
import re

from packaging.utils import canonicalize_version
from soupsieve import select


class sudokuFrame(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.parent = parent
        self.controller = controller



    def createGrid(self):
        self.textIDs = {}
        cellSize = 40
        canvasSize = 40 * 9

        canvas = Canvas(self, width=canvasSize, height=canvasSize)
        canvas.pack()
        canvas.focus_set()




        for row in range(9):
            for col in range(9):
                x1 = col * cellSize
                y1 = row * cellSize
                x2 = x1 + cellSize
                y2 = y1 + cellSize

                xCenter = (x1 + x2) / 2
                yCenter = (y1 + y2) / 2


                rectangleID = canvas.create_rectangle(x1,y1,x2,y2,fill="white", outline="black")
                textID = canvas.create_text(xCenter, yCenter, text='', font=("Arial", 16), fill="black", tags='text')
                self.textIDs[rectangleID] = textID

                canvas.tag_bind(rectangleID, "<Enter>", partial(self.mouseEnter, canvas, rectangleID))
                canvas.tag_bind(rectangleID, "<Leave>", partial(self.mouseExit, canvas, rectangleID))
                canvas.tag_bind(rectangleID, "<Button-1>",partial(self.onClick,canvas,rectangleID))

                canvas.bind('<Key>', partial(self.enterText, canvas))

        self.submitButton = Button(self, text='submit',command = partial(self.canvas2array,canvas))
        self.submitButton.pack()


    def mouseEnter(self,canvas, rectangleID, event):
        try:

            if rectangleID != self.selectedRectangleID:
                canvas.itemconfig(rectangleID, fill="grey")
        except:
            pass

    def mouseExit(self,canvas, rectangleID, event):
        try:

            if rectangleID != self.selectedRectangleID:
                canvas.itemconfig(rectangleID, fill="white")
        except:
            pass


    def onClick(self,canvas,rectangleID,event):
        try:
            canvas.itemconfig(self.selectedRectangleID,fill = 'white')

        except:
            pass
        self.selectedRectangleID = rectangleID
        self.selectedTextID = self.textIDs[rectangleID]
        canvas.itemconfig(rectangleID, fill="#ADD8E6")






    def enterText(self,canvas,event):
        pattern = r'\d'
        char = event.keysym.upper()
        match = re.match(pattern,char)
        match = bool(match)

        if match:
            canvas.itemconfig(self.selectedTextID,text = char)



    def canvas2array(self,canvas):
        grid = [[''for x in range(9)]for y in range(9)]
        print(grid)

        for i in range(2,163,2):
            print(i,canvas.itemcget(i, 'text'))

















