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

        self.secretKey = 'idkwhattoputforthis'


        #Widgets
        login_button = ttk.Button(self, text='Log in/Register', command=self.checkIfToken)
        login_button.grid(row=2,column=0)

        guest_button = ttk.Button(self, text='Play as Guest', command=lambda:self.controller.showFrame('choiceFrame','465x330','What to play'))
        guest_button.grid(row=2,column=2)


        welcome_label = ttk.Label(self, text='Welcome', font=('Georgia', 50))
        welcome_label.grid(row=1, column=1)


    def checkIfToken(self):
        afile = open('/Users/jake/main/NEA/Token.txt', 'r')
        encryptedToken = afile.read()
        afile.close()

        try:
            token = jwt.decode(encryptedToken, self.secretKey, algorithms=["HS256"])
            self.controller.showFrame('choiceFrame', '465x330', 'What to play')

        except jwt.ExpiredSignatureError:
            # Handle expired token
            print("Error: Token has expired.")
            self.controller.showFrame('loginEntryFrame', '300x200', 'Log in')


        except jwt.InvalidTokenError:
            # Handle any other errors related to token validity
            print("Error: Invalid token.")
            self.controller.showFrame('loginEntryFrame', '300x200', 'Log in')









