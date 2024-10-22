from flask import Flask,request,jsonify


app = Flask(__name__)

#In API's we have types of requests

#The ones we care about are GET and POST

#Get is getting something quickly

#POST is giving some data to the server in exchange for some more (sometimes)

#Tasks

#Research flask API's understand what a POST method is

#Implement a login through your API (simple if statements for now, SQL later)

@app.route('/')     #My first endpoint (Where someone gets something)
def hello_world():
    return 'hello forld !'
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



startPositions = []


for item in jsonified['entries']:
    temp = item['position']
    startPositions.append(temp)


for row in range(13):
    for col in range(13):
        for i in range(len(startPositions)):
            startPositions[i][0] = tempX
            startPositions[i][1] = tempY

            if row == tempX and col == tempY:
                obj = 'S'


            cell = Label(playWinCrossword, text= obj, justify='center')
            cell.grid(row=row, column=col, padx=4, pady=4)















url = genericUrl + '16978'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

mydivs = soup.find_all("div", {"class": "js-crossword"})
test = (mydivs[0].get('data-crossword-data'))

jsonified = json.loads(test)

# Writes an S where we need to start !
for item in jsonified['entries']:
    temp = item['position']
    tempX = temp['x']
    tempY = temp['y']
    for i in range(len(cells)):
        pos = cells[i][1]
        posY = pos[0]
        posX = pos[1]

        if (posX == tempX) and (posY == tempY):
            cell = cells[i][0]
            cell.config(text="S")

            if item['direction'] == 'across':
                Length = item['length']
                for x in range(1, Length):
                    cell = cells[i + x][0]
                    cell.config(text="--")

            if item['direction'] == 'down':
                Length = item['length']
                n = 13
                for _ in range(1, Length):
                    cell = cells[i + n][0]

                    text = cell.cget(key="text")
                    if text == "S":
                        pass

                    elif text == "--":
                        cell.config(text="□")

                    else:
                        cell.config(text="|")

                    n += 13

            break
playWinCrossword.mainloop()