from PerceptronBrain import BrainController
from collections import namedtuple
from random import shuffle, randint

AnimatInputs = namedtuple('AnimatInputs', ['auditoryInputs', 'vocalInputs'])
AnimatOutputs = namedtuple('AnimatOutputs',['auditoryOutputs','vocalOutputs'])

class Animat:
    def __init__(self):
        self.brain = BrainController()
        self.energy = 100
        self.openMouth = -1
        self.scare = -1

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
            auditoryInputs.append(animatInputs.auditoryInputs[i])
            auditoryOutputs.append(animatOutputs.auditoryOutputs[i])
            vocalInputs.append(animatInputs.vocalInputs[i])
            vocalOutputs.append(animatOutputs.vocalOutputs[i])

        error = self.brain.trainAuditory(auditoryInputs, auditoryOutputs, momentum=0.99)
        error += self.brain.trainVocal(vocalInputs, vocalOutputs, momentum=0.99)
        return error

    def getBehaviorString(self):
        auditoryInputs = [[-1],[1]]
        vocalInputs = [[-1],[1]]
        auditoryStrategy = ""
        vocalStrategy = ""
        for i in range(len(auditoryInputs)):
            input = auditoryInputs[i]
            aOut = map(lambda x: 0 if x <= 0 else 1, self.brain.activateAuditory(input))
            auditoryStrategy += ''.join(map(str,aOut))

        for i in range(len(vocalInputs)):
            input = vocalInputs[i]
            vOut = map(lambda x: 0 if x <= 0 else 1, self.brain.activateVocal(input))
            vocalStrategy += ''.join(map(str,vOut))

        return auditoryStrategy + " " + vocalStrategy

    def getTrainingData(self):
        #dataInputs = [(0,0),(1,0),(0,1),(1,1)]
        #dataInputs = [(-1,-1),(-1,1),(1,-1),(1,1)]
        #shuffle(dataInputs)
        auditoryInputs = []
        vocalInputs = []
        auditoryOutputs = []
        vocalOutputs = []
        for i in range(4):
            #input = AnimatInputs(*(dataInputs[i] + dataInputs[j]))
            #output = AnimatsOutputs(*self.brain.activateNetworks(dataInputs[i] + dataInputs[j]))
            #inputs.append(input)
            #outputs.append(output)
            dataInput = []
            for j in range(2):
                dataInput.append(-1 if randint(0,1) == 0 else 1)
            auditoryInputs.append(dataInput[0:1])
            vocalInputs.append(dataInput[1:2])
            o = self.brain.activateNetworks(dataInput)
            auditoryOutputs.append(o[0:1])
            vocalOutputs.append(o[1:3])

        return [AnimatInputs(auditoryInputs,vocalInputs), AnimatOutputs(auditoryOutputs,vocalOutputs)]

    def mouthOpen(self):
        return (self.openMouth > 0)

    def hidden(self):
        return (self.hide > 0)

    def scaring(self):
        return (self.scare > 0)

    def feed(self):
        self.energy += 15

    def timeCyle(self, hear1, nearby, fed):
        """

        @param inputs: a list of 4 floats (hear1, hear2, fed, hurt)
        @return: nothing #a list of 4 integers (openMouth, hide, make1, make2)
        """
        if fed == 1:
            self.feed()
        #if hurt == 1:
        #    self.energy -= 1
        [scare, make1, openMouth] = self.brain.activateNetworks([hear1, nearby])
        if(randint(0,99) < 5):
            self.scare = 1
        else:
            self.scare = scare

        if openMouth == 1:
            self.energy -= 0.5
        #if self.hide == 1:
        #    self.energy -= 0.05
        if self.scare == 1:
            self.energy -= 0.05
        if make1 == 1:
            self.energy -= 0.05
        #if make2 == 1:
        #    self.energy -= 0.05

        return [make1]

    def getSummaryString(self):
        return 'Behavior string: {0}, Energy: {1}'.format(self.getBehaviorString(),self.energy)

#a = Animat()
#a.getTrainingData()