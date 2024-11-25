from tkinter import *
from tkinter import ttk
import json
import requests
from functools import partial




class crosswordFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        textItems = {}
        nonTextRectangles = []
        startPositions = []
        normalRectangles = []




        def submit():
            code = codeEntry.get()
            url = f'http://127.0.0.1:5000/GenerateCells/{code}'
            dictData = None

            try:
                webResponse = requests.get(url, timeout=7)

                if webResponse.status_code != 200:
                    errorLabel.config(text='Error - Code not accepted. Try again.')
                else:
                    dictData = webResponse.json()

            except requests.exceptions.RequestException as e:
                errorLabel.config(text=f'Connection Error: {e}. Please try again.')

            if dictData is None:
                pass
            else:
                def getCrosswordData():
                    with open('Code.txt', 'w') as afile:
                        json.dump(dictData, afile, indent=4)

                getCrosswordData()

                def displayData():
                    codeLabel.destroy()
                    codeEntry.destroy()
                    codeSubmit.destroy()
                    errorLabel.destroy()


                    cellSize = 40
                    canvasSize = 40 * 13

                    canvas = Canvas(self, width=canvasSize, height=canvasSize)
                    canvas.pack()
                    canvas.focus_set()




                    with open('Code.txt', 'r') as afile:
                        data = json.load(afile)

                    for cellID, cellData in data.items():
                        posX = int(cellID[2:])
                        posY = int(cellID[:2])

                        x1 = posX * cellSize
                        y1 = posY * cellSize
                        x2 = x1 + cellSize
                        y2 = y1 + cellSize

                        obj = str(cellData.get("text"))

                        if obj == 'B':
                            rectangleID = canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
                            nonTextRectangles.append(rectangleID) #Make it so the program isnt stupid and understands that a black square is not a place to put text in




                        else:

                            # Add the text inside the rectangle
                            if obj.isdigit():

                                obj = int(obj)
                                offset = 6


                                if obj > 9 or x1 < 40:   #God forgive me
                                    if x1 < 40 and obj > 9:
                                        offset = 8.75

                                    elif obj < 9:
                                        offset = 8

                                    else:
                                        offset = 6.5

                                xOffset = x1 + offset
                                yOffset = y1 + 7.5


                                startID = canvas.create_text(xOffset, yOffset, text=obj, fill="black", font=('Guardian Egyptian', 8),tags = 'startPositions')
                                rectangleID = canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                                startPositions.append(startID)



                            else:
                                rectangleID = canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")


                            canvas.tag_raise(startID)

                            # Bind events to the rectangle
                            canvas.tag_bind(rectangleID, "<Enter>", partial(mouseEnter, canvas, rectangleID))
                            canvas.tag_bind(rectangleID, "<Leave>", partial(mouseExit, canvas, rectangleID))
                            canvas.tag_bind(rectangleID, "<Button-1>", partial(onClick, canvas, rectangleID))

                            canvas.bind('<Key>', partial(enterText, canvas, rectangleID))

                            canvas.bind('<Left>', partial(enterText, canvas, rectangleID))
                            canvas.bind('<Right>', partial(enterText, canvas, rectangleID))
                            canvas.bind('<Up>', partial(enterText, canvas, rectangleID))
                            canvas.bind('<Down>', partial(enterText, canvas, rectangleID))





                displayData()



        def mouseEnter(canvas,rectangleID,event):
            itemTags = canvas.gettags(rectangleID)

            if 'active' in itemTags:
                pass

            elif rectangleID in nonTextRectangles:
                return False

            elif rectangleID in startPositions:
                return False

            else:
                canvas.itemconfig(rectangleID, fill="grey")



        def mouseExit(canvas,rectangleID,event):
            itemTags = canvas.gettags(rectangleID)

            if 'active' in itemTags:
                pass

            elif rectangleID in nonTextRectangles:
                return False

            elif rectangleID in startPositions:
                return False



            else:
                canvas.itemconfig(rectangleID, fill="white")



        def onClick(canvas, rectangleID, event):

            if rectangleID in nonTextRectangles:
                return False

            elif rectangleID in startPositions:
                return False


            clearActive(canvas)
            setActive(canvas,rectangleID)



        def clearActive(canvas):
            for item in canvas.find_withtag('active'):
                itemTags = canvas.gettags(item)  # Get the tags of the current item
                cleanTags = list(filter(lambda x: (x != 'active'), itemTags)) # Remove the 'active' tag
                canvas.itemconfig(item, tags=cleanTags)  # Update the tags of the item
                canvas.itemconfig(item, fill="white")



        def setActive(canvas,rectangleID):
                tags = canvas.gettags(rectangleID)
                tags += ('active',)
                canvas.itemconfig(rectangleID, tags=tags)

                if rectangleID not in startPositions:
                    canvas.itemconfig(rectangleID, fill="#ADD8E6")



        def enterText(canvas,rectangleID,event):
            directions = ['LEFT','RIGHT','UP','DOWN']
            char = event.keysym.upper()
            replace = True

            if char in directions:
                replace = False

            if char == '\x08' or char == 'BACKSPACE':
                char = ''



            if not char.isalpha() and not char == '':
                return False

            for rectangleID in canvas.find_withtag('active'):
                coords = canvas.coords(rectangleID)


                xCenter = (coords[0] + coords[2]) / 2
                yCenter = (coords[1] + coords[3]) / 2



                if rectangleID in textItems and replace:
                    # If text exists, delete the existing text item
                    canvas.delete(textItems[rectangleID])

                    # Create new text and store the reference in the textItems dictionary
                if replace:
                    textID = canvas.create_text(xCenter, yCenter, text=char, font=("Arial", 16), fill="black", tags='text')
                    textItems[rectangleID] = textID

                    #Make sure the text has the same attributes as the rectangle because tkinter is goofy like that
                    canvas.tag_bind(textID, "<Enter>", partial(mouseEnter, canvas, rectangleID))
                    canvas.tag_bind(textID, "<Leave>", partial(mouseExit, canvas, rectangleID))
                    canvas.tag_bind(textID, "<Button-1>", partial(onClick, canvas, rectangleID))
                    canvas.bind('<Key>', partial(enterText, canvas, rectangleID))



                offset = 1

                if char == '' or char == 'LEFT':
                    offset = - 1

                nextRectangleID = rectangleID + offset


                if char == 'UP':
                    if yCenter != 20:
                        yCenter -= 40

                    tuple = canvas.find_overlapping(xCenter,yCenter,xCenter + 1,yCenter + 1) #Returns the ID as a tuple idk why
                    nextRectangleID = tuple[0]

                elif char == 'DOWN':
                    if yCenter != 500:
                        yCenter += 40
                    tuple = canvas.find_overlapping(xCenter,yCenter,xCenter + 1,yCenter + 1)
                    nextRectangleID = tuple[0]



                if nextRectangleID in nonTextRectangles:
                    return False


                elif nextRectangleID in startPositions and (char != 'UP' or char != 'DOWN'):
                    nextRectangleID = rectangleID + (offset * 2)

                    if nextRectangleID in nonTextRectangles:
                        return False


                newCoords = canvas.coords(nextRectangleID)
                nextYCenter = (newCoords[1] + newCoords[3]) / 2

                difference = yCenter - nextYCenter

                if difference != 0:
                    return False



                clearActive(canvas)
                setActive(canvas,nextRectangleID)





        # UI Elements
        codeLabel = ttk.Label(self, text='Enter Crossword Code')
        codeLabel.place(relx=0.5, rely=0.25, anchor="center")

        codeEntry = ttk.Entry(self,justify='center')
        codeEntry.place(relx=0.5, rely=0.5, anchor="center")

        codeSubmit = ttk.Button(self, text='Submit', command=submit)
        codeSubmit.place(relx=0.5, rely=0.8, anchor="center")

        errorLabel = ttk.Label(self)
        errorLabel.place(relx=0.5, rely=0.65, anchor="center")