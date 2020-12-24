import csv
import time
import matplotlib.pyplot as plt


def readSudoku(id):
    with open("./data/Sudoku.csv", "r") as f:
        reader = csv.reader(f, delimiter=';')
        row = next(reader)
        for i in range(id):
            row = next(reader)
        id, difficulty, sudoku, solution = [row[i] for i in range(4)]
    sudoku = sudoku.replace('.', '0')

    return [id, difficulty, sudoku, solution]

def printSudoku(sudoku):
    if sudoku == None:
        print(None)
        return -1
    for i in range(9):
        if(i%3==0 and i != 0):
            print("----------------------")
        for j in range(9):
            if(j%3 == 0 and j!=0):
                print("|", end = ' ')
            if(sudoku[(9*i)+j] != "."):
                print(sudoku[(9*i)+j], end = ' ')
            else:
                print("_", end = ' ')
        print("")

def varVector(sudoku):
    vector = []
    for i in range(len(sudoku)):
        if sudoku[i] == "0":
            vector.append(i)
    return vector

def checkColumn(sudoku, index, value):
    column = index%9
    for i in range(9):
        if(int(sudoku[column+9*i]) == value):
            return False
    return True

def checkRow(sudoku, index, value):
    row = int(index/9)
    for i in range(9):
        if (int(sudoku[i + 9 * row]) == value):
            return False
    return True

def checkSquare(sudoku, index, value):
    sq_column = int((index%9)/3)
    sq_row = int((index/9)/3)
    for i in range(3):
        for j in range(3):
            if int(sudoku[(sq_column*3+i) + (sq_row*3+j)*9]) == value:
                return False
    return True

def checkSolution(sudoku):
    for i in range(81):
        var = int(sudoku[i])
        sudoku = sudoku[:i] + "0" + sudoku[i+1:]
        c1 = checkRow(sudoku, i, var)
        c2 = checkColumn(sudoku, i, var)
        c3 = checkSquare(sudoku, i, var)

        if not(c1 or c2 or c3):
            return False
    return True

def test(sudoku, variables, i):
    sudoku = sudoku[:]

    if(i == len(variables)):
        if(checkSolution(sudoku)):
            return sudoku
        else:
            return None

    var = variables[i]

    for j in range(1, 10):
        if(checkRow(sudoku, var, j) and checkColumn(sudoku, var, j) and checkSquare(sudoku, var, j)):
            sol = test(sudoku[:var] + str(j) + sudoku[var+1:], variables, i+1)
            if sol != None:
                return sol
    return None


data = readSudoku(45)
sudoku = data[2]
variables = varVector(sudoku)
sol = test(sudoku, variables, 0)
if sol == None: print("No solution found")

printSudoku(sol)
