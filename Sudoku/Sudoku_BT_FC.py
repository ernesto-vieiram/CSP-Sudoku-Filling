import csv
import copy



class Variable(object):
    def __init__(self, index):
        self.domain = range(1, 10)
        self.index = index
        self.value = None

    def setDomain(self, domain):
        self.domain = domain[:]

    def __str__(self):
        return "Value " + str(self.value) + " at position #" + str(self.index) + " with domain " + str(self.domain)

def readSudoku(id):
    with open("./data/Sudoku.csv", "r") as f:
        reader = csv.reader(f, delimiter=';')
        row = next(reader)
        for i in range(id):
            row = next(reader)
        print(row)
        id, difficulty, sudoku, solution = [row[i] for i in range(4)]
    sudoku = sudoku.replace('.', '0')
    sudoku = [i for i in sudoku]

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
    '''Takes a sudoku represented by a String
        returns a list of variables'''
    vector = []
    for i in range(len(sudoku)):
        if sudoku[i] == "0":
            vector.append(Variable(i))
    return vector

#CHECK VALUE ACCEPTABILITY------------------------
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
        sudoku[i] = '0'
        c1 = checkRow(sudoku, i, var)
        c2 = checkColumn(sudoku, i, var)
        c3 = checkSquare(sudoku, i, var)
        sudoku[i] = var

        if not(c1 or c2 or c3):
            return False
    return True

def forwardChecking(sudoku, variables):
    '''Reduces variables domain to be compatible with the insertedValue in insertedIndex'''
    for var in variables:
        new_domain = []
        for value in var.domain:
            if(checkRow(sudoku, var.index, value) and checkColumn(sudoku, var.index, value) and checkSquare(sudoku, var.index, value)):
                #Compatible element of domain, we keep it
                new_domain.append(value)
        if len(new_domain) == 0:
            return -1
        else:
            var.setDomain(new_domain)
    return 0

def forwardCheckingRows(sudoku, variables, index):
    row = int(index / 9)
    for i in range(9):
        new_domain = []
        var = variables[i + 9 * row]
        if var.value == None:
            for val in var.domain:
                if(checkRow(sudoku, var.index, val)):
                    new_domain.append(val)
    return True

def test(sudoku, variables):

    sudoku = sudoku[:]
    #printSudoku(sudoku)

    if(len(variables) == 0):
        #All variables have a value
        if(checkSolution(sudoku)):
            return sudoku
        else:
            return None

    #Variable we are assigning
    var = variables[0]

    for j in var.domain:
        variables_copy = copy.deepcopy(variables[1:])
        var.value = j
        sudoku[var.index] = var.value
        if(forwardChecking(sudoku, variables_copy) == 0):
            #All domains are compatible with the partial solution
            sol = test(sudoku, variables_copy)
            if sol != None:
                return sol
    return None

data = readSudoku(45)
sudoku = data[2]
variables = varVector(sudoku)

print(forwardChecking(sudoku, variables))

variables.sort(key = lambda x: len(x.domain))
sol = test(sudoku, variables)
printSudoku(sol)

if sol == None: print("No solution found")
