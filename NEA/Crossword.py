import requests
from bs4 import BeautifulSoup
import json
class Game():
    def __init__(self):
        self.grid = [['*'for y in range(13)]for x in range(13)]
        self.clues = []
    def GetGame(self):
        url = "https://www.theguardian.com/crosswords/quick/16962"
        response = requests.get(url)
        if (response.status_code) == 200:
            print('success')
        else:
            print('cant find')

        soup = BeautifulSoup(response.text, 'html.parser')

        mydivs = soup.find_all("div", {"class": "js-crossword"})
        test = (mydivs[0].get('data-crossword-data'))

        jsonified = json.loads(test)
        print(jsonified['entries'])

        #Writes an S where we need to start !
        for item in jsonified['entries']:
            temp = item['position']
            tempX = temp['x']
            tempY = temp['y']
            #print(f'x:{tempX}, y:{tempY}')
            self.grid[tempY][tempX] = 'S'

            ##Make input cells different character  (-)!
            if item['direction'] == 'across':
                Length = item['length']
                for i in range(1,Length):
                    self.grid[tempY][tempX+i] = '-'
            elif item['direction'] == 'down':
                Length = item['length']
                for i in range(1,Length):
                    self.grid[tempY+i][tempX] = '|'


    def PrettyPrint(self):
        for row in self.grid:
            print(row)


url = "https://www.theguardian.com/crosswords/quick/16955"

NewGrid = Game()
NewGrid.GetGame()
NewGrid.PrettyPrint()
#NewGrid.PrettyPrint()










#We want to obtain crosswords for our game

#Users like guardian crosswords

#Because you did a survey and guardian was best

#So to source their crosswords we can either manually input data into our applciation and use this however this is time consuming

#Another option is to source this data from the guardian website via web-scraping.

#This is quicker and allows to use a vast collection of crosswords.

#DESIGN

#A cross word is gridlike data and therefore can be presented using a 2D List,

#Crosswords have grids where users can enter answers to clues as well as a display for clues.

#Mockup design of crossword