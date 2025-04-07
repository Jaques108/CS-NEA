from tkinter import *
from tkinter import PhotoImage



#Create the class
class successFrame(Frame):

    #Initialise the class
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.pack_propagate(False)  # Prevent resizing based on widgets


    #Function run when crossword is solved
    def triggerTimeUpdate(self):
        #Create new window
        app = Tk()
        app.geometry('350x150')
        app.title('Well Done!')

        #Collect the users time taken from the Timer.txt File
        afile = open('/Users/jake/main/NEA/Main Code/Timer.txt', 'r')
        time = afile.read()
        afile.close()


        #Widgets
        timerLabel = Label(app, text='Time Taken:', font=('Times New Roman', 35))
        timerLabel.place(relx=0.5, rely=0.3,anchor = 'center')

        valueLabel = Label(app,text = time,font = ('Georgia',35))
        valueLabel.place(relx = 0.5,rely = 0.7,anchor = 'center')

        #Delete the data in the text file as we already have it
        afile = open('/Users/jake/main/NEA/Main Code/Timer.txt', 'w')
        afile.write('')
        afile.close()