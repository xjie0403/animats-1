from Brain import BrainController
from collections import namedtuple

AnimatInputs = namedtuple('AnimatInputs', ['hear1', 'hear2', 'fed', 'hurt'])
AnimatsOutputs = namedtuple('AnimatsOutputs',['make1','make2','openMouth','hide'])

class Animat:
    def __init__(self):
        self.brain = BrainController()

    def train(self, animatInputs, animatOutputs):
        """

        @param animatInputs: a list of AnimatInput objects to train on
        @param animatOutputs: a list of AnimatOutput objects to train on
        """
        for i in len(animatInputs):
            input = animatInputs[i]
            output = animatOutputs[i]
            self.brain.trainAuditory([input.hear1, input.hear2],
                                     [output.openMouth, output.hide])
            self.brain.trainVocal([input.fed, input.hurt],
                                  [output.make1, output.make2])

    def getTrainingData(self):
        dataInputs = [(0,0),(1,0),(0,1),(1,1)]
        inputs = []
        outputs = []
        for i in range(len(dataInputs)):
            for j in range(len(dataInputs)):
                input = AnimatInputs(*(dataInputs[i] + dataInputs[j]))
                output = AnimatsOutputs(*self.brain.activateNetworks(dataInputs[i] + dataInputs[j]))
                inputs.append(input)
                outputs.append(output)

        return [inputs, outputs]

#a = Animat()
#a.getTrainingData()