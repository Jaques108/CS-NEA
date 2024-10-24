import requests
from bs4 import BeautifulSoup
import json

from tkinter import *


app = Tk()
app.geometry("400x400")
app.title('Main Menu')
app.resizable(width=FALSE,height=FALSE)





def crossword():
    playWinCrossword = Tk()
    playWinCrossword.title("Crossword")
    playWinCrossword.resizable(width=FALSE,height=FALSE)

    genericUrl = "https://www.theguardian.com/crosswords/quick/"


    cells = {}

    code = "16994"
    url = genericUrl + code

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

        startPosition = (tempX, tempY)

        # Removes duplicates. This is because some start positions belong to both across and down words.
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

            position = str(row) + str(col)
            cells[position] = cell



    cellsBelongingToWord(jsonified,cells)





def cellsBelongingToWord(var,cells):
    for item in var['entries']:
        temp = item['position']
        posX = temp['x']
        posY = temp['y']

        direction = item['direction']
        length = item['length']


        if direction == 'across':
            for x in range(1, length):
                position = str(posY) + str(posX + x)
                cell = cells.get(position)

                text = cell.cget(key="text")

                if text == "⬛":
                    cell.config(text="--")

                elif text == "S":
                    pass

                else:
                    cell.config(text="□")


        else:
            for n in range(1, length):
                position = str(posY + n) + str(posX)
                cell = cells.get(position)
                text = cell.cget(key="text")

                if text == "⬛":
                    cell.config(text = '|')

                elif text == "S":
                    pass

                else:
                    cell.config(text="□")







play = Button(app,text = 'play',command = crossword)
play.pack()


app.mainloop()






