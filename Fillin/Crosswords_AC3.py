import copy
import queue


class Variable(object):
    id = 0

    def __init__(self, l, type, i, j):
        self.length = l
        self.value = None
        self.type = type
        self.position = (i, j)
        self.id = Variable.id
        Variable.id += 1
        self.domain = None


def loadProblem(input, wordsInput):
    problem = []
    m = 0
    n = 0
    with open("./data/Jolka/" + input, 'r') as f:
        for line in f:
            line = line[:-1]
            problem.append(list(line))
            # dimensions[1] = n
            n = len(line)
            # dimensions[0] = m
            m += 1

    v_words = [row[:] for row in problem]
    h_words = [row[:] for row in problem]

    for i in range(m):
        for j in range(n):
            if problem[i][j] != '#':
                if v_words[i][j] != 'X':
                    d = checkVerticalDepth(v_words, m, n, i, j)
                    if d > 1:
                        v_words[i][j] = d
                    else:
                        v_words[i][j] = 0

                if h_words[i][j] != 'X':
                    d = checkHorizontalDepth(h_words, m, n, i, j)
                    if d > 1:
                        h_words[i][j] = d
                    else:
                        h_words[i][j] = 0
    domains = createDomains(wordsInput)
    variables = createVariables(v_words, h_words)
    for variable in variables:
        variable.domain = domains[variable.length][:]
    constraints = createConstraints(problem, variables, (m, n))
    ret = CSP(problem, variables, domains, constraints, (m, n))
    return ret


class CSP(object):
    def __init__(self, problem, variables, domains, constraints, dim):
        self.problem = problem
        self.variables = variables
        self.domains = domains
        self.numberOfVariables = len(variables)
        self.dim = dim
        self.constraints = constraints

    def AC(self):
        domains = {}
        TDA = queue.Queue()

        for variable in self.variables:
            domains[variable.id] = variable.domain[:]

        self.searchArcs(TDA)

        while not TDA.empty():
            arc = TDA.get()
            variable = arc[0]
            newDx = []
            for x in domains[variable]:
                if self.checkConsistency(x, arc):
                    newDx.append(x)
            if len(domains[variable]) != len(newDx):
                self.searchModifiedArcs(arc[0], TDA, arc[1])
                domains[variable] = newDx[:]
            self.assignDomains(domains)
        return domains

    def searchArcs(self, TDA: queue.Queue):
        for c in self.constraints:
            # Each constraint connects with two varaibles: two arcs
            arc1 = (c[0][0], c)
            arc2 = (c[1][0], c)

            TDA.put(arc1)
            TDA.put(arc2)
        return 0

    def searchModifiedArcs(self, varId, TDA: queue.Queue, constraintUsed):
        for c in self.constraints:
            if c[0][0] == varId and c != constraintUsed:
                TDA.put((c[1][0], c))
            if c[1][0] == varId and c != constraintUsed:
                TDA.put((c[0][0], c))

    def checkConsistency(self, x, arc) -> bool:
        verticalWord = arc[1][0]  # Constraint[0]
        horizontalWord = arc[1][1]  # Constraint[1]

        if verticalWord[0] == arc[0]:
            caller = verticalWord
            callee = horizontalWord
        else:
            caller = horizontalWord
            callee = verticalWord

        charToInsert = x[caller[1]]

        # Check if theres a word in the domain of callee where char is OK to put
        for value in self.variables[callee[0]].domain:
            if value[callee[1]] == charToInsert: return True
        return False

    def assignDomains(self, domains):
        for var in self.variables:
            var.domain = domains[var.id]

    def backtrack(self, varIndex):
        if varIndex == len(self.variables):
            return 0

        variable = self.variables[varIndex]
        problemBackup = copy.deepcopy(self.problem)
        domainBackup = variable.domain[:]

        for value in variable.domain:
            if self.addValueToVariable(varIndex, value):
                sol = self.backtrack(varIndex + 1)
                if sol != -1:
                    return 0
            self.problem = copy.deepcopy(problemBackup)
            variable.domain = domainBackup[:]

        return -1

    def addValueToVariable(self, varIndex, value):
        var = self.variables[varIndex]
        if value not in self.domains[var.length] or len(value) != var.length:
            return False
        i = var.position[0]
        j = var.position[1]
        type = var.type
        for k in range(var.length):
            if type == 'h':
                # Horizontal word
                if not self.setCharacter(i, j + k, value[k]):
                    return False
            if type == 'v':
                # Vertical word
                if not self.setCharacter(i + k, j, value[k]):
                    return False
        var.value = value
        self.domains[var.length].remove(value)
        return True

    def setCharacter(self, i, j, char):
        if self.problem[i][j] == '_':
            self.problem[i][j] = char
            return True
        elif self.problem[i][j] == char:
            return True
        else:
            return False

    def printProblem(self):
        for i in self.problem:
            print(i)


def checkVerticalDepth(v_map, m, n, i, j):
    if i == m or v_map[i][j] == '#':
        return 0
    else:
        v_map[i][j] = 'X'
        return 1 + checkVerticalDepth(v_map, m, n, i + 1, j)


def checkHorizontalDepth(problem, m, n, i, j):
    if j == n or problem[i][j] == '#':
        return 0
    else:
        problem[i][j] = 'X'
        return 1 + checkHorizontalDepth(problem, m, n, i, j + 1)


def createVariables(v_words, h_words):
    variables = []
    for i in range(len(v_words)):
        for j in range(len(v_words[i])):
            if v_words[i][j] != 'X' and v_words[i][j] != '#':
                if v_words[i][j] > 0:
                    variables.append(Variable(v_words[i][j], 'v', i, j))

    for i in range(len(h_words)):
        for j in range(len(h_words[i])):
            if h_words[i][j] != 'X' and h_words[i][j] != '#':
                if h_words[i][j] > 0:
                    variables.append(Variable(h_words[i][j], 'h', i, j))

    return variables


def createDomains(wordsFile):
    domains = {}
    addedDomains = []
    with open("./data/Jolka/" + wordsFile, 'r') as f:
        while True:
            try:
                word = next(f).rstrip()
                l = len(word)
                if l < 2: pass
                if l not in domains.keys():
                    newDomain = []
                    domains[l] = newDomain
                    addedDomains.append(l)
                domains[l].append(word)
            except StopIteration:
                break
    return domains


def createConstraints(problem, variables, dim):
    cons_v = [row[:] for row in problem]
    cons_h = [row[:] for row in problem]
    for var in variables:
        pos = var.position
        len = var.length
        type = var.type
        varId = var.id

        assignVarId(cons_h, cons_v, varId, pos, len, type, 0)
    constraints = []
    for i in range(dim[0]):
        for j in range(dim[1]):
            con_v = cons_v[i][j]
            con_h = cons_h[i][j]

            if con_v not in ['_', '#'] and con_h not in ['_', '#']:
                # New constraint
                constraints.append((con_v, con_h))
    return constraints


def assignVarId(rawConstraints_h: list, rawConstraints_v: list, varId: int, position: tuple, length: int, type: str,
                offset: int):
    if offset == length: return 0
    if type == 'h':
        rawConstraints_h[position[0]][position[1] + offset] = (varId, offset)
    if type == 'v':
        rawConstraints_v[position[0] + offset][position[1]] = (varId, offset)
    return assignVarId(rawConstraints_h, rawConstraints_v, varId, position, length, type, offset + 1)

csp = loadProblem("puzzle1", "words1")
csp.AC()
print(csp.backtrack(0))
csp.printProblem()
