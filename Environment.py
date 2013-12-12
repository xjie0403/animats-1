#Environment Class

import random
from collections import Counter
from Animat import Animat, AnimatOutputs, AnimatInputs

'''
----------------------------------
XYValues Class
This class is used as a helper to move food and predators in the
environment. It was created to make movement easier using a
simple coordinate system
----------------------------------
'''
class XYValues:
    
    xValue = 0
    yValue = 0
    def __init__(self):
        self.xValue = 0
        self.yValue = 0
        self.scareCount = 0

    def setX(self, x):
        self.xValue = x

    def setY(self, y):
        self.yValue = y

    def getX(self):
        return self.xValue

    def getY(self):
        return self.yValue

    def incScareCount(self):
        self.scareCount += 1

    def resetScareCount(self):
        self.scareCount = 0

    def maxScareCount(self):
        return 1

    def getScareCount(self):
        return self.scareCount

    def getCoordinates(self):
        return "(" + str(self.xValue) + ", " + str(self.yValue) + ")"

'''
----------------------------------
Environment Class
This class is used to construct the Environment. Animats, food, and
predators are added here. The training methods for animats are called
and inputs and outputs are passed to the Animat class
----------------------------------
'''
class Environment:

    def __init__(self):
        self.environmentSize = 32
        self.numFood = 10
        self.numPredators = 0
        self.animats = []
        self.soundHistory = []
        for i in range(self.environmentSize):
            self.soundHistory.append([])
            self.animats.append([])
            for j in range(self.environmentSize):
                self.animats[i].append([Animat(), -1, -1])
                print self.animats[i][j][0].getBehaviorString()

        # initialize sound images
        self.soundHistory = [[[-1] for j in range(self.environmentSize)] for i in range(self.environmentSize)]

        #initialize food
        self.food = [XYValues() for k in range(self.numFood)]
        self.generateRandomFood()

        #initialize predator
        self.predators = [XYValues() for l in range(self.numPredators)]
        self.generateRandomPredators()

    '''
    Trains the initial perfect animats
    '''
    def trainPerfectBlock(self, begrow, endrow, begcol, endcol):
        for i in range(begrow, endrow+1):
            for j in range(begcol, endcol+1):
                self.trainPerfect(self.animats[i][j][0])

    '''
    Trains a perfect animat
    '''
    def trainPerfect(self, animat, strat=1):
        auditoryInputs = [[-1],[1]]
        vocalInputs = [[-1],[1]]

        if(strat == 1):
            audOutputDict = {'-1': [-1],
                             '1': [1]}
            vocOutputDict = {'-1':[-1],'1':[1]}

        else:
            sampOutputs = [(-1,-1),(1,-1),(-1,1),(1,1)]

        error = 1
        while(error > 0.05):
            audInputs = []
            vocInputs = []
            audOutputs = []
            vocOutputs = []
            for i in auditoryInputs:
                for j in vocalInputs:
                    audInputs.append(i)
                    vocInputs.append(j)
                    audOutputs.append(audOutputDict[''.join(map(str,i))])
                    vocOutputs.append(vocOutputDict[''.join(map(str,j))])

            error = animat.train(AnimatInputs(audInputs,vocInputs), AnimatOutputs(audOutputs,vocOutputs))

    '''
    Generates initial random food in the environment
    '''
    def generateRandomFood(self):
        for i in self.food:
            i.setX(random.randint(0, self.environmentSize - 1))
            i.setY(random.randint(0, self.environmentSize -1))

        #set the food in the tiles for the first time
        self.setFoodInTiles()

        print "Here are the coordinates for the food:"
        for j in self.food:
            print j.getCoordinates()

    '''
    Generates initial random predators in the environment
    '''
    def generateRandomPredators(self):
        for i in self.predators:
            i.setX(random.randint(0, self.environmentSize -1))
            i.setY(random.randint(0, self.environmentSize -1))

        #set the predators in the tiles fo the first time
        self.setPredatorsInTiles()

        print "Here are the coordinates for the predators:"
        for j in self.predators:
            print j.getCoordinates()

    '''
    Goes through each food object and determined whether it is scared or not
    '''
    def computeScares(self):
        scaredFoods = 0
        for foodObj in self.food:
            if(self.checkNeighborScares(foodObj.getX(),foodObj.getY())):
                foodObj.incScareCount()
                if(foodObj.getScareCount() > foodObj.maxScareCount()):
                    foodObj.resetScareCount()
                else:
                    scaredFoods += 1
            else:
                foodObj.resetScareCount()

    '''
    Determines whether there are sufficient number of neighbors to the tile to scare the food object
    Returns a boolean value
    '''
    def checkNeighborScares(self, row, col):
        # keep a table of the scares, so that we can see if we have a full row or col
        scareTable = []

        # keep the number of neighbor scarers. If over a certain threshold we will freeze
        neighborScares = 0

        for i in range(-1,2):
            scareTable.append([])
            for j in range(-1,2):
                if row + i >= len(self.animats):
                    i -= len(self.animats) + 1
                if col + j >= len(self.animats[i]):
                    j -= len(self.animats[i]) + 1
                if(self.animats[row+i][col+j][0].scaring()):
                    neighborScares += 1
                    if(neighborScares >= 3):
                        return True
                scareTable[-1].append(self.animats[row+i][col+j][0].scaring())
        return False

        # go through and talley each row/col, to see if we have a full row of scarers.

        # don't count the animat itself. We want a row/col of 3 not including itself.
        scareTable[1][1] = False
        for i in range(-1,2):
            vertScares = 0
            horizScares = 0
            for j in range(-1,2):
                if(scareTable[i][j] == True):
                    vertScares += 1
                if(scareTable[j][i] == True):
                    horizScares += 1
                if(vertScares >= 3 or horizScares >= 3):
                    return True
        return False

    '''
    Moves the food randomly in one timestep
    '''
    def moveFood(self):
        #remove food in tiles
        self.removeFoodInTiles()

        # go through and increment scare counts on food objects that are scared, resetting if necessary
        self.computeScares()

        #generate new positions in the food list
        for i in self.food:
            if(i.getScareCount() > 0): # don't move the food if it is scared
                continue

            tempX = random.randint(-1, 1)
            if i.getX() == self.environmentSize - 1 and tempX == 1:
                i.setX(0)
            elif i.getX() == 0 and tempX == -1:
                i.setX(self.environmentSize -1)
            else:
                i.setX(i.getX() + tempX)

            tempY = random.randint(-1, 1)
            if i.getY() == self.environmentSize - 1 and tempY == 1:
                i.setY(0)
            elif i.getY() == 0 and tempY == -1:
                i.setY(self.environmentSize -1)
            else:
                i.setY(i.getY() + tempY)

        #set new food positions in the tiles
        self.setFoodInTiles()

    '''
    Moves the predators randomly in one timestep
    '''
    def movePredators(self):
        #remove predators in tiles
        self.removePredatorsInTiles()

        #generate new positions in the predator list
        for i in self.predators:
            tempX = random.randint(-1, 1)
            if i.getX() == self.environmentSize - 1 and tempX == 1:
                i.setX(0)
            elif i.getX() == 0 and tempX == -1:
                i.setX(self.environmentSize -1)
            else:
                i.setX(i.getX() + tempX)

            tempY = random.randint(-1, 1)
            if i.getY() == self.environmentSize - 1 and tempY == 1:
                i.setY(0)
            elif i.getY() == 0 and tempY == -1:
                i.setY(self.environmentSize -1)
            else:
                i.setY(i.getY() + tempY)

        #set new predator positions in the tiles
        self.setPredatorsInTiles()

    '''
    Helper method that removes all food in the array by setting
    the values equal to -1
    '''
    def removeFoodInTiles(self):
        for i in self.food:
            tile = self.animats[i.getX()][i.getY()]
            tile[1] = -1

    '''
    Helper method that removes all predators in the array by setting
    the values equal to -1
    '''
    def removePredatorsInTiles(self):
        for i in self.predators:
            tile = self.animats[i.getX()][i.getY()]
            tile[2] = -1

    '''
    Helper method that sets all the tiles to the values
    in the food array
    '''
    def setFoodInTiles(self):
        for i in self.food:
            tile = self.animats[i.getX()][i.getY()]
            tile[1] = 1

    '''
    Helper method that sets all the tiles to the values
    in the predator array
    '''
    def setPredatorsInTiles(self):
        for i in self.predators:
            tile = self.animats[i.getX()][i.getY()]
            tile[2] = 1

    '''
    Cycle the time - execute a timestep

    This controls the functionality of the environment based
    on the timeCycle this method is called per each timestep
    and moves the food and sets an animats attributes
    '''
    def timeCycle(self):
        newSounds = []
        for i in range(self.environmentSize):
            for j in range(self.environmentSize):
                tile = self.animats[i][j]
                fed = -1
                sounds = self.soundHistory[i][j]
                nearby = 1 if self.foodNearby(i,j) else -1
                [make1] = tile[0].timeCyle(sounds[0], nearby, fed)
                make1 = -1 if make1 <= 0 else 1
                newSounds.append([i, j, make1])

        self.soundHistory = [[[-1] for j in range(self.environmentSize)] for i in range(self.environmentSize)]
        for soundList in newSounds:
            if soundList[2] == 1:
                self.propagateSound(soundList[0],soundList[1],0)

        #move food
        self.moveFood()

        for i in range(self.environmentSize):
            for j in range(self.environmentSize):
                tile = self.animats[i][j]
                if tile[1] == 1:
                    for foodObj in self.food:
                        if foodObj.getX() == i and foodObj.getY() == j and foodObj.getScareCount() > 0:
                            tile[0].feed()
                            break

    '''
    Function that computes whether food is nearby
    an animat (used for scaring)
    '''
    def foodNearby(self, row, col):
        for i in range(-1,2):
            for j in range(-1,2):
                if row + i >= len(self.animats):
                    i -= len(self.animats) + 1
                if col + j >= len(self.animats[i]):
                    j -= len(self.animats[i]) + 1
                if(self.animats[row+i][col+j][1] == 1):
                    return True
        return False

    '''
    Propagates a sound from where it originated to the neighboring tiles
    '''
    def propagateSound(self, row, col, soundnum):
        for i in range(-1,2):
            for j in range(-1,2):
                if row + i >= len(self.animats):
                    i -= len(self.animats) + 1
                if col + j >= len(self.animats[i]):
                    j -= len(self.animats[i]) + 1
                self.soundHistory[row + i][col + j][soundnum] = 1

    '''
    Returns the healthies animat neighbor
    @rtype : Animat
    '''
    def getHealthiestNeighbor(self, row, col):
        bestAnimat = self.animats[row][col][0]
        maintain = True
        for i in range(-1,2):
            for j in range(-1,2):
                # wraparound if the index is too big
                if row + i >= len(self.animats):
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

    '''
    Executes a training cycle. Goes through and trains each animat based on its healthiest neighbor.
    '''
    def trainCycle(self):
        trainingData = []
        for i in range(self.environmentSize):
            trainingData.append([])
            for j in range(self.environmentSize):
                individual = self.animats[i][j][0]
                neighbor = self.getHealthiestNeighbor(i,j)
                if neighbor:
                    trainingData[i].append(neighbor.getTrainingData())
                else:
                    trainingData[i].append(False)

        for i in range(self.environmentSize):
            for j in range(self.environmentSize):
                individual = self.animats[i][j][0]
                neighborData = trainingData[i][j]
                if neighborData:
                    individual.train(*neighborData)

    '''
    Returns the behaviors of the animats
    '''
    def getBehaviors(self):
        cnt = Counter()
        for i in range(self.environmentSize):
            for j in range(self.environmentSize):
                cnt[self.animats[i][j][0].getBehaviorString()] += 1

        return cnt

