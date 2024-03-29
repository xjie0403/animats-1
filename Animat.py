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
    Trains the network with a given set of inputs and outputs
    @param animatInputs: an AnimatInput object to train on
    @param animatOutputs: an AnimatOutput object to train on
    '''
    def train(self, animatInputs, animatOutputs):
        auditoryInputs = []
        auditoryOutputs = []
        vocalInputs = []
        vocalOutputs = []

        # build the inputs and output lists to train on, from the animatInputs and animatOutputs tuples
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
        dataInputs = [(-1,-1),(-1,1),(1,-1),(1,1)]
        auditoryStrategy = ""
        vocalStrategy = ""

        # go through each possible input and get the outputs of the network
        for i in range(len(dataInputs)):
            input = dataInputs[i]
            aOut = map(lambda x: 0 if x <= 0 else 1, self.brain.activateAuditory(input))
            vOut = map(lambda x: 0 if x <= 0 else 1, self.brain.activateVocal(input))
            auditoryStrategy += str(aOut[0])+str(aOut[1])
            vocalStrategy += str(vOut[0])+str(vOut[1])

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
            for j in range(4):
                dataInput.append(-1 if randint(0,1) == 0 else 1)

            # get the outputs for dataInput and add them to the output training data
            auditoryInputs.append(dataInput[0:2])
            vocalInputs.append(dataInput[2:4])
            o = self.brain.activateNetworks(dataInput)
            auditoryOutputs.append((o[0],o[1]))
            vocalOutputs.append((o[2],o[3]))

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
    Method called each timestep and sets an animats attributes
    @param inputs: a list of 4 floats (hear1, hear2, fed, hurt)
    @return: A list of make1, make2; the sounds that were made by the animat
    '''
    def timeCyle(self, hear1, hear2, fed, hurt):
        if fed == 1:
            self.energy += 1
        if hurt == 1:
            self.energy -= 1
        [openMouth, hide, make1, make2] = self.brain.activateNetworks([hear1, hear2, fed, hurt])

        # Add randomness to the animat behavior
        if(randint(0,99) < 3):
            self.openMouth = 1
        else:
            self.openMouth = openMouth

        if(randint(0,99) < 3):
            self.hide = 1
        else:
            self.hide = hide

        # Enforce energy penalties
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
    Returns a string that summarizes the animat: its current behavior and its energy. Used for debugging.
    '''
    def getSummaryString(self):
        return 'Behavior string: {0}, Energy: {1}'.format(self.getBehaviorString(),self.energy)