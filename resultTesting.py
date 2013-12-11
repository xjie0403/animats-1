from Environment import *
import csv
from CreateImage import *

environment = Environment()
createImage = CreateImage()
environment.trainPerfectBlock(10,12,10,12)
testN = 5
cntArray = []
numCenturies = 500

'''
----------------------------------
ResultTesting File
This file acts as a controller for the entire program
----------------------------------
'''

#calculates when to save an image pased on the number of images
def calculateWhenToSaveImage(centuries):
    #change the number of images here!
    images = 5
    return centuries/(images-1)

#sets the save point in the iteration based on the value from calculateWhenToSaveImage method
savePoint = calculateWhenToSaveImage(numCenturies)

#for loop is used to call each timeCycle in the environment
for century in range(numCenturies):
    print "Beginning century {0}".format(century)
    for round in range(100):
        environment.timeCycle()
    print environment.animats[testN][testN][0].getSummaryString() + "\t\t" + environment.animats[testN+1][testN][0].getSummaryString()
    if (environment.getHealthiestNeighbor(testN,testN)):
        print "(10,10) neighbor: " + environment.getHealthiestNeighbor(testN,testN).getSummaryString()
    if (environment.getHealthiestNeighbor(testN+1,testN)):
        print "(11,10) neighbor: " + environment.getHealthiestNeighbor(testN+1,testN).getSummaryString()
    #print environment.getHealthiestNeighbor(10,10).getSummaryString() + "\t\t" + environment.getHealthiestNeighbor(11,10).getSummaryString() + "\n"
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
    #print environment.getHealthiestNeighbor(10,10).getSummaryString() + "\t\t" + environment.getHealthiestNeighbor(11,10).getSummaryString() + "\n"

    print cnt.most_common(10)
    print cnt['01 01']
    #numCenturies = numCenturies +1
    #print cnt['00011011 00011011']
    #print cnt['00100111 00100111']

''''
function which creates a CSV file once the program is complete
the CSV file creates columns for each behavior and the number of
occures based on the century
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
    #temporarily return list of behaviors for image
    #return behaviors

#call to the createCSV function
createCSV()
