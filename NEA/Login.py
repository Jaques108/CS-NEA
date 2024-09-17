
from tkinter import *



app = Tk()
app.geometry("400x400")
app.title('Main Menu')
app.resizable(width=FALSE,height=FALSE)



def login():


    loginWin = Toplevel(app)
    loginWin.geometry("300x200")
    loginWin.resizable(width=FALSE, height=FALSE)

    userNameEntry = Entry(loginWin)
    userNameEntry.place(relx = 0.6, rely =0.2,anchor = CENTER)

    userLabel = Label(loginWin, text = 'Username')
    userLabel.place(relx = 0.15,rely = 0.2,anchor = CENTER)

    passEntry = Entry(loginWin)
    passEntry.place(relx=0.6, rely=0.5, anchor=CENTER)

    passLabel = Label(loginWin, text='Password')
    passLabel.place(relx = 0.15,rely = 0.5,anchor = CENTER)

    def check():
        user = userNameEntry.cget(key="text")
        password = passEntry.cget(key="text")

    def cont():
        if user == "" or password == "":
            pass

        else:
            loginWin.destroy()
            sudoku()

    playButton = Button(loginWin, text = 'Play', command = cont)
    playButton.place(relx = 0.5, rely = 0.75,anchor = CENTER)

    for widget in loginWin.winfo_children():
        widget.config(font='Georgia')




def sudoku():

    playWin = Tk()
    playWin.title("Sudoku")
    playWin.resizable(width=FALSE, height=FALSE)

    #way too hard
    """canvas = Canvas(playWin)
    canvas.create_line(15, 25, 200, 25,width=5)
    line1.grid(row = 3,column = 3)"""

    valid = (playWin.register(validate_entry), '%P')
    playWin.geometry("350x335")
    for row in range(9):
        for col in range(9):
            entry = Entry(playWin, width=2, validate='key', validatecommand=valid,justify = 'center')
            entry.grid(row=row, column=col, padx=4, pady=4)

    playWin.mainloop()



def crosswords():
    pass






def choose():
    app.destroy()

    chooseWin = Tk()
    chooseWin.geometry("400x150")
    chooseWin.title("What to play")

    sudokuButton = Button(chooseWin,text = "Sudoku",command = sudoku, width=20,height=20)
    sudokuButton.place(relx = 0.25,rely = 0.5,anchor = CENTER)

    crosswordsButton = Button(chooseWin, text="Crossword", width=20, height=20)
    crosswordsButton.place(relx=0.75, rely=0.5, anchor=CENTER)










login_button = Button(app, text = 'Log in',command = login)
login_button.place(relx = 0.5,rely = 0.6, anchor = CENTER)

guest_button = Button(app, text = 'Play as Guest',command = choose)
guest_button.place(relx = 0.5, rely = 0.8, anchor = CENTER)


for widget in app.winfo_children():
    widget.config(font = ('Georgia', 30))


welcome_label = Label(app,text = 'Welcome',font = ('Georgia', 50))
welcome_label.place(relx = 0.5,rely = 0.2, anchor = CENTER)








def validate_entry(char_input):
    if len(char_input) <= 1 and char_input.isdigit() or char_input == "":
        return True
    else:
        return False




app.mainloop()