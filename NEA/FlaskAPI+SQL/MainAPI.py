from flask import Flask,request,jsonify
from bs4 import BeautifulSoup
from sqlite3 import Error
from SQLBackEnd import SQLBackEnd

import json
import requests
import random
import hashlib
import datetime
import copy
import jwt
import secrets
import re




SQL = SQLBackEnd('main.db')

API = Flask(__name__)


@API.route('/CreateUser', methods=['POST'])
def createUser():

    #Get the username and password
    #We do not need to check for validity as it has already been done by the LoginFrame
    data = request.get_json()
    username = data['username']
    password = data['password']



    # Hash the password
    encodedPassword = password.encode('utf-8')
    passwordHash = hashlib.sha256(encodedPassword).hexdigest()

    # Connect to the database and insert the user
    SQL.connect()
    insertUser = 'INSERT INTO users (username, password) VALUES (?, ?)'
    e = SQL.executeQuery(insertUser, [username, passwordHash])
    SQL.closeConnection()

    # Check for errors in insertion
    if isinstance(e, Error):
        return jsonify({'message': f'Error: {str(e)}'}), 400

    return jsonify({'message': 'User created successfully'}), 201








@API.route('/GetUsers', methods = ['GET'])
def getUsers():
    # Connect to the database
    SQL.connect()

    # Define the query to select all users
    query = 'SELECT * FROM users'



    # Execute the query
    result = SQL.executeQuery(query)

    # Close the database connection
    SQL.closeConnection()

    # Check if any users were retrieved
    if result:
        # Return users as JSON
        # The result will be a list of tuples. Convert it into a dictionary if needed
        users = [{"id": user[0], "username": user[1], "password": user[2]} for user in result]
        return jsonify({'users': users}), 200

    else:
        return jsonify({'message': 'No users found'}), 404


@API.route('/DeleteUser/<username>', methods=['DELETE'])
def deleteUser(username):
    # Connect to the database
    SQL.connect()

    if username == '*':
        # Delete all users
        query = 'DELETE FROM users'
        SQL.executeQuery(query)

        # Reset the AUTOINCREMENT index for the users table
        reset_query = "DELETE FROM sqlite_sequence WHERE name='users'"
        SQL.executeQuery(reset_query)

    else:
        # Delete a specific user
        query = 'DELETE FROM users WHERE username = ?'
        SQL.executeQuery(query, [username])

    # Close the database connection
    SQL.closeConnection()
    return jsonify({'message': f'User {username} deleted successfully' if username != '*' else 'All users deleted successfully'}), 200



#Function to log in the user
@API.route('/Login', methods = ['POST'])
def login():
    #Get the data the user has sent
    data = request.get_json()

    #Separate the username and password
    username = data['username']
    password = data['password'].encode('utf-8') #Encode with utf-8 so we can hash it without errors

    #Generate the hash for the password
    passwordHash = hashlib.sha256(password).hexdigest()

    #SQL Query - select the users where username = user input and password = user input
    selectQuery = 'SELECT * FROM users WHERE username = ? AND password = ?'
    #Connect to the database
    SQL.connect()
    #Excute the query and save it in variable user as it will return the user found (if there is one matching inputs)
    user = SQL.executeQuery(selectQuery,[username,passwordHash])
    #Close the connectio
    SQL.closeConnection()

    #Use a string to encode the users auth token
    secretKey = 'idkwhattoputforthis'

    #If we have found a user ->
    if user:
        #Payload is all the data around the user
        payload = {"user": username,  "exp": (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours = 1)).timestamp()}
        #Create our token based on the payload
        token = jwt.encode(payload, secretKey, algorithm='HS256')

        #Write the token to a text file
        afile = open('../Token.txt', 'w')
        afile.write(token)
        afile.close()

        #Return success
        return jsonify({'message': 'Login successful'}), 200

    #If a user is not returned than there is an error in the users inputs
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


