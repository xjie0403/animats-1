from Environment import *

environment = Environment()

for century in range(50):
    print "Beginning century {0}".format(century)
    for round in range(100):
        environment.timeCycle()
    environment.trainCycle()
    print environment.animats[10][10][0].getSummaryString() + "\t\t" + environment.animats[11][10][0].getSummaryString()
    print environment.getHealthiestNeighbor(10,10).getSummaryString() + "\t\t" + environment.getHealthiestNeighbor(11,10).getSummaryString() + "\n"