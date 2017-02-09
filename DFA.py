__author__ = 'daniel'

class Graph:

    def __init__(self):
        self.numNodes = 0
        self.alphabetSize = 0
        self.startState = 0
        self.alphabet = ""
        self.graph = []
        self.acceptingStates = []
        self.accessableStates = []
        self.table = []
        self.equivilences = []

    def readFile(self, fileName):
        self.fileName = fileName
        f = open(fileName, 'r')
        i = 0
        for line in f:
            if (i == 0):
                self.numNodes = int(line[0])
                self.alphabetSize = int(line[2])
            elif (i == 1):
                self.alphabet = line.strip('\n')
            elif (i > 1 and i < self.numNodes + 2):
                row = []
                for j in range(self.alphabetSize):
                    row.append(int(line[j * 2]))
                self.graph.append(row)
            elif (i == self.numNodes + 2):
                self.startState = int(line[0])
            elif (i == self.numNodes + 3):
                for j in range(self.numNodes):
                    self.acceptingStates.append(int(line[j * 2]))
            i += 1
        f.close()

    def trimDFA(self):
        for i in range(self.numNodes):
            self.accessableStates.append(0)

        self.accessableStates[self.startState] = 2
        for i in range(self.alphabetSize):
            if(self.accessableStates[self.graph[self.startState][i]] == 0):
                self.accessableStates[self.graph[self.startState][i]] = 1
        hasChanged = True
        while hasChanged:
            for i in range(self.numNodes):
                if self.accessableStates[i] == 1:
                    self.accessableStates[i] = 2
                    hasChanged = True
                    for j in range(self.alphabetSize):
                        if self.accessableStates[self.graph[i][j]] == 0:
                            self.accessableStates[self.graph[i][j]] = 1
                else:
                    hasChanged = False

    def minDFA(self):
        for i in range(self.numNodes):
            self.equivilences.append(i)
        for r in range(self.numNodes):
            row = []
            for c in range(self.numNodes):
                if(r > c):
                    row.append(0)
            self.table.append(row)

        for r in range(self.numNodes):
            for c in range(r):
                if (self.acceptingStates[r] != self.acceptingStates[c]):
                    self.table[r][c] = 1
        hasChanged = True
        while hasChanged:
            for r in range(self.numNodes):
                for c in range(r):
                    if(self.table[r][c] == 0):
                        for i in range(self.alphabetSize):
                            if self.graph[r][i] > self.graph[c][i] and self.table[self.graph[r][i]][self.graph[c][i]] == 1:
                                self.table[r][c] = 1
                                hasChanged = True
                            elif self.graph[r][i] < self.graph[c][i] and self.table[self.graph[c][i]][self.graph[r][i]] == 1:
                                self.table[r][c] = 1
                                hasChanged = True
                            else:
                                hasChanged = False

    def printResult(self):
        firstLine = "m = " + str(self.numNodes) + ",n = " + str(self.alphabetSize)
        secondLine = "alphabet: " + self.alphabet
        thirdLine = "   "
        for i in range(self.numNodes):
            thirdLine += str(i) + " "
        print(firstLine)
        print(secondLine)
        print(thirdLine)
        for r in range(1, self.numNodes):
            nextLine = str(r) + "  "
            for c in range(r):
                nextLine += str(self.table[r][c])
                nextLine += " "
            print(nextLine)
        for r in range(self.numNodes):
            for c in range(r):
                nextLine = ""
                if self.table[r][c] == 0:
                    nextLine = "combining state " + str(r) + " into " + str(c)
                    self.equivilences[r] = c
                    print(nextLine)
        lastLine = ""
        for i in range(self.numNodes):
            lastLine = lastLine + str(self.equivilences[i]) + " "
        print(lastLine)
        for i in range(self.numNodes):
            if(self.accessableStates[i] == 0):
                printMessage = "trimming state " + str(i)
                print(printMessage)
        print("")

    def toString(self):
        stringRep = ""
        firstLine = "m = " + str(self.numNodes) + ",n = " + str(self.alphabetSize)
        secondLine = "alphabet: " + self.alphabet
        thirdLine = "   "
        for i in range(self.numNodes):
            thirdLine += str(i) + " "
        stringRep = firstLine + "\n" + secondLine + "\n" + thirdLine + "\n"
        for r in range(1, self.numNodes):
            nextLine = str(r) + "  "
            for c in range(r):
                nextLine += str(self.table[r][c])
                nextLine += " "
            stringRep = stringRep + nextLine + "\n"

        for r in range(self.numNodes):
            for c in range(r):
                nextLine = ""
                if self.table[r][c] == 0:
                    nextLine = "combining state " + str(r) + " into " + str(c)
                    self.equivilences[r] = c
                    stringRep += nextLine + "\n"
        lastLine = ""
        for i in range(self.numNodes):
            lastLine = lastLine + str(self.equivilences[i]) + " "
        stringRep += lastLine + "\n"
        for i in range(self.numNodes):
            if(self.accessableStates[i] == 0):
                printMessage = "trimming state " + str(i)
                stringRep += printMessage + "\n"
        stringRep += "\n"
        print(stringRep)
        return stringRep

class fileWriter:

    def __init__(self):
        self.fileName = "output"

    def printToFile(self, outputString):
        f = open(self.fileName, "w")
        f.write(outputString)
        f.close

sampleGraph = Graph()
sampleGraph.readFile("sampleDFA")
sampleGraph.minDFA()
sampleGraph.trimDFA()
sampleGraph1 = Graph()
sampleGraph1.readFile("sampleDFA1")
sampleGraph1.minDFA()
sampleGraph1.trimDFA()
g2 = Graph()
g2.readFile("sampleDFA2")
g2.minDFA()
g2.trimDFA()
programOutput = fileWriter()
programOutput.printToFile(sampleGraph.toString() + sampleGraph1.toString() + g2.toString())