#Function for generating the crossword
@API.route('/GenerateCells/<code>', methods=['GET'])
def crossword(code):

    #Using generic url is because every crossword starts off with this url and the only difference
    #is the number that way separating the two allows for greater control of the crossword we want
    genericUrl = "https://www.theguardian.com/crosswords/quick/"
    #Concanatate the url with the number
    url = genericUrl + code

    #Dictionary for our cells and an array for our cluess
    cells = {}
    clues = []
    #List to store cells with a starting number
    startPositions = []

    #Get the response from our url
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    #Parse it with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    #Find all the details relating to our crossword - clues,solutions etc
    fullData = soup.find("gu-island", {"name": "CrosswordComponent"})


    #If the program was not able to get any data return this instead of breaking the program
    if fullData is None:
        return 'No data was returned'

    # Return our data in the variable 'data'
    data = (fullData.get('props'))

    #Get the json data and then return the dictionary 'data' inside our data lol
    jsonified = json.loads(data)['data']



    #Iterate through our clues stored in 'entries'
    for item in jsonified['entries']:
        #Pattern is a variable which we can use in re.sub - it comes from some of the clues still
        #having html elements in them like <i> or <b> -
        #so we use these following lines of code to remove them
        pattern = r'</?(i|span|b)>'
        uncleanClueText = item['clue']
        clue = re.sub(pattern, '', uncleanClueText)

        #Temp holds the position of the cell and direction holds the direction (duh)
        temp = item['position']
        direction = item['direction']

        #This bit is for getting the number of the clue, however we are only given it in the form '3-down' for example.
        #We can use string[0] to get the number which works well except if its a two digit number, so we check if the second
        # char (string[1]) is a dash (meaning its a 1 digit number) and if not then we accommodate for that
        numberList = (item['group'])[0]

        if numberList[1] == '-':
            number = int(numberList[0])

        else:
            number = int(numberList[:2])


        #Find the X and Y coordinates of the clue
        tempX = temp['x']
        tempY = temp['y']

        #Append the position (a tuple) to the startPositions list
        startPosition = (tempX, tempY)
        startPositions.append(startPosition)

        #Do the same with the clues but include their number and direction
        clue = (clue,number,direction)
        clues.append(clue)

        #Sort the startpositions as they are not sorted when we retrieve them
        startPositions = sorted(startPositions, key=lambda x: (x[1], x[0]))


    #Create two for loops to generate our 169 cells
    for row in range(13):
        for col in range(13):
            #Start them all as being black cells or in this case have obj as 'B'
            obj = "B"
            #Variable to tell each cell what clue it belongs to
            wordNumber = None

            #Create their coordinates. We use zfill as we don't want leading 0s to be removed as every coordinates must be 4 chars long eg '0306'
            position = str(row).zfill(2) + str(col).zfill(2)

            #Add the cell to the dictionary with text 'B' and wordNumber None --> we change it later in the program it's just to set it up
            cells[position] = {'text':obj,'wordNumber':wordNumber}



    #Our solution grid will be the result of the function 'createSolutionGrid'.
    #The point of the grid is to have a representation of what the solved grid should look like
    solutionGrid = createSolutionGrid(jsonified,cells)

    #Return all the data we have
    result = {
        "cells": cells,
        "clues": clues,
        "solutionGrid":solutionGrid
    }
    return result


