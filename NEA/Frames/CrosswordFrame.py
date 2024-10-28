from tkinter import *
from tkinter import ttk
import requests
import json





class crosswordFrame(ttk.Frame):
    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent)
        self.parent = parent
        self.controller = controller


        def submit():
            code = codeEntry.get()
            url = f'http://127.0.0.1:5000/GenerateCells/{code}'
            dictData = None

            try:
                webResponse = requests.get(url, timeout=5)  #Add a timeout to prevent indefinite waiting

                if webResponse != 200:  #Check if response is successful
                    errorLabel.config(text='Error - Code not accepted. Try again.')

                else:
                    dictData = webResponse.json()


            except requests.exceptions.RequestException as e:
                #Handle network errors, timeouts, etc.
                errorLabel.config(text=f'Connection Error: {e}. Please try again.')

            if dictData == None:
                pass

            else:
                def getCrosswordData():
                    afile = open('Code.txt', 'w')
                    json.dump(dictData, afile, indent=4)
                    afile.close()

                getCrosswordData()
                displayData()



                def displayData():
                    codeLabel.destroy()
                    codeEntry.destroy()
                    codeSubmit.destroy()
                    errorLabel.destroy()

                    afile = open('Code.txt', 'r')
                    data = json.load(afile)
                    self.cells = []

                    for cellID, cellData in data.items():
                        posX = int(cellID[2:])
                        posY = int(cellID[:2])

                        obj = cellData.get("text")

                        cell = ttk.Label(self, text=obj)
                        cell.grid(column=posX, row=posY,padx=10,pady=10)

                        self.cells.append(cell)











        codeLabel = ttk.Label(self,text = 'Enter Crossword Code')
        codeLabel.place(relx = 0.5,rely = 0.25,anchor = CENTER)

        codeEntry = ttk.Entry(self,justify='center')
        codeEntry.place(relx = 0.5,rely = 0.5,anchor = CENTER)

        codeSubmit = ttk.Button(self,text = 'Submit',command = submit)
        codeSubmit.place(relx = 0.5,rely = 0.8,anchor = CENTER)

        errorLabel = ttk.Label(self)
        errorLabel.place(relx=0.5, rely=0.65, anchor=CENTER)










