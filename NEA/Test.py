from tkinter import *
app = Tk()
app.geometry("300x300")


Label = Label(app,text = "TESTING")
Label.pack()


text = Label.cget(key="text")
print(text)

if text == "-":
    print("bazinga")
    Label.config(text = "bazinga")





app.mainloop()
