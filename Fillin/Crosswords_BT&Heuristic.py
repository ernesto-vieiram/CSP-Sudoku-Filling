import copy

class CSP(object):
    def __init__(self, problem, variables, domains, dim):
        self.problem = problem
        self.variables = variables
        self.domains = domains
        self.numberOfVariables = len(variables)
        self.dim = dim

    def addVariable(self, newVariable):
        self.variables.append(newVariable)
        self.numberOfVariables += 1

    def orderVariables(self, reverse, inter):
        self.variables.sort(key = lambda x: x.length, reverse=reverse)
        h = list(filter(lambda x: x.type == 'h', self.variables))
        v = list(filter(lambda x: x.type == 'v', self.variables))

        lista = []

        if inter:
            for i in range(max(len(h), len(v))*2):
                try:
                    lista.append(h[i])
                except:
                    continue
                try:
                    lista.append(v[i])
                except:
                    continue
        else:
            lista = h+v

        print([i.type for i in lista])
        print([i.length for i in lista])
        self.variables = copy.deepcopy(lista)

    def printProblem(self):
        for i in self.problem:
            print(i)

    def addValuetoVariable(self, varIndex, value):
        var = self.variables[varIndex]
        if value not in self.domains[var.length] or len(value) != var.length:
            return False
        i = var.position[0]
        j = var.position[1]
        type = var.type
        for k in range(var.length):
            if type == 'h':
                #Horizontal word
                if not self.setCharacter(i, j+k, value[k]):
                    return False
            if type == 'v':
                #Vertical word
                if not self.setCharacter(i+k, j, value[k]):
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

    def backtrack(self, varIndex):
        if varIndex == len(self.variables):
            return 0

        problemBackup = [x[:] for x in self.problem]
        domainsBackup = self.copyDomain(self.domains)

        var = self.variables[varIndex]

        for value in domainsBackup[var.length]:
            #print(self.domains[var.length][value])
            if self.addValuetoVariable(varIndex, value):
                sol = self.backtrack(varIndex+1)
                if sol != -1:
                    return sol

            #self.problem = copy.deepcopy(problemBackup)
            self.problem = [x[:] for x in problemBackup]
            self.domains = self.copyDomain(domainsBackup)

        return -1

    def copyDomain(self, domain: dict):
        ret = {}
        for k in domain.keys():
            ret[k] = domain[k][:]
        return ret

class Variable(object):
    def __init__(self, l, type, i, j):
        self.length = l
        self.value = None
        self.type = type
        self.position = (i, j)

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
    ret = CSP(problem, variables, domains, (m, n))
    return ret

def checkVerticalDepth(v_map, m, n, i, j):
    if i == m or v_map[i][j] == '#': return 0
    else:
        v_map[i][j] = 'X'
        return 1 + checkVerticalDepth(v_map, m, n, i+1, j)

def checkHorizontalDepth(problem, m, n, i, j):
    if j == n or problem[i][j] == '#': return 0
    else:
        problem[i][j] = 'X'
        return 1 + checkHorizontalDepth(problem, m, n, i, j+1)

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

csp = loadProblem("puzzle4", "words4")
csp.printProblem()
csp.orderVariables(reverse = True, inter = True)
csp.backtrack(0)
csp.printProblem()