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

    '''
    takes the animatInputs and animatOutputs as parameters and
    adds the inputs and outputs to a list and computes the error
    @param animatInputs: an AnimatInput object to train on
    @param animatOutputs: an AnimatOutput object to train on
    '''
    def train(self, animatInputs, animatOutputs):
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

    '''
    returns the auditory and vocal strategy
    '''
    def getBehaviorString(self):
        dataInputs = [(-1,-1),(-1,1),(1,-1),(1,1)]
        auditoryStrategy = ""
        vocalStrategy = ""
        for i in range(len(dataInputs)):
            input = dataInputs[i]
            aOut = map(lambda x: 0 if x <= 0 else 1, self.brain.activateAuditory(input))
            vOut = map(lambda x: 0 if x <= 0 else 1, self.brain.activateVocal(input))
            auditoryStrategy += str(aOut[0])+str(aOut[1])
            vocalStrategy += str(vOut[0])+str(vOut[1])
        return auditoryStrategy + " " + vocalStrategy

    '''
    returns the inputs and outputs
    '''
    def getTrainingData(self):
        auditoryInputs = []
        vocalInputs = []
        auditoryOutputs = []
        vocalOutputs = []
        for i in range(4):
            dataInput = []
            for j in range(4):
                dataInput.append(-1 if randint(0,1) == 0 else 1)
            auditoryInputs.append(dataInput[0:2])
            vocalInputs.append(dataInput[2:4])
            o = self.brain.activateNetworks(dataInput)
            auditoryOutputs.append((o[0],o[1]))
            vocalOutputs.append((o[2],o[3]))

        return [AnimatInputs(auditoryInputs,vocalInputs), AnimatOutputs(auditoryOutputs,vocalOutputs)]

    '''
    returns true if the mouth is open
    '''
    def mouthOpen(self):
        return (self.openMouth > 0)

    '''
    returns hidden if the animat is hidden
    '''
    def hidden(self):
        return (self.hide > 0)

    '''
    method called each timestep and sets an animats attributes
    @param inputs: a list of 4 floats (hear1, hear2, fed, hurt)
    @return: nothing #a list of 4 integers (openMouth, hide, make1, make2)
    '''
    def timeCyle(self, hear1, hear2, fed, hurt):
        if fed == 1:
            self.energy += 1
        if hurt == 1:
            self.energy -= 1
        [openMouth, hide, make1, make2] = self.brain.activateNetworks([hear1, hear2, fed, hurt])
        if(randint(0,99) < 3):
            self.openMouth = 1
        else:
            self.openMouth = openMouth

        if(randint(0,99) < 3):
            self.hide = 1
        else:
            self.hide = hide

        if self.openMouth == 1:
            self.energy -= 0.05
        if self.hide == 1:
            self.energy -= 0.05
        if make1 == 1:
            self.energy -= 0.05
        if make2 == 1:
            self.energy -= 0.05

        return [make1, make2]

    '''
    returns a string of behaviors
    '''
    def getSummaryString(self):
        return 'Behavior string: {0}, Energy: {1}'.format(self.getBehaviorString(),self.energy)