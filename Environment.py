#Environment Class

import random
from Animat import Animat

class XYValues:
    
    xValue = 0
    yValue = 0
    def __init__(self):
        self.xValue = 0
        self.yValue = 0

    def __init__(self, x, y):
        self.xValue = x
        self.yValue = y

    def setX(self, x):
        self.xValue = x

    def setY(self, y):
        self.yValue = y

    def getX(self):
        return self.xValue

    def getY(self):
        return self.yValue

    def getCoordinates(self):
        return "(" + str(self.xValue) + ", " + str(self.yValue) + ")"



class Environment:
    #environmentSize = 1000
    #animats = [[Animat() for i in range(environmentSize)] for j in range(environmentSize)]

    #food = [XYValues() for k in range(100)]

    #predators = [XYValues() for l in range(100)]

    def __init__(self):
        self.environmentSize = 64
        self.animats = []
        self.soundHistory = []
        for i in range(self.environmentSize):
            self.soundHistory.append([]) # [sig1 sig2]
            self.animats.append([])
            for j in range(self.environmentSize):
                self.animats[i].append([Animat(), 0, 0])
                self.soundHistory[i].append([0, 0])

    """
    def generateRandomFood(self):

        for i in self.food:
            i.setX(random.randint(0, self.environmentSize))
            i.setY(random.randint(0, self.environmentSize))

        print "Here are the coordinates for the food:"
        for j in self.food:
            print j.getCoordinates()


    def generateRandomPredators(self):

        for i in self.predators:
            i.setX(random.randint(0, self.environmentSize))
            i.setY(random.randint(0, self.environmentSize))

        print "Here are the coordinates for the predators:"
        for j in self.predators:
            print j.getCoordinates()


    def moveFood(self):

        for i in self.food:
            i.setX(i.getX() + random.randint(-1, 1))
            i.setY(i.getY() + random.randint(-1, 1))

        #print "Here are the food coordinates after moving:"
        #for j in self.food:
        #    print j.getCoordinates()

    def movePredators(self):
        for i in self.predators:
            i.setX(i.getX() + random.randint(-1, 1))
            i.setY(i.getY() + random.randint(-1, 1))

        #print "Here are the predator coordinates after moving:"
        #for j in self.predators:
        #    print j.getCoordinates()
    """
    def timeCycle(self):
        for i in range(self.environmentSize):
            for j in range(self.environmentSize):
                tile = self.animats[i][j]
                if tile[1] == 1 and tile[0].mouthOpen():
                    fed = 1
                else :
                    fed = 0
                if tile[2] == 1 and (not tile[0].hide()):
                    hurt = 1
                else:
                    hurt = 0
                sounds = self.soundHistory[i][j]
                [make1, make2] = tile[0].timeCyle(sounds[0],sounds[1],fed,hurt)

    def getHealthiestNeighbor(self, row, col):
        """

        @rtype : Animat
        """
        bestAnimat = self.animats[row][col][0] # current animat
        maintain = True
        for i in range(-1,2):
            for j in range(-1,2):
                if row + i >= len(self.animats): # wraparound if the index is too big (don't need to handle negative case)
                    i -= len(self.animats) + 1
                if col + j >= len(self.animats[i]):
                    j -= len(self.animats[i]) + 1
                tile = self.animats[row+i][col+j]
                if (i != 0 or j != 0) and tile[0].energy > bestAnimat.energy:
                    bestAnimat = tile[0]
                    maintain = False
        if not maintain:
            return bestAnimat
        else:
            return False



    def trainCycle(self):
        for i in range(self.environmentSize):
            for j in range(self.environmentSize):
                individual = self.animats[i][j][0]
                neighbor = self.getHealthiestNeighbor(i,j)
                if neighbor:
                    individual.train(*neighbor.getTrainingData())

environment = Environment()
#environment.timeCycle()
#environment.trainCycle()

#environment.generateRandomFood()
#environment.generateRandomPredators()
#environment.moveFood()
#environment.movePredators()