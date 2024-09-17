

from tkinter import *
app = Tk()
app.geometry("400x400")

def change():
    update = entry1.cget(key = 'text')
    label1.config(text = update)
    print("new text = ",update)


entry1 = Entry(app)
entry1.pack()

button1 = Button(app, text = "testing",command = change)
button1.pack()

label1 = Label(app, text = "")
label1.pack()

app.mainloop()
