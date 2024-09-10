
from tkinter import *



app = Tk()
app.geometry("400x400")
app.title('Puzzle Games')


login_button = Button(app, text = 'Log in')
login_button.place(relx = 0.5,rely = 0.6, anchor = CENTER)

guest_button = Button(app, text = 'Play as Guest')
guest_button.place(relx = 0.5, rely = 0.8, anchor = CENTER)


for widget in app.winfo_children():
    widget.config(font = ('Georgia', 30))


welcome_label = Label(app,text = 'Welcome',font = ('Georgia', 50))
welcome_label.place(relx = 0.5,rely = 0.2, anchor = CENTER)






def login():
    pass


def contAsGuest():
    pass






app.mainloop()

