from crypt import methods
from flask import Flask,request,jsonify
from bs4 import BeautifulSoup
import json
import requests
from tkinter import *


app = Flask(__name__)

#In API's we have types of requests

#The ones we care about are GET and POST

#GET is getting something quickly

#POST is giving some data to the server in exchange for some more (sometimes)

#Tasks

#Research flask API's understand what a POST method is

#Implement a login through your API (simple if statements for now, SQL later)

#My first endpoint (Where someone gets something)


@app.route('/GenerateCells',methods=['GET'])
def crossword():

    genericUrl = "https://www.theguardian.com/crosswords/quick/"
    code = "16992"
    url = genericUrl + code


    cells = {}


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


            position = str(row) + str(col)
            cells[position] = {'text':obj}



    cellsBelongingToWord(jsonified,cells)
    return cells


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
                text = cell.get('text')

                if text == "⬛":
                    cell['text'] = "--"

                elif text == "S":
                    pass

                else:
                    cell['text'] = "□"


        else:
            for n in range(1, length):
                position = str(posY + n) + str(posX)
                cell = cells.get(position)
                text = cell.get('text')


                if text == "⬛":
                    cell['text'] = "|"

                elif text == "S":
                    pass

                else:
                    cell['text'] = "□"


app.run(debug=True)








