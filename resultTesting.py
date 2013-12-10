from Environment import *
import csv

environment = Environment()
#environment.trainPerfectBlock(11,12,11,12)
testN = 11
cntArray = []
numCenturies = 500

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

    print environment.animats[testN][testN][0].getSummaryString() + "\t\t" + environment.animats[testN+1][testN][0].getSummaryString()
    if (environment.getHealthiestNeighbor(testN,testN)):
        print "(10,10) neighbor: " + environment.getHealthiestNeighbor(testN,testN).getSummaryString()
    if (environment.getHealthiestNeighbor(testN+1,testN)):
        print "(11,10) neighbor: " + environment.getHealthiestNeighbor(testN+1,testN).getSummaryString()
    #print environment.getHealthiestNeighbor(10,10).getSummaryString() + "\t\t" + environment.getHealthiestNeighbor(11,10).getSummaryString() + "\n"

    print cnt.most_common(10)
    print cnt['01 01']

    #print cnt['00011011 0011']
    #print cnt['01 01']


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

createCSV()