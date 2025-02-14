import tkinter as tk
from tkinter import ttk
import jwt


#Create the class
class mainMenuFrame(tk.Frame):
    #Initialise the class
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent = parent

        #Create a set font to use for all the widgets
        self.font = 'Georgia', 15



        # Make it so that buttons are placed correctly and the formatting doesn't mess up
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #Widgets
        self.welcomeLabel = ttk.Label(self, text='Welcome to the Puzzle game!', font = ('Georgia',50))
        self.welcomeLabel.pack(padx = 10,pady = 50)

        self.loginButton = tk.Button(self, text='Log in/Register', command=self.checkIfToken,font=self.font,width = 20,height = 10)
        self.loginButton.place(relx = 0.15,rely =0.4,anchor = 'center')

        self.guestButton = tk.Button(self, text='Play as Guest', command=lambda:self.controller.showFrame('choiceFrame','725x585','Games'),font=self.font,width = 20,height = 10)
        self.guestButton.place(relx = 0.85,rely =0.4,anchor = 'center')

        self.instructionsButton = tk.Button(self, text='Instructions',command = self.instructions,font=self.font, width=10, height=5)
        self.instructionsButton.place(relx=0.5, rely=0.4, anchor='center')

        self.secretKey = 'idkwhattoputforthis'












    def checkIfToken(self):
        afile = open('/Users/jake/main/NEA/Token.txt','r')
        encryptedToken = afile.read()
        afile.close()

        try:
            token = jwt.decode(encryptedToken, self.secretKey, algorithms=["HS256"])
            if token:
                print('Success')
                self.controller.showFrame('choiceFrame','725x585','Games')

        except jwt.ExpiredSignatureError:
            # Handle expired token
            print("Error: Token has expired.")
            self.controller.showFrame('loginEntryFrame', '465x330', 'Log in')


        except jwt.InvalidTokenError:
            # Handle any other errors related to token validity
            print("Error: Invalid token.")
            self.controller.showFrame('loginEntryFrame', '465x330', 'Log in')


    def instructions(self):
        self.controller.showFrame('instructionsFrame','','Instructions')








