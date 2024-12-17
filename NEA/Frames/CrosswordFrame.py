#Import our needed modules
import random
from tkinter import *
from tkinter import font
from tkinter import ttk
import json
import requests
from functools import partial
from datetime import date



#Create the class
class crosswordFrame(ttk.Frame):

    #Initiate the class
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.randomCode = False

        textItems = {} #Dictionary for the locations of rectangles with text
        textChars = {}
        nonTextRectangles = [] #List for the locations of black rectangles (Non-Text)
        startPositions = [] #List of rectangles at the start of every word

        # Variables to account for pixel sizes
        cellSize = 40
        canvasSize = 40 * 13

        def dailyCrossword():
            self.dailyCrossword = True
            submit()


        #This function is binded to the submit button which is run when it is pressed - starts the whole process
        def submit():

            if self.dailyCrossword:
                startDay = date(2024,12,17)
                today = date.today()

                difference = (today - startDay).days

                #Just when i set this yk
                code = 17041 + difference
            else:
                #Get the code entered
                code = codeEntry.get()

                if code.isdigit():
                    code = int(code) + 9250


            #Create the whole URL by appending the code to the main URL
            url = f'http://127.0.0.1:5000/GenerateCells/{code}'

            #Variable to see if we get returned crossword data
            dictData = None

            try:
                webResponse = requests.get(url, timeout=7) #Include a timeout becuase internet can be slow and we don't want the user to be stuck

                if webResponse.status_code != 200: #Check if response is invalid (200 is a successful status code)
                    errorLabel.config(text='Error - Code not accepted. Try again.') #Display error message to user
                else:
                    dictData = webResponse.json() #Update dictData if response is valid

            except requests.exceptions.RequestException: #Connection error handling
                errorLabel.config(text=f'Connection Error. Please try again.') #Display connection error message to user


            #Make sure we have crossword data
            if dictData is None:
                pass


            else:
                #If we have crossword data run the getCrosswordData function to retrieve it
                def getCrosswordData():
                    #Open text file
                    with open('Code.txt', 'w') as afile:
                        #Write the data into a text file
                        json.dump(dictData, afile, indent=4)

                getCrosswordData() #Actually call the function

                def displayData():
                    #Destroy previous widgets for the crossword
                    codeLabel.destroy()
                    codeEntry.destroy()
                    codeSubmit.destroy()
                    errorLabel.destroy()


                    #Create the canvas and display it
                    canvas = Canvas(self, width=canvasSize + (cellSize*16), height=canvasSize)
                    canvas.pack()
                    canvas.focus_set()

                    self.userGrid = [[None for x in range(13)] for y in range(13)]

                    # Collect the data from the text file
                    with open('Code.txt', 'r') as afile:
                        self.data = json.load(afile)
                        self.solutionGrid = self.data['solutionGrid']

                    def goBack(canvas):
                        canvas.destroy()
                        self.controller.showFrame('choiceFrame', '465x330', 'What to play')
                        canvas.focus_set()

                    def submit(canvas):
                        rectangleIDs = []

                        for cellID in self.data['cells'].items():
                            coords = cellID[0]

                            xCoords = (int(coords[2:]) * 40) + 20
                            yCoords = (int(coords[:2]) * 40) + 20

                            xPos = int(coords[2:])
                            yPos = int(coords[:2])

                            rectangleID = canvas.find_overlapping(xCoords,yCoords,xCoords + 5,yCoords + 5)[0]

                            if rectangleID in textItems:
                                char = textChars[rectangleID]
                                self.userGrid[yPos][xPos] = char

                        solved = True
                        for i in range(13):
                            for x in range(13):
                                userChar = self.userGrid[i][x]
                                solutionChar = self.solutionGrid[i][x]

                                xCoords = (x * 40) + 30
                                yCoords = (i * 40) + 30

                                tempRectangleID = canvas.find_overlapping(xCoords, yCoords, xCoords - 10, yCoords - 10)

                                if userChar is None:
                                    pass

                                else:
                                    textID = tempRectangleID[1]


                                    if userChar == solutionChar and textID in textItems.values():
                                        canvas.itemconfig(textID, fill='Blue')


                                    else:
                                        canvas.itemconfig(textID,fill = 'Red')
                                        solved = False




                        canvas.focus_set()


                    def combinedFunction(canvas,rectangleID,event):
                        enterText(canvas,rectangleID,event)
                        changeTextDirection(canvas,event)



                    for cellID, cellData in self.data['cells'].items(): #Iterate through the data
                        #Find the x and y coordinates for each item using list comprehension

                        posX = int(cellID[2:])
                        posY = int(cellID[:2])

                        #Multiply the coordinates by cellSize to get the pixel values of where to place the rectangles (this finds the top left corner of the rectangle)
                        x1 = posX * cellSize
                        y1 = posY * cellSize

                        #Add 40 to both coordinates to find the bottom right corner of the rectangle
                        x2 = x1 + cellSize
                        y2 = y1 + cellSize


                        #Get the text value of each item ['B','S','W']
                        obj = str(cellData.get("text"))




                        #If the current items text is 'B' it is meant to be a non-text rectangle
                        if obj == 'B':
                            rectangleID = canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black",tags = 'rectangle')
                            nonTextRectangles.append(rectangleID) #Make it so the program isnt stupid and understands that a black square is not a place to put text in



                        #Any other item text
                        else:
                            wordNumberTag = cellData.get('wordNumber')
                            #If the object is a number (one of the numbers to mark the start of a worf)
                            if obj.isdigit():

                                #This next code is due to formatting issues. Numbers on the leftmost column are cut off slightly. Two digit numbers have a similar problem
                                obj = int(obj)
                                offset = 6

                                #God forgive me
                                if obj > 9 or x1 < 40:
                                    if x1 < 40 and obj > 9:
                                        offset = 8.75

                                    elif obj < 9:
                                        offset = 8

                                    else:
                                        offset = 6.5

                                xOffset = x1 + offset
                                yOffset = y1 + 7.5

                                #Alright it's done


                                #Create the little numbers in the top left of rectangles at the start of a word
                                startID = canvas.create_text(xOffset, yOffset, text=obj, fill="black", font=('Guardian Egyptian', 8),tags ='startPositions')
                                rectangleID = canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black",tags = wordNumberTag)

                                #Append the start ID to the array startPositions to keep track of them
                                startPositions.append(startID)



                            else:
                                rectangleID = canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black",tags = wordNumberTag)


                            canvas.tag_raise(startID)

                            #Bind events to the rectangle
                            canvas.tag_bind(rectangleID, "<Enter>", partial(mouseEnter, canvas, rectangleID))
                            canvas.tag_bind(rectangleID, "<Leave>", partial(mouseExit, canvas, rectangleID))
                            canvas.tag_bind(rectangleID, "<Button-1>", partial(onClick, canvas, rectangleID))

                            #Bind key presses
                            canvas.bind('<Key>', partial(enterText, canvas, rectangleID))


                            #Bind arrow keys
                            canvas.bind('<Left>', partial(enterText, canvas, rectangleID))
                            canvas.bind('<Right>', partial(enterText, canvas, rectangleID))
                            canvas.bind('<Up>', partial(combinedFunction, canvas, rectangleID))
                            canvas.bind('<Down>', partial(combinedFunction, canvas, rectangleID))



                    canvas.create_text(canvasSize + (cellSize * 2.3), cellSize - 20, text='Across',font=("Helvetica", 30, "bold"))
                    canvas.create_text(canvasSize + (cellSize * 10), cellSize - 20, text='Down',font=("Helvetica", 30, "bold"))

                    acrossOffset = cellSize + 15
                    downOffset = cellSize + 15

                    wrapWidth = cellSize * 7

                    fontStyle = font.Font(family='Arial', size=12)
                    textFont = ('Arial',16)

                    padding = 1
                    numTimesWraps = 1
                    wraps = False

                    for index, (clue, number, position) in enumerate(self.data['clues']):
                        clueWidth = fontStyle.measure(clue)

                        text = str(number) + ' ' + clue

                        if clueWidth > wrapWidth or wraps:
                            if wraps:
                                wraps = False
                            else:
                                wraps = True

                            padding = numTimesWraps * 10
                            numTimesWraps += 1



                        if position == 'across':
                            canvas.create_text(canvasSize + cellSize,(acrossOffset + padding), text=text,width=wrapWidth,font = textFont,anchor='w')
                            acrossOffset += 30

                        elif position == 'down':
                            canvas.create_text(canvasSize + (cellSize * 9),(downOffset + padding), text=text,width=wrapWidth,font = textFont,anchor='w')
                            downOffset += 30



                    #goBackButton = ttk.Button(self, text='Go Back', command=None)
                    #goBackButton.place(relx=0.95, rely=0.965, anchor='center')

                    checkButton = ttk.Button(self,text = 'Check!',command = partial(submit,canvas))
                    checkButton.place(relx = 0.75,rely = 0.965,anchor = 'center')


                #Call the function
                displayData()







        #Function called when cursor enters the area of a rectangle - provides the user with feedback makes it feel more responsive
        def mouseEnter(canvas,rectangleID,event):
            #Get the current tags of the rectangle
            itemTags = canvas.gettags(rectangleID)


            #Exception handling

            #If rectangle is the current one selected i.e it is blue
            if 'active' in itemTags:
                pass

            #If the rectangle is not in use/meant to be used for text i.e it is black
            elif rectangleID in nonTextRectangles:
                return False

            #If the item is the little text at the top right
            elif rectangleID in startPositions:
                return False

            else:
                #Make the rectangle grey
                canvas.itemconfig(rectangleID, fill="grey")



        #Function that works the same as the previous just when the mouse exits the rectangle
        def mouseExit(canvas,rectangleID,event):
            #Get the current tags of the rectangle
            itemTags = canvas.gettags(rectangleID)

            #Same exception handling

            if 'active' in itemTags:
                pass

            elif rectangleID in nonTextRectangles:
                return False

            elif rectangleID in startPositions:
                return False
            else:
                #Change the rectangle back to normal
                canvas.itemconfig(rectangleID, fill="white")



        #Function called when rectangle is clicked on
        def onClick(canvas, rectangleID, event):

            if rectangleID in nonTextRectangles:
                return False

            elif rectangleID in startPositions:
                return False

            allWordNumberTags = canvas.gettags(rectangleID)

            firstWordTag = None
            secondWordTag = None
            counter = 0

            for tag in allWordNumberTags:
                if tag == 'active' or tag == 'current':
                    pass

                elif tag.isdigit():
                    if counter == 0:
                        firstWordTag = tag
                        counter += 1

                    else:
                        secondWordTag = tag


            if secondWordTag == None:
                rectangles = canvas.find_withtag(firstWordTag)

            else:
                rectangles = canvas.find_withtag(firstWordTag) + canvas.find_withtag(secondWordTag)





            #Make the rectangle clicked the active one and clear the other active one (if there is one)
            clearActive(canvas)
            setActive(canvas,rectangleID)



        #Function to clear the active cells - simple
        def clearActive(canvas):
            #Find the current active one - if there is - if not then this function does nothing - good - no errors
            for item in canvas.find_withtag('active'):
                itemTags = canvas.gettags(item)  #Get the tags of the current item
                cleanTags = list(filter(lambda x: (x != 'active'), itemTags)) #Remove the 'active' tag
                canvas.itemconfig(item, tags=cleanTags)  #Update the tags of the item
                canvas.itemconfig(item, fill="white") #Change the color back to white



        #Function that sets a rectangle to be 'active'
        def setActive(canvas,rectangleID):
                #Finds the tags of the current item
                tags = canvas.gettags(rectangleID)

                #Add the 'active' tag to it
                tags += ('active',)
                canvas.itemconfig(rectangleID, tags=tags)


                #Exception handling
                if rectangleID not in startPositions:
                    #Give it a blueish color
                    canvas.itemconfig(rectangleID, fill="#ADD8E6")



        #Complicated function used to enter text in rectangles - the issue is these rectangles don't have a text attribute unlike labels which do, so it gets a little trickier
        def enterText(canvas,rectangleID,event):
            #List of key directions - avoids the repetitive if/else statements
            directions = ['LEFT','RIGHT','UP','DOWN']

            #Record the character pressed
            char = event.keysym.upper()


            #Boolean used if using arrow keys
            replace = True

            #Check if arrow keys are being used
            if char in directions:
                #Set boolean to false
                replace = False

            #If char is a backspace - set char to blank so it performs a delete function
            if char == '\x08' or char == 'BACKSPACE':
                char = ''

            if len(char) != 1 and char != '' and char not in directions:
                return False


            #Error handling
            if not char.isalpha() and not char == '':
                return False

            #Get rectangle ID of active rectangle
            for rectangleID in canvas.find_withtag('active'):
                coords = canvas.coords(rectangleID)

                #Calculate the center of the rectangle to place text properly
                xCenter = (coords[0] + coords[2]) / 2
                yCenter = (coords[1] + coords[3]) / 2



                #Check if rectangle has text in it and check that we are not using arrow keys
                if rectangleID in textItems and replace:
                    #Delete the existing text item
                    canvas.delete(textItems[rectangleID])


                #Check if we are not using arrow keys
                if replace:
                    textID = canvas.create_text(xCenter, yCenter, text=char, font=("Arial", 16), fill="black", tags='text')
                    textItems[rectangleID] = textID
                    textChars[rectangleID] = char
                    #Create new text and store the reference in the textItems dictionary

                    #Make sure the text has the same attributes as the rectangle because tkinter is goofy like that - the text creates a dead zone where the normal functions of the rectangle do not work
                    canvas.tag_bind(textID, "<Enter>", partial(mouseEnter, canvas, rectangleID))
                    canvas.tag_bind(textID, "<Leave>", partial(mouseExit, canvas, rectangleID))
                    canvas.tag_bind(textID, "<Button-1>", partial(onClick, canvas, rectangleID))
                    canvas.bind('<Key>', partial(enterText, canvas, rectangleID))


                #Variable used to decide if moving to the left(-1) or right(1)
                offset = 1

                #Deleting goes back - so does using the left arrow key
                if char == '' or char == 'LEFT':
                    offset = - 1

                #Calculate the ID of next rectangle to be set active
                nextRectangleID = rectangleID + offset


                #If we're going up then add 40 pixels (size of rectangle) and find the overlapping rectangle and set that active
                if char == 'UP':
                    #Make sure we don't go off the grid
                    if yCenter != 20:
                        yCenter -= 40

                    #Find the ID of the overlapping rectangle but it gets returned as a tuple idk why
                    tuple = canvas.find_overlapping(xCenter,yCenter,xCenter + 1,yCenter + 1)

                    #Convert into integer from tuple
                    nextRectangleID = tuple[0]

                #Same thing for going down
                elif char == 'DOWN':
                    if yCenter != 500:
                        yCenter += 40
                    tuple = canvas.find_overlapping(xCenter,yCenter,xCenter + 1,yCenter + 1)
                    nextRectangleID = tuple[0]


                #If the next rectangle is a black rectangle return false
                if nextRectangleID in nonTextRectangles:
                    return False

                #This is an error because text ID takes the place of a rectangle so its not as simple as adding 1 because it goes to the little number in the top right - so we have to add 2 to skip it - so we multiply the value of offset by 2
                elif nextRectangleID in startPositions and (char != 'UP' or char != 'DOWN'):
                    nextRectangleID = rectangleID + (offset * 2)

                    #However if we go too far and the next rectangle is black then return false
                    if nextRectangleID in nonTextRectangles:
                        return False


                #Check if we have gone to the next row - causes problems so we want to stop it - sides should be hard

                #Retrieve the coordinates of the next rectangle
                newCoords = canvas.coords(nextRectangleID)

                #We are only interested in the Y coordinates so get those from newCoords
                try:
                    nextYCenter = (newCoords[1] + newCoords[3]) / 2

                except:
                    pass


                #Subtract the previous rectangle Y coordinates with the new one
                if nextYCenter:
                    difference = yCenter - nextYCenter
                else:
                    return False

                #If the Y coordinates have changed return false
                if difference != 0:
                    return False


                #If we've made it this far clear the current active rectange and set active the next rectangle
                clearActive(canvas)
                setActive(canvas,nextRectangleID)



        def changeTextDirection(canvas,event):
            print('working')



        #Tkinter Widgets
        codeLabel = ttk.Label(self, text='Enter Crossword Code')
        codeLabel.place(relx=0.5, rely=0.25, anchor="center")

        codeLabel = ttk.Label(self, text='Valid codes range from : 1-7750')
        codeLabel.place(relx=0.5, rely=0.35, anchor="center")

        codeEntry = ttk.Entry(self,justify='center')
        codeEntry.place(relx=0.5, rely=0.5, anchor="center")

        codeSubmit = ttk.Button(self, text='Submit', command=submit)
        codeSubmit.place(relx=0.5, rely=0.75, anchor="center")

        randomCode = ttk.Button(self,text = 'Daily Crossword',command= dailyCrossword)
        randomCode.place(relx = 0.5,rely = 0.875,anchor = 'center')

        errorLabel = ttk.Label(self)
        errorLabel.place(relx=0.5, rely=0.65, anchor="center")







