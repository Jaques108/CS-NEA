from tkinter import *
from tkinter import ttk
import json
import requests
from functools import partial

class crosswordFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        def submit():
            code = codeEntry.get()
            url = f'http://127.0.0.1:5000/GenerateCells/{code}'
            dictData = None

            try:
                webResponse = requests.get(url, timeout=7)

                if webResponse.status_code != 200:
                    errorLabel.config(text='Error - Code not accepted. Try again.')
                else:
                    dictData = webResponse.json()

            except requests.exceptions.RequestException as e:
                errorLabel.config(text=f'Connection Error: {e}. Please try again.')

            if dictData is None:
                pass
            else:
                def getCrosswordData():
                    with open('Code.txt', 'w') as afile:
                        json.dump(dictData, afile, indent=4)

                getCrosswordData()

                def displayData():
                    codeLabel.destroy()
                    codeEntry.destroy()
                    codeSubmit.destroy()
                    errorLabel.destroy()

                    cellSize = 40
                    canvasSize = 40 * 13

                    canvas = Canvas(self, width=canvasSize, height=canvasSize)
                    canvas.pack()

                    with open('Code.txt', 'r') as afile:
                        data = json.load(afile)

                    for cellID, cellData in data.items():
                        posX = int(cellID[2:])
                        posY = int(cellID[:2])

                        x1 = posX * cellSize
                        y1 = posY * cellSize
                        x2 = x1 + cellSize
                        y2 = y1 + cellSize

                        obj = cellData.get("text")

                        if obj == 'B':
                            rectangleID = canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
                            canvas.tag_bind(rectangleID, "<Button-1>", partial(onClick, canvas, rectangleID))

                        else:
                            rectangleID = canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                            canvas.tag_bind(rectangleID, "<Button-1>", partial(onClick, canvas, rectangleID))

                displayData()

        def onClick(canvas, rectangleID, event):
            coords = canvas.coords(rectangleID)
            textTag = f"text_{rectangleID}"

            if coords[0] < event.x < coords[2] and coords[1] < event.y < coords[3]:
                canvas.delete(textTag)
                canvas.create_text((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2,text="K", font=("Arial", 24), tags=textTag)

        # UI Elements
        codeLabel = ttk.Label(self, text='Enter Crossword Code')
        codeLabel.place(relx=0.5, rely=0.25, anchor="center")

        codeEntry = ttk.Entry(self)
        codeEntry.place(relx=0.5, rely=0.5, anchor="center")

        codeSubmit = ttk.Button(self, text='Submit', command=submit)
        codeSubmit.place(relx=0.5, rely=0.8, anchor="center")

        errorLabel = ttk.Label(self)
        errorLabel.place(relx=0.5, rely=0.65, anchor="center")