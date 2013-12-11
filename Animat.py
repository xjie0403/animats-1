from PerceptronBrain import BrainController
from collections import namedtuple
from random import shuffle, randint

AnimatInputs = namedtuple('AnimatInputs', ['auditoryInputs', 'vocalInputs'])
AnimatOutputs = namedtuple('AnimatOutputs',['auditoryOutputs','vocalOutputs'])

'''
----------------------------------
Animat Class
This class defines each animat object
----------------------------------
'''
class Animat:
    def __init__(self):
        self.brain = BrainController()
        self.energy = 100
        self.openMouth = 0
        self.hide = 0

    #takes the animatInputs and animatOutputs as parameters
    #adds the inputs and outputs to a list and computes the error
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

    #returns the auditory and vocal strategy
    def getBehaviorString(self):
        dataInputs = [(-1),(1)]
        auditoryStrategy = ""
        vocalStrategy = ""
        for i in range(len(dataInputs)):
            input = [dataInputs[i]]
            aOut = map(lambda x: 0 if x <= 0 else 1, self.brain.activateAuditory(input))
            vOut = map(lambda x: 0 if x <= 0 else 1, self.brain.activateVocal(input))
            auditoryStrategy += str(aOut[0])
            vocalStrategy += str(vOut[0])
        return auditoryStrategy + " " + vocalStrategy

    #returns the inputs and outputs
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
            auditoryOutputs.append([o[0]])
            vocalOutputs.append([o[1]])

        return [AnimatInputs(auditoryInputs,vocalInputs), AnimatOutputs(auditoryOutputs,vocalOutputs)]

    #returns true if the mouth is open
    def mouthOpen(self):
        return (self.openMouth > 0)

    #returns hidden if the animat is hidden
    def hidden(self):
        return (self.hide > 0)

    #method called each timestep and sets an animats attributes
    def timeCyle(self, hear1, fed):
        """

        @param inputs: a list of 4 floats (hear1, hear2, fed, hurt)
        @return: nothing #a list of 4 integers (openMouth, hide, make1, make2)
        """
        if fed == 1:
            self.energy += 1
        #if hurt == 1:
        #    self.energy -= 1
        [openMouth, make1] = self.brain.activateNetworks([hear1, fed])
        if(randint(0,99) < 5):
            self.openMouth = 1
        else:
            self.openMouth = openMouth

        #if(randint(0,99) < 5):
        #    self.hide = 1
        #else:
        #    self.hide = hide

        if self.openMouth == 1:
            self.energy -= 0.05
        #if self.hide == 1:
        #    self.energy -= 0.05
        if make1 == 1:
            self.energy -= 0.05
        #if make2 == 1:
        #    self.energy -= 0.05

        return [make1]

    #returns a string of behaviors
    def getSummaryString(self):
        return 'Behavior string: {0}, Energy: {1}'.format(self.getBehaviorString(),self.energy)

#a = Animat()
#a.getTrainingData()