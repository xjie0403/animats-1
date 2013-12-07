from Environment import *

environment = Environment()
#environment.trainPerfectBlock(11,12,11,12)
testN = 11
for century in range(500):
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