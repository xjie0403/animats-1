from Brain import BrainController
from collections import namedtuple
from random import shuffle, randint

AnimatInputs = namedtuple('AnimatInputs', ['auditoryInputs', 'vocalInputs'])
AnimatOutputs = namedtuple('AnimatOutputs',['auditoryOutputs','vocalOutputs'])

class Animat:
    def __init__(self):
        self.brain = BrainController()
        self.energy = 100
        self.openMouth = 0
        self.hide = 0

    def train(self, animatInputs, animatOutputs):
        """
        @param animatInputs: an AnimatInput object to train on
        @param animatOutputs: an AnimatOutput object to train on
        """
        auditoryInputs = []
        auditoryOutputs = []
        vocalInputs = []
        vocalOutputs = []
        for i in range(len(animatInputs.auditoryInputs)):
            for j in range(10):
                auditoryInputs.append(animatInputs.auditoryInputs[i])
                auditoryOutputs.append(animatOutputs.auditoryOutputs[i])
                vocalInputs.append(animatInputs.vocalInputs[i])
                vocalOutputs.append(animatOutputs.vocalOutputs[i])

        error = self.brain.trainAuditory(auditoryInputs, auditoryOutputs, momentum=0.99)
        error += self.brain.trainVocal(vocalInputs, vocalOutputs, momentum=0.99)
        return error

    def getBehaviorString(self):
        dataInputs = [(-1,-1),(-1,1),(1,-1),(1,1)]
        auditoryStrategy = ""
        vocalStrategy = ""
        for i in range(len(dataInputs)):
            input = dataInputs[i]
            aOut = self.brain.activateAuditory(input)
            vOut = self.brain.activateVocal(input)
            auditoryStrategy += str(aOut[0])+str(aOut[1])
            vocalStrategy += str(vOut[0])+str(vOut[1])
        return auditoryStrategy + " " + vocalStrategy

    def getTrainingData(self):
        #dataInputs = [(0,0),(1,0),(0,1),(1,1)]
        dataInputs = [(-1,-1),(-1,1),(1,-1),(1,1)]
        shuffle(dataInputs)
        inputs = []
        auditoryOutputs = []
        vocalOutputs = []
        for i in range(len(dataInputs)):
            #input = AnimatInputs(*(dataInputs[i] + dataInputs[j]))
            #output = AnimatsOutputs(*self.brain.activateNetworks(dataInputs[i] + dataInputs[j]))
            #inputs.append(input)
            #outputs.append(output)
            o = self.brain.activateNetworks(dataInputs[i]+dataInputs[i])
            auditoryOutputs.append((o[0],o[1]))
            vocalOutputs.append((o[2],o[3]))

        return [AnimatInputs(dataInputs,dataInputs), AnimatOutputs(auditoryOutputs,vocalOutputs)]

    def mouthOpen(self):
        return self.openMouth

    def hidden(self):
        return self.hide

    def timeCyle(self, hear1, hear2, fed, hurt):
        """

        @param inputs: a list of 4 floats (hear1, hear2, fed, hurt)
        @return: nothing #a list of 4 integers (openMouth, hide, make1, make2)
        """
        if fed == 1:
            self.energy += 1
        if hurt == 1:
            self.energy -= 1
        [openMouth, hide, make1, make2] = self.brain.activateNetworks([hear1, hear2, fed, hurt])
        if(randint(0,99) < 5):
            self.openMouth = 1
        else:
            self.openMouth = openMouth

        self.hide = hide

        if self.openMouth == 1:
            self.energy -= 0.05
        if hide == 1:
            self.energy -= 0.05
        if make1 == 1:
            self.energy -= 0.05
        if make2 == 1:
            self.energy -= 0.05

        return [make1, make2]

    def getSummaryString(self):
        return 'Behavior string: {0}, Energy: {1}'.format(self.getBehaviorString(),self.energy)

#a = Animat()
#a.getTrainingData()