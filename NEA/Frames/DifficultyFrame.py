#Create the class
class difficultyFrame(ttk.Frame):

    #Initiate the class
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

