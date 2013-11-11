from Environment import *

environment = Environment()

for century in range(30):
    print "Beginning century {0}".format(century)
    for round in range(100):
        environment.timeCycle()
    environment.trainCycle()
    print environment.animats[10][10][0].getBehaviorString()