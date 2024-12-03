from tkinter import *
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

        self.responseLabel = Label(self, text='')


    # Function that creates the 9x9 grid
    def createGrid(self):
        # Dictionary that stores the rectangle IDs with their corresponding text IDs
        self.textIDs = {}

        # Variables to account for pixel sizes
        cellSize = 40
        canvasSize = 40 * 9

        # Create the canvas and place it
        canvas = Canvas(self, width=canvasSize, height=canvasSize)
        canvas.pack()
        canvas.focus_set()

        API_URL = "http://127.0.0.1:5000/GenerateGrid"

        try:
            # Make a GET request to the API
            response = requests.get(API_URL)

            # Check if the request was successful
            if response.status_code == 200:
                grids = response.json()
                sudokuGrid = grids[9:]# Parse the JSON response
                solutionGrid = grids[:9]

            else:
                print(f"Error: Unable to fetch data. Status Code: {response.status_code}")
                print(response.text)

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        # Generate the rectangles
        for row in range(9):
            for col in range(9):

                # Multiply the coordinates by cellSize to get the pixel values of where to place the rectangles (this finds the top left corner of the rectangle)
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

                number = sudokuGrid[row][col]
                if number == '':
                    tag = 'blankSquare'
                    color = 'black'
                else:
                    tag = 'permanentNumber'
                    color = 'blue'

                # Create the text/textID
                textID = canvas.create_text(xCenter, yCenter, text=number, font=("Arial", 16), fill=color, tags=('text',tag))

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

        pixelWidth= 120
        for rowLine in range(1,3):
            canvas.create_line((pixelWidth*rowLine),0,(pixelWidth*rowLine),canvasSize,fill='black',width = 5)

        for columnLine in range(1,3):
            canvas.create_line(0, (pixelWidth*columnLine), canvasSize, (pixelWidth*columnLine),fill = 'black',width = 5)


        self.submitButton = Button(self, text='submit', command=partial(self.canvas2array, canvas,solutionGrid))
        self.submitButton.pack()

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
        itemTags = canvas.gettags(rectangleID)

        if 'active' in itemTags:
            pass

        else:
            canvas.itemconfig(rectangleID, fill="grey")

    def mouseExit(self, canvas, rectangleID, event):
        itemTags = canvas.gettags(rectangleID)

        if 'active' in itemTags:
            pass

        else:
            canvas.itemconfig(rectangleID, fill="white")

    def onClick(self, canvas, rectangleID, event):
        self.clearActive(canvas)

        self.selectedRectangleID = rectangleID
        self.setActive(canvas, self.selectedRectangleID)
        self.selectedTextID = self.textIDs[rectangleID]



    def enterText(self, canvas, event):
        pattern = r'\d'
        char = event.keysym.upper()
        match = re.match(pattern, char)
        match = bool(match)


        tags = canvas.gettags(self.selectedTextID)


        if 'permanentNumber' in tags:
            return False

        if match or char == 'BACKSPACE':
            if char == 'BACKSPACE':
                char = ''
            canvas.itemconfig(self.selectedTextID, text=char)

        canvas.itemconfig(self.selectedTextID, fill='black')



    def canvas2array(self, canvas,solutionGrid):
        solved = True
        self.grid = [['' for x in range(9)] for y in range(9)]

        index = 2

        for col in range(9):
            for row in range(9):
                number = canvas.itemcget(index, 'text')
                self.grid[col][row] = number

                if number == '':
                    pass

                elif solutionGrid[col][row] != int(number):
                    self.responseLabel.config(text='Incorrect')
                    solved = False



                index += 2

        if solved:
            self.responseLabel.config(text = 'Correct!')





















