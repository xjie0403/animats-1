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

testN = 11
cntArray = []
numCenturies = 500

'''
Calculates when to save an image based on the number of images
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
    print environment.animats[testN][testN][0].getSummaryString() + "\t\t" + environment.animats[testN+1][testN][0].getSummaryString()
    if (environment.getHealthiestNeighbor(testN,testN)):
        print "(10,10) neighbor: " + environment.getHealthiestNeighbor(testN,testN).getSummaryString()
    if (environment.getHealthiestNeighbor(testN+1,testN)):
        print "(11,10) neighbor: " + environment.getHealthiestNeighbor(testN+1,testN).getSummaryString()

    environment.trainCycle()
    cnt = environment.getBehaviors()

    #each count object is added to an array
    cntArray.append(cnt)
    imageBehaviors = []

    if ((century+1) % savePoint == 0) or (century == 0):
        for i in list(cntArray[century]):
            imageBehaviors.append(i)

        createImage.createBMP("animatAtCentury"+ str(century) +".bmp", environment.animats, imageBehaviors)

    print environment.animats[testN][testN][0].getSummaryString() + "\t\t" + environment.animats[testN+1][testN][0].getSummaryString()
    if (environment.getHealthiestNeighbor(testN,testN)):
        print "(10,10) neighbor: " + environment.getHealthiestNeighbor(testN,testN).getSummaryString()
    if (environment.getHealthiestNeighbor(testN+1,testN)):
        print "(11,10) neighbor: " + environment.getHealthiestNeighbor(testN+1,testN).getSummaryString()

    print cnt.most_common(10)
    print cnt['01 01']

'''
Function which creates a CSV file once the program is complete
the CSV file creates columns for each behavior and the number of
occurs based on the century
'''
def createCSV():
    lastCenturyBehaviors = cntArray[numCenturies-1]
    behaviors = []

    for i in list(lastCenturyBehaviors):
        behaviors.append(i)

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