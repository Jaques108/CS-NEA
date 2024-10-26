from flask import Flask,request,jsonify
from bs4 import BeautifulSoup
import json
import requests



app = Flask(__name__)

#In API's we have types of requests

#The ones we care about are GET and POST

#GET is getting something quickly

#POST is giving some data to the server in exchange for some more (sometimes)

#Tasks

#Research flask API's understand what a POST method is

#Implement a login through your API (simple if statements for now, SQL later)

#My first endpoint (Where someone gets something)




@app.route('/GenerateCells/<code>',methods=['GET'])
def crossword(code):
    genericUrl = "https://www.theguardian.com/crosswords/quick/"

    if code.isdigit():
        url = genericUrl + code

    else:
        return 'Invalid Code'


    cells = {}


    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        mydivs = soup.find_all("div", {"class": "js-crossword"})
        test = (mydivs[0].get('data-crossword-data'))

        jsonified = json.loads(test)

    except:
        return "Code doesn't exist"




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
            obj = "B"

            position = str(row).zfill(2) + str(col).zfill(2)
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
            for x in range(0,length):
                position = str(posY).zfill(2) + str(posX + x).zfill(2)
                cell = cells.get(position)
                text = cell.get('text')

                if x == 0:
                    cell['text'] = 'S'

                elif text == "B":
                    cell['text'] = "--"

                elif text == "S":
                    pass

                else:
                    cell['text'] = "W"


        elif direction == 'down':
            for n in range(0,length):
                position = str(posY + n).zfill(2) + str(posX).zfill(2)
                cell = cells.get(position)
                text = cell.get('text')

                if x == 0:
                    cell['text'] = 'S'

                elif text == "B":
                    cell['text'] = "|"

                elif text == "S":
                    pass

                else:
                    cell['text'] = "W"




app.run(debug=True)








