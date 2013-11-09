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
        self.environmentSize = 100
        self.animats = []
        for i in range(self.environmentSize):
            self.animats.append([])
            for j in range(self.environmentSize):
                self.animats[i].append([Animat(), 0, 0])

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
                tile = self.animats[i,j]
                if tile[1] == 1 and tile[0].mouthOpen():
                    fed = 1
                else :
                    fed = 0
                if tile[2] == 1 and (not tile[0].hide()):
                    hurt = 1
                else:
                    hurt = 0
                tile[0].timeCyle(0,0,fed,hurt)

environment = Environment()
#environment.generateRandomFood()
#environment.generateRandomPredators()
#environment.moveFood()
#environment.movePredators()