from tkinter import *
from tkinter import ttk,font

from functools import partial
import re
import requests


# Create the class
class sudokuFrame(Frame):
    # Initialise the class
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # Initialize attributes for the selected rectangle and text
        self.selectedRectangleID = None
        self.selectedTextID = None


        self.font = ('Raleway',50)


    #Function for the user to choose the difficulty of the Sudoku
    def chooseDifficulty(self):

        #Create widgets
        self.goButton = ttk.Button(self, text='\n'+'Play!'+'\n', width=25,command = lambda:setDifficulty('Play'))
        self.goButton.pack()

        self.easyButton = Button(self, text = 'Easy', width = 25, fg = 'green',font = self.font,command = lambda:setDifficulty('Easy'))
        self.easyButton.place(relx = 0.5,rely = 0.2,anchor = 'center')

        self.medButton = Button(self, text='Medium',width = 25,fg = 'orange',font = self.font,command = lambda:setDifficulty('Medium'))
        self.medButton.place(relx = 0.5,rely = 0.5,anchor = 'center')

        self.hardButton = Button(self, text='Hard',width = 25,fg = 'red',font = self.font,command = lambda:setDifficulty('Hard'))
        self.hardButton.place(relx = 0.5,rely = 0.8,anchor = 'center')

        self.difficultyLabel = Label(self,text = 'Difficulty: ',font = self.font)
        self.difficultyLabel.place(relx = 0.35,rely = 0.95,anchor = 'center')

        self.difficultyChoiceLabel = Label(self,text = '',font = self.font)
        self.difficultyChoiceLabel.place(relx = 0.65,rely = 0.95,anchor = 'center')

        #Start the value of self.B (the difficulty variable)
        #as None for easy error checking
        self.B = None




        #Function pairing the user's button press with
        #The value of B (Difficuly Variable)
        def setDifficulty(choice):
            #Create dictionary of choices for easy linking
            choices = {'Easy':16,'Medium':11,'Hard':9}


            #If the input is in the choices dictionary do this
            if choice in choices:

                #Set the integer value of B with it's corresponding
                #string in the dictionary
                self.B = choices[choice]

                #Update the label to provide UI feedback to the user,
                #letting them know the difficulty they clicked on
                self.difficultyChoiceLabel.config(text=choice)


            #If the input is to play
            else:
                #If self.B has been chosen already
                if self.B is not None:
                    #Delete all the current widgets on the screen
                    for widget in self.winfo_children():
                        widget.destroy()

                    #Call the createGrid function
                    self.createGrid()





    # Function that creates the 9x9 grid
    def createGrid(self):
        # Dictionary that stores the rectangle IDs with their corresponding text IDs
        self.textIDs = {}
        self.candidateModeBool = False
        self.directions = {'1':'nw','2':'n','3':'ne','4':'w','5':'center','6':'e','7':'sw','8':'s','9':'se',}

        self.candidateModeTexts = {i: [] for i in range(0, 81)}
        self.responseLabel = Label(self, text='')




        # Variables to account for pixel sizes
        cellSize = 80
        canvasSize = 80 * 9

        # Create the canvas and place it
        canvas = Canvas(self, width=canvasSize, height=canvasSize)
        canvas.pack()
        canvas.focus_set()




        self.API_URL = f'http://127.0.0.1:5000/GenerateGrid/{int(self.B)}'
        try:
            # Make a GET request to the API
            response = requests.get(self.API_URL)

            # Check if the request was successful
            if response.status_code == 200:
                grids = response.json()
                solutionGrid = grids['original']# Parse the JSON response
                sudokuGrid = grids['removed']

            else:
                print(f"Error: Unable to fetch data. Status Code: {response.status_code}")
                print(response.text)

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        # Generate the rectangles
        for row in range(9):
            for col in range(9):

                # Multiply the coordinates by cellSize to get the pixel values of where to
                # place the rectangles (this finds the top left corner of the rectangle)
                x1 = col * cellSize
                y1 = row * cellSize

                # Add 40 to both coordinates to find the bottom right corner of the rectangle
                x2 = x1 + cellSize
                y2 = y1 + cellSize

                # Find the center of every rectangle to place text properly
                xCenter = (x1 + x2) / 2
                yCenter = (y1 + y2) / 2

                # Create rectangle
                rectangleID = canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")




                #Retrieve the number value of the rectangle
                number = sudokuGrid[row][col]
                #If there is no number there then it is a blank square or where a user can input text
                if number == '':
                    #Give it a tag so we can validate it
                    tag = 'blankSquare'
                    font=('Arial', 24)

                #If there is text there then it should be protected and not be modified in any way
                else:
                    #Give it a tag so we can protect it
                    tag = 'permanentNumber'
                    #Give it a bold text for visual differentiation
                    font=('Arial', 24,'bold')

                # Create the text/textID
                textID = canvas.create_text(xCenter, yCenter, text=number, font=font, fill='black', tags=('text',tag))

                # Append to dictionary
                self.textIDs[rectangleID] = textID

                # Bind functions to each rectangle and text
                canvas.tag_bind(rectangleID, "<Enter>", partial(self.mouseEnter, canvas, rectangleID))
                canvas.tag_bind(rectangleID, "<Leave>", partial(self.mouseExit, canvas, rectangleID))
                canvas.tag_bind(rectangleID, "<Button-1>", partial(self.onClick, canvas, rectangleID))

                canvas.tag_bind(textID, "<Enter>", partial(self.mouseEnter, canvas, rectangleID))
                canvas.tag_bind(textID, "<Leave>", partial(self.mouseExit, canvas, rectangleID))
                canvas.tag_bind(textID, "<Button-1>", partial(self.onClick, canvas, rectangleID))

                canvas.bind('<Key>', partial(self.enterText, canvas))

        #Variable to store length of lines
        pixelWidth = 240

        #Create the big lines making our 9x9 grid into a 3x3x3 grid
        for rowLine in range(1,3):
            canvas.create_line((pixelWidth*rowLine),0,(pixelWidth*rowLine),canvasSize,fill='black',width = 5)

        for columnLine in range(1,3):
            canvas.create_line(0, (pixelWidth*columnLine), canvasSize, (pixelWidth*columnLine),fill = 'black',width = 5)


        #Widgets
        self.submitButton = Button(self, text='Check!', command=partial(self.canvas2array, canvas,solutionGrid))
        self.submitButton.pack()

        self.candidateButton = Button(self,text = 'Candidate Mode',command = self.candidateMode)
        self.candidateButton.place(relx = 0.2,rely = 0.975,anchor = 'center')

        self.normalButton = Button(self,text = 'Normal Mode',command = self.normalMode)
        self.normalButton.place(relx = 0.8,rely = 0.975,anchor = 'center')

        self.responseLabel.pack()


    # Function that sets a rectangle to be 'active'
    def setActive(self, canvas, rectangleID):
        # Finds the tags of the current item
        self.tags = canvas.gettags(rectangleID)

        # Add the 'active' tag to it
        self.tags += ('active',)
        canvas.itemconfig(rectangleID, tags=self.tags)

        # Give it a blueish color
        canvas.itemconfig(rectangleID, fill="#ADD8E6")

    # Function to clear the active cells - simple
    def clearActive(self, canvas):
        # Find the current active one - if there is - if not then this function does nothing - good - no errors
        for item in canvas.find_withtag('active'):
            self.itemTags = canvas.gettags(item)  # Get the tags of the current item
            self.cleanTags = list(filter(lambda x: (x != 'active'), self.itemTags))  # Remove the 'active' tag
            canvas.itemconfig(item, tags=self.cleanTags)  # Update the tags of the item
            canvas.itemconfig(item, fill="white")  # Change the color back to white



    def mouseEnter(self, canvas, rectangleID, event):
        #Get the tags of the rectangle
        itemTags = canvas.gettags(rectangleID)

        #If its a active rectangle (colored light blue) then it wouldnt make sense to darken it
        if 'active' in itemTags:
            pass

        else:
            canvas.itemconfig(rectangleID, fill="grey")

    #Same function as mouseEnter except we fill it back to white
    def mouseExit(self, canvas, rectangleID, event):
        itemTags = canvas.gettags(rectangleID)

        if 'active' in itemTags:
            pass

        else:
            canvas.itemconfig(rectangleID, fill="white")


    #When we click on a rectangle it will set it to be the active onc
    def onClick(self, canvas, rectangleID, event):
        #Remove all active rectangles
        self.clearActive(canvas)

        #Get the rectangleID of our selected rectangle
        self.selectedRectangleID = rectangleID
        #Set it active
        self.setActive(canvas, self.selectedRectangleID)
        #Append it to textIDs as it is probable the user will input a value in the cell - if not no worries it will just store an empty string
        self.selectedTextID = self.textIDs[rectangleID]



    def enterText(self, canvas, event):
        #This pattern is for re - we want to make sure the
        #input is a number so r'\d' means digit
        pattern = r'\d'
        #Our char is the input from the keyboard
        char = event.keysym.upper()
        #This is for validation. bool(match) will return true or false.
        #If it returns true, we know that it is a number thus a valid input
        match = re.match(pattern, char)
        match = bool(match)

        #Get the tags of the selectedTextID
        self.tags = canvas.gettags(self.selectedTextID)
        self.currentText = canvas.itemcget(self.selectedTextID,'text')


        #If the number we are on is a permanent number or char is 0 (an invalid input in sudoku) then we prevent the user from changing it
        if 'permanentNumber' in self.tags or char == '0':
            return False


        #If the user wants to delete the number then we just update the value in the rectangle to be blank (empty string)
        if match or char == 'BACKSPACE':
            if char == 'BACKSPACE':
                char = ''

            #If we are in candidate mode run thus
            if self.candidateModeBool:
                #Remove the existing number if there is one in the cell
                canvas.itemconfig(self.selectedTextID,text = '')

                #Get the coordinates of the rectangle
                rectangleCoords = canvas.coords(self.selectedRectangleID)
                #Break up our coordinates into 4 seperate variables
                x1, y1, x2, y2 = rectangleCoords

                #Get our anchor value
                anchor = self.directions.get(char, None)
                #Set up our anchor positions
                anchorPositions = {
                    'nw': (x1 + 5, y1 + 5),  # Top-left
                    'n': ((x1 + x2) / 2, y1 + 5),  # Top-middle
                    'ne': (x2 - 5, y1 + 5),  # Top-right
                    'w': (x1 + 5, (y1 + y2) / 2),  # Middle-left
                    'center': ((x1 + x2) / 2, (y1 + y2) / 2),  # Center
                    'e': (x2 - 5, (y1 + y2) / 2),  # Middle-right
                    'sw': (x1 + 5, y2 - 5),  # Bottom-left
                    's': ((x1 + x2) / 2, y2 - 5),  # Bottom-middle
                    'se': (x2 - 5, y2 - 5)  # Bottom-right
                }

                if anchor is None:
                    return False

                #Save our anchor position in two variables x and y
                x, y = anchorPositions[anchor]

                #Get the text values
                data = self.candidateModeTexts[(self.selectedTextID / 2) - 1]
                #Create a list to temporarily hold the numbers
                self.numbers = []

                #Iterate through the numbers we have and append it to the list
                for i in range(len(data)):
                    number = data[i][0]
                    self.numbers.append(number)




                #If the input is already there the user has requested to delete the number
                if char in self.numbers:
                    #Iterate through the list finding all the numbers
                    chars = [item[0] for item in data]

                    #Get the index of the chacter
                    index = chars.index(char)
                    text = data[index]

                    #Delete the text and textID
                    canvas.delete(text[1])
                    del self.candidateModeTexts[(self.selectedTextID / 2) - 1][index]


                #If the user wants to add the number normally then do this
                else:
                    #Create text at location x,y and anchor anchor (the value we previously determined)
                    self.candidateText = canvas.create_text(x, y, text=char, font=('Arial', 16), anchor=anchor,fill = 'black',tags = 'candidateNumber')

                    #Get the text values
                    dataTexts = char,str(self.candidateText)
                    #Append them to the list of candidateModeTexts
                    self.candidateModeTexts[(self.selectedTextID / 2) - 1].append(dataTexts)


                
                canvas.coords(self.selectedTextID, x, y)

            if not self.candidateModeBool:
                # Reset to centered placement for normal mode
                rectangleCoords = canvas.coords(self.selectedRectangleID)
                x1, y1, x2, y2 = rectangleCoords
                xCenter = (x1 + x2) / 2
                yCenter = (y1 + y2) / 2

                # In the Normal Mode logic
                data = self.candidateModeTexts[(self.selectedTextID / 2) - 1]

                #Iterate through the texts
                for candidate in data:
                    #Return the textID for every text
                    textID = candidate[1]
                    #Delete it
                    canvas.delete(textID)
                #Clear it from the list
                self.candidateModeTexts[(self.selectedTextID / 2) - 1].clear()



                # Update text content and reset its anchor to 'center'
                canvas.itemconfig(self.selectedTextID,text=char,font=('Arial', 26),anchor='center') # Ensure it's centered

                # Reset the coordinates of the text to match the rectangle's center
                canvas.coords(self.selectedTextID, xCenter, yCenter)


        #Set it to black color
        canvas.itemconfig(self.selectedTextID, fill='black')


    #Function to return the canvas of numbers into a 2D array
    def canvas2array(self, canvas,solutionGrid):
        #Create an empty 9x9 2D array
        self.grid = [['' for x in range(9)] for y in range(9)]
        #Booleans for checking 
        self.complete = True
        self.solved = True


        index = 2

        #Create a nested for loop inside a for loop to run 9x9 times
        for col in range(9):
            for row in range(9):
                #Get the number value from the rectangle
                number = canvas.itemcget(index, 'text')
                #Append it to the list
                self.grid[col][row] = number

                #If it is a number (the alternative would be an empty string) we cast it to an INT data type
                if number.isdigit():
                    number = int(number)

                #If the user hasn't input anything for one of the cells we change self.complete to False as the puzzle isn't complete
                if number == '':
                    self.complete = False

                #If the number is wrong then we set self.solved as False as the puzzle is incorrectly solved
                elif solutionGrid[col][row] != number:
                    self.solved = False
                    #Return incorrect message to user
                    self.responseLabel.config(text='Incorrect')
                    #Highlight the number in red so the user can see the incorrect numbers
                    canvas.itemconfig(index,fill = 'red')

                #If the number is correct do this
                else:
                    #Get the font of the number
                    font = canvas.itemcget(index,'font')
                    #If its bold then we ignore it as it is a permanent number
                    if 'bold' not in font:
                        canvas.itemconfig(index, fill='green')


                #Increment index value by two every time this is run
                index += 2


        #If all the answers are correct but the puzzle isn't complete then return 'incomplete' to the user
        if self.solved and not self.complete:
            self.responseLabel.config(text = 'Incomplete')

        #If its solved and complete then display the success frame to the user congratulating them :)
        elif self.complete and self.solved:
            self.controller.showFrame('successFrame', '600x650', 'Well Done!')



    #Functions that swich boolean values for candiate and normal mode
    def candidateMode(self):
        self.candidateModeBool = True

    def normalMode(self):
        self.candidateModeBool = False