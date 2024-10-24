from crypt import methods

from flask import Flask,request,jsonify


app = Flask(__name__)

#In API's we have types of requests

#The ones we care about are GET and POST

#Get is getting something quickly

#POST is giving some data to the server in exchange for some more (sometimes)

#Tasks

#Research flask API's understand what a POST method is

#Implement a login through your API (simple if statements for now, SQL later)

@app.route('/fun')     #My first endpoint (Where someone gets something)
def hello_world():
    return 'hello world !'

@app.route('/login',methods=['POST'])
def login():

    if password =='Password123':
        return True
    #Do this !
    pass
@app.route('/Multiplyby5',methods=['GET'])
def Multiply():
    data_id = request.args.get('input')
    if data_id:
        return f'{int(data_id) * 5}'
    else:
        return 'no data !'
app.run(debug=True)




@app.route('/GenerateCells',methods=['POST'])
def generateCells(code):
    cells = []
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

        startPosition = [tempX, tempY]

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
            cells.append(cell)


    cellsBelongingToWord()

    return cells






def cellsBelongingToWord():
    for item in startPositions:
        pos = startPositions[item]
        posY = pos[0]
        posX = pos[1]

        direction = item['direction']
        length = item['length']

        if direction == 'across':
            for x in range(1, length):
                cell = cells[i + x][0]
                text = cell.cget(key="text")

                if text == "S":
                    pass

                elif text == "|":
                    cell.config(text="□")

                else:
                    cell.config(text="--")


        else:
            for n in range(1, (Length * 13), 13):
                cell = cells[i + n][0]
                text = cell.cget(key="text")

                if text == "S":
                    pass

                elif text == "--":
                    cell.config(text="□")

                else:
                    cell.config(text="|")


        break

