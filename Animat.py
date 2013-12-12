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
        self.openMouth = -1
        self.scare = -1

    '''
    Trains the network with a given set of inputs and outputs
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
    Returns the binary string that encodes the animat behavior
    '''
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

    '''
    Returns data that another animat can train on
    '''
    def getTrainingData(self):
        # the training data that we're going to build
        auditoryInputs = []
        vocalInputs = []
        auditoryOutputs = []
        vocalOutputs = []
        for i in range(4): # get four rounds of training data
            dataInput = []
            for j in range(2):
                dataInput.append(-1 if randint(0,1) == 0 else 1)

            # get the outputs for dataInput and add them to the output training data
            auditoryInputs.append(dataInput[0:1])
            vocalInputs.append(dataInput[1:2])
            o = self.brain.activateNetworks(dataInput)
            auditoryOutputs.append(o[0:1])
            vocalOutputs.append(o[1:2])

        return [AnimatInputs(auditoryInputs,vocalInputs), AnimatOutputs(auditoryOutputs,vocalOutputs)]

    '''
    Returns true if the mouth is open
    '''
    def mouthOpen(self):
        return (self.openMouth > 0)

    '''
    Returns true if the animat is hidden
    '''
    def hidden(self):
        return (self.hide > 0)

    '''
    Returns true if animat is scaring
    '''
    def scaring(self):
        return (self.scare > 0)

    '''
    adds 10 energy points to the animat (used when
    fed using scaring method)
    '''
    def feed(self):
        self.energy += 10

    '''
    Method called each timestep and sets an animats attributes
    @param inputs: a list of 4 floats (hear1, hear2, fed, hurt)
    @return: A list of make1, make2; the sounds that were made by the animat
    '''
    def timeCyle(self, hear1, nearby, fed):
        if fed == 1:
            self.feed()

        [scare, make1] = self.brain.activateNetworks([hear1, nearby])

        self.scare = scare

        if self.scare == 1:
            self.energy -= 0.05
        if make1 == 1:
            self.energy -= 0.05

        return [make1]

    '''
    Returns a string that summarizes the animat: its current
    behavior and its energy. Used for debugging.
    '''
    def getSummaryString(self):
        return 'Behavior string: {0}, Energy: {1}'.format(self.getBehaviorString(),self.energy)
