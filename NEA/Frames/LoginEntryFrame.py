from multiprocessing.resource_tracker import register
from tkinter import ttk
import tkinter as tk
import requests


class loginEntryFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.username = None
        self.password = None

        self.controller = controller
        self.parent = parent

        self.API_URL = 'http://127.0.0.1:5000/'

        self.userNameEntry = ttk.Entry(self)
        self.userNameEntry.grid(row=1,column=1,sticky = 'news')

        self.passEntry = ttk.Entry(self,show ='*')
        self.passEntry.grid(row=2, column=1,sticky = 'news')

        self.userLabel = ttk.Label(self, text='Username')
        self.userLabel.grid(row=1,column=0)

        self.passLabel = ttk.Label(self, text='Password')
        self.passLabel.grid(row=2,column=0)

        self.playButton = ttk.Button(self, text='Log In',command = self.onPlayButtonClick)
        self.playButton.grid(row=3, column=1,sticky = 'news')

        self.responseLabel = ttk.Label(self,text = '',wraplength=185)
        self.responseLabel.grid(row = 4,column = 1,sticky = 'news')

        self.signUpButton = ttk.Button(self,text = 'Register',command = self.signUp)
        self.signUpButton.grid(row = 5,column = 1,sticky = 'news')



    def getUserDetails(self):
        # Fetch the latest user input every time the button is clicked
        username = self.userNameEntry.get()
        password = self.passEntry.get()

        if username == '' or password == '':
            return False  # Return False if either is empty

        return username, password



    def onPlayButtonClick(self):
        # Get the user details (username and password)
        result = self.getUserDetails()

        # Check if the result is valid
        if result:
            username, password = result
            data = {'username': username, 'password': password}
            sendData = requests.post(self.API_URL + 'Login',json = data)

            if not sendData:
                self.responseLabel.config(text = 'Incorrect Username/Password')


            else:
                self.controller.showFrame('choiceFrame', '', 'What to play')

        else:
            self.responseLabel.config(text = "Username or Password fields are empty. Please provide valid inputs.")



    def signUp(self):
        result = self.getUserDetails()

        if result:
            username,password = result
            data = {'username':username,'password':password}
            registerUser = requests.post(self.API_URL + 'CreateUser',json = data)

            if not registerUser:
                self.responseLabel.config(text='User already exists')

            else:
                self.responseLabel.config(text='Registered Successfully')

        else:
            self.responseLabel.config(text="Username or Password fields are empty. Please provide valid inputs.")






