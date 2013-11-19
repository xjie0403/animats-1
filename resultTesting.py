from Environment import *

environment = Environment()

for century in range(50):
    print "Beginning century {0}".format(century)
    for round in range(100):
        environment.timeCycle()
    environment.trainCycle()
    print "--Animat 1--\n" + environment.animats[10][10][0].getSummaryString() + "--Animat 2--\n" + environment.animats[11][10][0].getSummaryString()