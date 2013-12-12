from Environment import *
import csv
from CreateImage import *

'''
----------------------------------
ResultTesting File
This file acts as a controller for the entire program
----------------------------------
'''

environment = Environment()
createImage = CreateImage()

# setup an initial block of perfect communicators
environment.trainPerfectBlock(6,10,6,10,1)
environment.trainPerfectBlock(21,25,21,25,2)

testN = 9 # for debugging. Select which animat to debug heavily
cntArray = []
numCenturies = 500

'''
Calculates when to save an image pased on the number of images
'''
def calculateWhenToSaveImage(centuries):
    #change the number of images here!
    images = 5
    return centuries/(images-1)

'''
Sets the save point in the iteration based on the value
from calculateWhenToSaveImage method
'''
savePoint = calculateWhenToSaveImage(numCenturies)

'''
For loop is used to call each timeCycle in the environment
'''
for century in range(numCenturies):
    print "Beginning century {0}".format(century)
    for round in range(100):
        environment.timeCycle()

    environment.trainCycle()
    cnt = environment.getBehaviors()

    #each count object is added to an array
    cntArray.append(cnt)

    imageBehaviors = []

    if ((century+1) % savePoint == 0) or (century == 0):
        for i in list(cntArray[century]):
            imageBehaviors.append(i)

        createImage.createBMP("animatAtCentury"+ str(century) +".bmp", environment.animats, imageBehaviors)


'''
Function which creates a CSV file once the program is complete
the CSV file creates columns for each behavior and the number of
occurs based on the century
'''
def createCSV():
    lastCenturyBehaviors = cntArray[numCenturies-1].most_common(10)

    behaviors = []

    for i in lastCenturyBehaviors:
        behaviors.append(i[0])

    results = [[] for i in range(len(behaviors))]

    resultsCounter = 0
    for i in cntArray:
        tempListOfBehaviors = list(i)
        behaviorCounter = 0
        for j in behaviors:
            if j in tempListOfBehaviors:
                results[behaviorCounter].append(i[j])
            else:
                results[behaviorCounter].append(0)
            behaviorCounter = behaviorCounter +1

    csvMatrix = zip(*results)

    with open('results.csv','wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(behaviors)
            count = 0
            for i in csvMatrix:
                writer.writerow(csvMatrix[count])
                count = count + 1

#call to the createCSV function
createCSV()