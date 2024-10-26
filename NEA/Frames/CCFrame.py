from tkinter import *
from tkinter import ttk
from NEA.Frames.CrosswordFrame import crosswordFrame
import requests
import json




class ccFrame(ttk.Frame):
    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent)
        self.parent = parent
        self.controller = controller


        def submit():
            code = codeEntry.get()
            if code == '':
                return False

            self.controller.show_frame('crosswordFrame', '', 'Crossword')

            def getCrosswordData():
                url = f'http://127.0.0.1:5000/GenerateCells/{code}'
                webResponse = requests.get(url)
                dictData = webResponse.json()


                afile = open('Code.txt', 'w')
                json.dump(dictData, afile, indent=4)
                afile.close()



            getCrosswordData()
            crosswordFrame.displayData(self)





        codeLabel = ttk.Label(self,text = 'Enter Crossword Code')
        codeLabel.place(relx = 0.5,rely = 0.25,anchor = CENTER)

        codeEntry = ttk.Entry(self,justify='center')
        codeEntry.place(relx = 0.5,rely = 0.5,anchor = CENTER)

        codeSubmit = ttk.Button(self,text = 'Submit',command = submit)
        codeSubmit.place(relx = 0.5,rely = 0.8,anchor = CENTER)










