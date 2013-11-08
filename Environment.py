#Environment Class

import random


class XYValues:
    
    xValue = 0
    yValue = 0

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

    #animats = [[Animats() for i in range(1000)] for j in range(1000)]

    food = [XYValues() for k in range(100)]

    predators = [XYValues() for l in range(100)]


    def generateRandomFood(self):

        for i in self.food:
            i.setX(random.randint(0, 1000))
            i.setY(random.randint(0, 1000))

        print "Here are the coordinates for the food:"
        for j in self.food:
            print j.getCoordinates()


    def generateRandomPredators(self):

        for i in self.predators:
            i.setX(random.randint(0, 1000))
            i.setY(random.randint(0, 1000))

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


environment = Environment()
environment.generateRandomFood()
environment.generateRandomPredators()
environment.moveFood()
environment.movePredators()