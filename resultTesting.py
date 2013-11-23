from Environment import *

environment = Environment()

for century in range(10):
    print "Beginning century {0}".format(century)
    for round in range(100):
        environment.timeCycle()
    print environment.animats[10][10][0].getSummaryString() + "\t\t" + environment.animats[11][10][0].getSummaryString()
    print environment.getHealthiestNeighbor(10,10).getSummaryString() + "\t\t" + environment.getHealthiestNeighbor(11,10).getSummaryString() + "\n"
    environment.trainCycle()
    cnt = environment.getBehaviors()
    #print cnt.most_common(10)
    #print cnt['00011011 00011011']
    #print cnt['00100111 00100111']
    print environment.animats[10][10][0].getSummaryString() + "\t\t" + environment.animats[11][10][0].getSummaryString()
    print environment.getHealthiestNeighbor(10,10).getSummaryString() + "\t\t" + environment.getHealthiestNeighbor(11,10).getSummaryString() + "\n"