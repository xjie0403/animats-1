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
        self.numFood = 25
        self.numPredators = 50
        self.animats = []
        self.soundHistory = []
        for i in range(self.environmentSize):
            self.soundHistory.append([])
            self.animats.append([])
            for j in range(self.environmentSize):
                self.animats[i].append([Animat(), -1, -1])
                print self.animats[i][j][0].getBehaviorString()

        #initialize sound history
        self.soundHistory = [[[-1, -1] for j in range(self.environmentSize)] for i in range(self.environmentSize)]

        #initialize food
        self.food = [XYValues() for k in range(self.numFood)]

        #generate food for the first time
        self.generateRandomFood()

        #initialize predator
        self.predators = [XYValues() for l in range(self.numPredators)]

        #generate predators for the first time
        self.generateRandomPredators()

    '''
    Trains a block of initial perfect animats
    '''
    def trainPerfectBlock(self, begrow, endrow, begcol, endcol, strat=1):
        for i in range(begrow, endrow+1):
            for j in range(begcol, endcol+1):
                self.trainPerfect(self.animats[i][j][0],strat=strat)

    '''
    Trains a perfect animat
    '''
    def trainPerfect(self, animat, strat=1):
        sampInputs = [(-1,-1),(-1,1),(1,-1),(1,1)]
        ind = [0, 1, 2, 3]
        random.shuffle(ind)
        if(strat == 1):
            sampOutputs = [(-1,-1),(-1,1),(1,-1),(1,1)]
        else:
            sampOutputs = [(-1,-1),(1,-1),(-1,1),(1,1)]

        error = 1
        while(error > 0.05):
            sampInputs = [ sampInputs[i] for i in ind]
            sampOutputs = [ sampOutputs[i] for i in ind]
            error = animat.train(AnimatInputs(sampInputs*50,sampInputs*50), AnimatOutputs(sampOutputs*50,sampOutputs*50))
            print error

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
    Moves the food randomly in one timestep
    '''
    def moveFood(self):
        #remove food in tiles
        self.removeFoodInTiles()

        #generate new positions in the food list
        for i in self.food:
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
        newSounds = [] # the sounds made in this timestep

        # Go through and evaluate each animat according to its inputs. Record the sounds that it makes
        for i in range(self.environmentSize):
            for j in range(self.environmentSize):
                tile = self.animats[i][j]
                if tile[1] == 1 and tile[0].mouthOpen():
                    fed = 1
                else:
                    fed = -1
                if tile[2] == 1 and (not tile[0].hidden()):
                    hurt = 1
                else:
                    hurt = -1
                sounds = self.soundHistory[i][j]
                [make1, make2] = tile[0].timeCyle(sounds[0],sounds[1],fed,hurt)
                make1 = -1 if make1 <= 0 else 1
                make2 = -1 if make2 <= 0 else 1
                newSounds.append([i, j, make1, make2])

        # reset the sounds in the environment and go through adding the new sounds that were just made
        self.soundHistory = [[[-1, -1] for j in range(self.environmentSize)] for i in range(self.environmentSize)]
        for soundList in newSounds:
            if(soundList[2] == 1):
                self.propagateSound(soundList[0],soundList[1],0)
            if(soundList[3] == 1):
                self.propagateSound(soundList[0],soundList[1],1)

        #move food
        self.moveFood()

        #move predators
        self.movePredators()

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
    Returns the healthiest neighbor given a row and column
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
        # get the training data for every animat in the environment
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

        # go through each animat, and execute the training
        for i in range(self.environmentSize):
            for j in range(self.environmentSize):
                individual = self.animats[i][j][0]
                neighborData = trainingData[i][j];
                if neighborData: # if no neighborData exists, this means that the animat didn't have any neighbors
                                 # healthier than itself, and we don't need to train
                    individual.train(*neighborData)

    '''
    Returns a counter for the behavior strings of the animats
    '''
    def getBehaviors(self):
        cnt = Counter()
        for i in range(self.environmentSize):
            for j in range(self.environmentSize):
                cnt[self.animats[i][j][0].getBehaviorString()] += 1

        return cnt
