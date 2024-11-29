from flask import Flask,jsonify
import random
import copy

from NEA.Frames.ChoiceFrame import choiceFrame

sudoku = Flask(__name__)


@sudoku.route('/GenerateGrid',methods = ['GET'])
def generateSudoku():
    # Initialize a 9x9 grid with empty values
    grid = [[0 for x in range(9)] for y in range(9)]

    # Attempt to fill the grid
    if fillGrid(0, 0,grid):
        changedGrid = copy.deepcopy(grid)
        for n in range(9):
            for m in range(9):
                diceRoll = random.randint(1,3)
                if diceRoll == 1:
                    changedGrid[n][m] = ''

        return grid + changedGrid
    else:
        return "Failed to generate Sudoku!"



def fillGrid(row, col,grid):
    # If we've reached the end of the grid, return True (base case)
    if row == 9:
        return True

    # Calculate next cell's position
    nextRow, nextCol = (row, col + 1) if col < 8 else (row + 1, 0)

    # Try placing a random number (1-9) in the current cell
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    for num in numbers:
        if isValid(num, row, col,grid):
            grid[row][col] = num
            if fillGrid(nextRow, nextCol,grid):  # Recursively fill the next cell
                return True
            grid[row][col] = 0  # Backtrack if needed

    return False  # If no valid number is found, return False


def isValid(number, row, col,grid):
    # Check if the number is valid in the current row
    if number in grid[row]:
        return False

    # Check if the number is valid in the current column
    for i in range(9):
        if grid[i][col] == number:
            return False

    # Check if the number is valid in the 3x3 subgrid
    startRow, startCol = 3 * (row // 3), 3 * (col // 3)
    for i in range(startRow, startRow + 3):
        for j in range(startCol, startCol + 3):
            if grid[i][j] == number:
                return False

    return True



# Generate and print the Sudoku grid
result = generateSudoku()


sudoku.run(debug = False,port = 8080)




















