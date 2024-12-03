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

        self.API_URL = 'http://127.0.0.1:5000/CreateUser'

        self.userNameEntry = ttk.Entry(self)
        self.userNameEntry.grid(row=1,column=1)

        self.passEntry = ttk.Entry(self)
        self.passEntry.grid(row=2, column=1)

        self.userLabel = ttk.Label(self, text='Username')
        self.userLabel.grid(row=1,column=0)

        self.passLabel = ttk.Label(self, text='Password')
        self.passLabel.grid(row=2,column=0)

        self.playButton = ttk.Button(self, text='Play',command = self.onPlayButtonClick)
        self.playButton.grid(row=3, column=1)

    def getUserDetails(self):
        # Fetch the latest user input every time the button is clicked
        username = self.userNameEntry.get()
        password = self.passEntry.get()

        if username == '' or password == '':
            return False  # Return False if either is empty

        print('Success')
        return username, password




    def onPlayButtonClick(self):
        # Get the user details (username and password)
        result = self.getUserDetails()

        # Check if the result is valid
        if result:
            username, password = result
            data = {'username': username, 'password': password}
            sendData = requests.post(self.API_URL,json = data)
            if not sendData:
                print('Username/Password not accepted')


        else:
            print("Username or password is empty. Please provide valid inputs.")