#Now we use our previous setup to differentiate our cells
def createSolutionGrid(var,cells):
    solutionGrid = [[None for x in range(13)] for y in range(13)]

    #Do the same iteration as the previous function - the variable jsonified is passed from the original function
    for item in var['entries']:
        #Variables we need for if a word is across or down so we don't have to write the whole code twice
        across = False
        down = False
        #Variables for the across or down symbols
        defaultChar = None
        inferiorChar = None


        #Find where the x and y coordinates are stored and save in variable temp
        temp = item['position']

        #Find the respective x and y coordinates
        posX = temp['x']
        posY = temp['y']

        #Also retrieve the number of the clue
        number = item['number']

        #Get other details from the clue
        direction = item['direction']
        length = item['length']
        solution = item['solution']

        if direction == 'across':
            across = True
            defaultChar = '--'
            inferiorChar = '|'


        elif direction == 'down':
            down = True
            defaultChar = '|'
            inferiorChar = '--'

        for x in range(length):
            if across:
                #Assign each cell a correct letter based of the string of the clue solution -
                #store this in the array solution grid
                solutionGrid[posY][posX + x] = solution[x]

                #Generate the cell coordinates - using zfill again to retain leading 0s
                position = str(posY).zfill(2) + str(posX + x).zfill(2)


            #Same thing here execept its for down clues
            elif down:
                solutionGrid[posY + x][posX] = solution[x]
                position = str(posY + x).zfill(2) + str(posX).zfill(2)



            #Get the cell from our generated coordinates
            cell = cells.get(position)

            #Find the cells text and what word(clue) it belongs to
            text = cell.get('text')
            currentNum = cell.get('wordNumber')


            #If we just started then the first cell is the start of a word so is a number
            if x == 0:
                cell['text'] = number

            #If the cell is currently a black square then we add two dashes across
            #to signify that it belongs to an across word
            elif text == "B":
                cell['text'] = defaultChar

            #If its the start of the word then we ignore it
            elif text == "S":
                pass

            #If its already belongs to the other direction word then we show it belongs to both
            elif text == inferiorChar:
                cell['text'] = "W"


            #I have no idea what is happening here :P
            if currentNum != None:
                cell['wordNumber'] = [currentNum,number]

            else:
                cell['wordNumber'] = [number]



    #Return our solutionGrid
    return solutionGrid





@API.route('/GenerateGrid/<int:B>', methods = ['GET'])
def generateSudoku(B): #The var 'B' controlls how hard the sudoku is higher the easier it is



    # Initialize a 9x9 grid with empty values
    grid = [[0 for x in range(9)] for y in range(9)]

    #Attempt to fill the grid
    if fillGrid(0, 0,grid):
        #If successful we create a 'deepcopy' of the grid which creates a perfect replica
        changedGrid = copy.deepcopy(grid)
        #Iterate through our copied grid
        for n in range(9):
            for m in range(9):
                #Randomly remove numbers
                diceRoll = random.randint(1,B)
                if diceRoll <= 6: #Removes 6/B numbers from the grid where B is the upper bound for our random number
                    #Overwrite the existing number
                    changedGrid[n][m] = ''

        #Return our original grid and the grid with numbers removed
        return jsonify({'original': grid, 'removed': changedGrid})

    #If we can't do it :( return error message
    else:
        return "Failed to generate Sudoku!"

def fillGrid(row, col,grid):
    # If we've reached the end of the grid, return True (base case)
    if row == 9:
        return True

    # Calculate next cell's position
    nextRow, nextCol = (row, col + 1) if col < 8 else (row + 1, 0)

    # Try placing a random number (1-9) in the current cell
    numbers = list(range(1, 10))
    #Randomly shuffle the numbers
    random.shuffle(numbers)
    #Iterate through the result
    for num in numbers:
        #Check if it maintains the rules of sudoku
        if isValid(num, row, col,grid):
            #If true then write it in the position we are currently at
            grid[row][col] = num

            #Recursively fill the next cell
            if fillGrid(nextRow, nextCol,grid):
                return True

            #Backtrack if needed
            grid[row][col] = 0

    return False  # If no valid number is found, return False

def isValid(number, row, col,grid):
    # Check if the number is valid in the current row
    if number in grid[row]:
        return False

    # Check if the number is valid in the current column
    for i in range(9):
        if grid[i][col] == number:
            return False

    # Check if the number is valid in the 3x3 subgrid
    startRow, startCol = 3 * (row // 3), 3 * (col // 3)
    for i in range(startRow, startRow + 3):
        for j in range(startCol, startCol + 3):
            if grid[i][j] == number:
                return False

    #If we made it through return True
    return True



#Run the API
API.run(debug=False, port=5002)