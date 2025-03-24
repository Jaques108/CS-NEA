from tkinter import *

#Create the class
class successFrame(Frame):
    #Initialise the class
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller



        self.pack_propagate(False)  # Prevent resizing based on widgets

        self.koolaidOhYeahMan = PhotoImage(file='/Users/jake/main/NEA/ohyeah.png')

        self.koolaidOhYeahManLabel = Label(self,image = self.koolaidOhYeahMan)
        self.koolaidOhYeahManLabel.place(relx = 0.05,rely = 0.005)

        afile = open('Timer.txt','r')
        time = afile.read()
        afile.close()


        self.timerLabel = Label(self, text=f'Time Taken: {time}', font=('Arial', 35), bg='black')
        self.timerLabel.place(relx=0.15, rely=0.9)






