#Environment Class

import random
from Animat import Animat

class XYValues:
    
    xValue = 0
    yValue = 0
    def __init__(self):
        self.xValue = 0
        self.yValue = 0

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

        #initialize food
        self.food = [XYValues() for k in range(self.environmentSize)]
        self.generateRandomFood()

        #initialize predator
        self.predators = [XYValues() for l in range(self.environmentSize)]
        self.generateRandomPredators()

    def generateRandomFood(self):
        for i in self.food:
            i.setX(random.randint(0, self.environmentSize - 1))
            i.setY(random.randint(0, self.environmentSize -1))

        #set the food in the tiles for the first time
        self.setFoodInTiles()

        print "Here are the coordinates for the food:"
        for j in self.food:
            print j.getCoordinates()

    def generateRandomPredators(self):
        for i in self.predators:
            i.setX(random.randint(0, self.environmentSize -1))
            i.setY(random.randint(0, self.environmentSize -1))

        #set the predators in the tiles fo the first time
        self.setPredatorsInTiles()

        print "Here are the coordinates for the predators:"
        for j in self.predators:
            print j.getCoordinates()

    def moveFood(self):
        #remove food in tiles
        self.removeFoodInTiles()

        #generate new positions in the food list
        for i in self.food:
            i.setX(i.getX() + random.randint(-1, 1))
            i.setY(i.getY() + random.randint(-1, 1))

        #set new food positions in the tiles
        self.setFoodInTiles()

        print "Here are the food coordinates after moving:"
        for k in self.food:
            print k.getCoordinates()

    def movePredators(self):
        #remove predators in tiles
        self.removePredatorsInTiles()

        #generate new positions in the predator list
        for i in self.predators:
            i.setX(i.getX() + random.randint(-1, 1))
            i.setY(i.getY() + random.randint(-1, 1))

        #set new predator positions in the tiles
        self.setPredatorsInTiles()

        print "Here are the predator coordinates after moving:"
        for k in self.predators:
            print k.getCoordinates()

    def removeFoodInTiles(self):
        for i in self.food:
            tile = self.animats[i.getX()][i.getY()]
            tile[1] = 0

    def removePredatorsInTiles(self):
        for i in self.predators:
            tile = self.animats[i.getX()][i.getY()]
            tile[2] = 0

    def setFoodInTiles(self):
        for i in self.food:
            tile = self.animats[i.getX()][i.getY()]
            tile[1] = 1

    def setPredatorsInTiles(self):
        for i in self.predators:
            tile = self.animats[i.getX()][i.getY()]
            tile[2] = 1

    def timeCycle(self):
        for i in range(self.environmentSize):
            for j in range(self.environmentSize):
                tile = self.animats[i][j]
                if tile[1] == 1 and tile[0].mouthOpen():
                    fed = 1
                else:
                    fed = 0
                if tile[2] == 1 and (not tile[0].hidden()):
                    hurt = 1
                else:
                    hurt = 0
                sounds = self.soundHistory[i][j]
                [make1, make2] = tile[0].timeCyle(sounds[0],sounds[1],fed,hurt)

        #move food
        self.moveFood()

        #move predators
        self.movePredators()

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
#environment.generateRandomFood()
#environment.generateRandomPredators()
#environment.moveFood()
#environment.movePredators()
environment.timeCycle()
#environment.timeCycle()
#environment.trainCycle()

#environment.generateRandomFood()
#environment.generateRandomPredators()
#environment.moveFood()
#environment.movePredators()
