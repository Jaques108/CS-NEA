import requests
from bs4 import BeautifulSoup
import json

from tkinter import *


app = Tk()
app.geometry("400x400")
app.title('Main Menu')
app.resizable(width=FALSE,height=FALSE)



def login():


    loginWin = Toplevel(app)
    loginWin.geometry("300x200")
    loginWin.resizable(width=FALSE, height=FALSE)

    userNameEntry = Entry(loginWin)
    userNameEntry.place(relx = 0.6, rely =0.2,anchor = CENTER)

    userLabel = Label(loginWin, text = 'Username')
    userLabel.place(relx = 0.15,rely = 0.2,anchor = CENTER)

    passEntry = Entry(loginWin)
    passEntry.place(relx=0.6, rely=0.5, anchor=CENTER)

    passLabel = Label(loginWin, text='Password')
    passLabel.place(relx = 0.15,rely = 0.5,anchor = CENTER)

    def check():
        user = userNameEntry.cget(key="text")
        password = passEntry.cget(key="text")

    def cont():
        if user == "" or password == "":
            pass

        else:
            loginWin.destroy()
            sudoku()

    playButton = Button(loginWin, text = 'Play', command = cont)
    playButton.place(relx = 0.5, rely = 0.75,anchor = CENTER)

    for widget in loginWin.winfo_children():
        widget.config(font='Georgia')




def sudoku():

    playWinSudoku = Tk()
    playWinSudoku.title("Sudoku")
    playWinSudoku.resizable(width=FALSE, height=FALSE)
    playWinSudoku.geometry("350x335")


    valid = (playWinSudoku.register(validate_entry), '%P')
    for row in range(9):
        for col in range(9):
            entry = Entry(playWinSudoku, width=2, validate='key', validatecommand=valid,justify = 'center')
            entry.grid(row=row, column=col, padx=4, pady=4)

    playWin.mainloop()




def crossword():

    def submit():
        number = urlEntry.cget(key = "text")


    playWinCrossword = Tk()
    playWinCrossword.title("Crossword")
    playWinCrossword.resizable(width=FALSE,height=FALSE)

    genericUrl = "https://www.theguardian.com/crosswords/quick/"

    # Label1 = Label(playWinCrossword, text="Enter crossword number #")
    # Label1.place(relx=0.5, rely=0.075, anchor=CENTER)
    #
    # urlEntry = Entry(playWinCrossword)
    # urlEntry.place(relx = 0.5,rely = 0.25,anchor = CENTER)
    #
    # submitButton = Button(playWinCrossword,text = "Submit",command = submit)
    # submitButton.place(relx = 0.5,rely = 0.45,anchor = CENTER)



    #Label2 = Label(playWinCrossword, text="----------------------------------")
    #abel2.place(relx=0.5, rely=0.575, anchor=CENTER)

    #randomButton = Button(playWinCrossword,text = "Random",command = random)
    #randomButton.place(relx= 0.5,rely = 0.80,anchor = CENTER)





    # play = False
    #
    # while not play:
    #     cont = input("yes? ")
    #
    #     if cont == "yes":
    #         play = True

    # cells = []
    #
    # for row in range(13):
    #     for col in range(13):
    #         cell = Label(playWinCrossword, text="⬛", justify='center')
    #         cell.grid(row=row, column=col, padx=4, pady=4)
    #
    #         cells.append([cell,[row,col]])


    url = genericUrl + '16993'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.find_all("div", {"class": "js-crossword"})
    test = (mydivs[0].get('data-crossword-data'))


    jsonified = json.loads(test)
    startPositions = []

    seen = set()
    for item in jsonified['entries']:
        temp = item['position']
        tempX = temp['x']
        tempY = temp['y']

        startPosition = (tempX,tempY)

        #Removes duplicates. This is because some start positions belong to both across and down words.
        if startPosition not in seen:
            startPositions.append(startPosition)
            seen.add(startPosition)


        startPositions = sorted(startPositions, key=lambda x: (x[1], x[0]))


    length = len(startPositions) - 1


    x = 0
    for row in range(13):
        for col in range(13):
            currentStartPos = startPositions[x]
            tempX = startPositions[x][0]
            tempY = startPositions[x][1]

            if col == tempX and row == tempY:
                obj = 'S'

                if x != length:
                    x += 1




            else:
                obj = '⬛'



            cell = Label(playWinCrossword, text=obj, justify='center')
            cell.grid(row=row, column=col, padx=4, pady=4)






    #Writes an S where we need to start !
    # for item in jsonified['entries']:
    #     temp = item['position']
    #     tempX = temp['x']
    #     tempY = temp['y']
    #     for i in range(len(cells)):
    #         pos = cells[i][1]
    #         posY = pos[0]
    #         posX = pos[1]
    #
    #         if (posX == tempX) and (posY == tempY):
    #             cell = cells[i][0]
    #             cell.config(text = "S")
    #
    #             if item['direction'] == 'across':
    #                 Length = item['length']
    #                 for x in range(1,Length):
    #                     cell = cells[i+x][0]
    #                     cell.config(text = "--")
    #
    #             if item['direction'] == 'down':
    #                 Length = item['length']
    #                 n = 13
    #                 for _ in range(1,Length):
    #                     cell = cells[i + n][0]
    #
    #                     text = cell.cget(key="text")
    #                     if text == "S":
    #                         pass
    #
    #                     elif text == "--":
    #                         cell.config(text="□")
    #
    #                     else:
    #                         cell.config(text="|")
    #
    #                     n += 13
    #
    #             break
    # playWinCrossword.mainloop()







        #Make input cells different character  (-)!
        # if item['direction'] == 'across':
        #     Length = item['length']
        #     for i in range(1,Length):
        #         self.grid[tempY][tempX+i] = '-'
        # elif item['direction'] == 'down':
        #     Length = item['length']
        #     for i in range(1,Length):
        #         self.grid[tempY+i][tempX] = '|'






def choose():
    app.destroy()

    chooseWin = Tk()
    chooseWin.geometry("400x150")
    chooseWin.title("What to play")

    sudokuButton = Button(chooseWin,text = "Sudoku",command = sudoku, width=20,height=20)
    sudokuButton.place(relx = 0.25,rely = 0.5,anchor = CENTER)

    crosswordsButton = Button(chooseWin, text="Crossword", command = crossword, width=20, height=20)
    crosswordsButton.place(relx=0.75, rely=0.5, anchor=CENTER)








login_button = Button(app, text = 'Log in',command = login)
login_button.place(relx = 0.5,rely = 0.6, anchor = CENTER)

guest_button = Button(app, text = 'Play as Guest',command = choose)
guest_button.place(relx = 0.5, rely = 0.8, anchor = CENTER)


for widget in app.winfo_children():
    widget.config(font = ('Georgia', 30))


welcome_label = Label(app,text = 'Welcome',font = ('Georgia', 50))
welcome_label.place(relx = 0.5,rely = 0.2, anchor = CENTER)






#To make it so that the only thing a user can input is a number and only 1 number max

def validate_entry(char_input):
    if len(char_input) <= 1 and char_input.isdigit() or char_input == "":
        return True
    else:
        return False





app.mainloop()









#We want to obtain crosswords for our game

#Users like guardian crosswords

#Because you did a survey and guardian was best

#So to source their crosswords we can either manually input data into our applciation and use this however this is time consuming

#Another option is to source this data from the guardian website via web-scraping.

#This is quicker and allows to use a vast collection of crosswords.

#DESIGN

#A cross word is gridlike data and therefore can be presented using a 2D List,

#Crosswords have grids where users can enter answers to clues as well as a display for clues.

#Mockup design of crossword
