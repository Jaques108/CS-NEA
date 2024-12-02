from click import password_option
from flask import Flask,request,jsonify
from bs4 import BeautifulSoup
import json
import requests
import random
import hashlib
import jwt
import datetime
from sqlite3 import Error

from soupsieve import select

from SQLBackEnd import SQLBackEnd



SQL = SQLBackEnd('main.db')

Crossword = Flask(__name__)


@Crossword.route('/CreateUser',methods = ['POST'])
def createUser():
    data = requests.get_json()
    username = data['username']
    password = data['password'].encode('utf-8')
    passwordHash = hashlib.sha256(password).hexdigest()


    SQL.connect()
    insertUser = 'INSERT INTO users (username,password) VALUES (?,?)'
    e = SQL.executeQuery(insertUser, [username, passwordHash])
    SQL.closeConnection()

    if isinstance(e,'Error'):
        return jsonify('Error',e),400



    return jsonify({'message': 'User created successfully'}),201


@Crossword.route('/Login',methods = ['POST'])
def login():
    data = requests.get_json()
    username = data['username']
    password = data['password'].encode('utf-8')
    passwordHash = hashlib.sha256(password).hexdigest()

    selectQuery = 'SELECT * FROM users WHERE username = ? AND password = ?'
    SQL.connect()
    user = SQL.executeQuery(selectQuery,[username,passwordHash])













#In API's we have types of requests

#The ones we care about are GET and POST

#GET is getting something quickly

#POST is giving some data to the server in exchange for some more (sometimes)

#Tasks

#Research flask API's understand what a POST method is

#Implement a login through your API (simple if statements for now, SQL later)

#My first endpoint (Where someone gets something)

@Crossword.route('/GenerateCells/<code>',methods=['GET'])
def crossword(code):

    genericUrl = "https://www.theguardian.com/crosswords/quick/"
    url = genericUrl + code
    cells = {}
    clues = []


    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.find_all("div", {"class": "js-crossword"})
    test = (mydivs[0].get('data-crossword-data'))

    jsonified = json.loads(test)




    startPositions = []
    seen = set()


    for item in jsonified['entries']:
        temp = item['position']

        clue = item['clue']
        direction = item['direction']
        numberList = (item['group'])[0]
        if numberList[1] == '-':
            number = int(numberList[0])

        else:
            number = int(numberList[:2])



        tempX = temp['x']
        tempY = temp['y']



        startPosition = (tempX, tempY)

        # Removes duplicates. This is because some start positions belong to both across and down words.
        if startPosition not in seen:
            startPositions.append(startPosition)
            seen.add(startPosition)


            clue = (clue,number,direction)
            clues.append(clue)





        startPositions = sorted(startPositions, key=lambda x: (x[1], x[0]))

    length = len(startPositions) - 1

    x = 0
    for row in range(13):
        for col in range(13):
            obj = "B"

            position = str(row).zfill(2) + str(col).zfill(2)
            cells[position] = {'text':obj}



    cellsBelongingToWord(jsonified,cells)
    result = {
        "cells": cells,
        "clues": clues
    }


    return result


def cellsBelongingToWord(var,cells):
    for item in var['entries']:
        temp = item['position']
        posX = temp['x']
        posY = temp['y']

        number = item['number']

        direction = item['direction']
        length = item['length']


        if direction == 'across':
            for x in range(length):
                position = str(posY).zfill(2) + str(posX + x).zfill(2)
                cell = cells.get(position)
                text = cell.get('text')

                if x == 0:
                    cell['text'] = number


                elif text == "B":
                    cell['text'] = "--"

                elif text == "S":
                    pass

                elif text == '|':
                    cell['text'] = "W"





        elif direction == 'down':
            for n in range(length):
                position = str(posY + n).zfill(2) + str(posX).zfill(2)
                cell = cells.get(position)
                text = cell.get('text')

                if n == 0:
                    cell['text'] = number


                elif text == "B":
                    cell['text'] = "|"

                elif text == "S":
                    pass

                elif text == '--':
                    cell['text'] = "W"



Crossword.run(debug=True)