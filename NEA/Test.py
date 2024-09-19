from tkinter import *

app = Tk()
app.title("Test")

x = [2,3,4,5]
y = [2,3,4,5]

for row in range(9):
    for col in range(9):
        label = Label(app,text = "FUN",padx = 5,pady=5)
        label.grid(row = row, column = col)


label.grid()



label1 = Label(app,text = 'test')
label1.grid(row = 10,column = 10)


label1.config(text = "fixed")

app.mainloop()