from Brain import BrainController
from collections import namedtuple

AnimatInputs = namedtuple('AnimatInputs', ['hear1', 'hear2', 'fed', 'hurt'])
AnimatsOutputs = namedtuple('AnimatsOutputs',['make1','make2','openMouth','hide'])

class Animat:
    def __init__(self):
        self.brain = BrainController()
        self.energy = 100
        self.openMouth = 0
        self.hide = 0
    def train(self, animatInputs, animatOutputs):
        """
        @param animatInputs: a list of AnimatInput objects to train on
        @param animatOutputs: a list of AnimatOutput objects to train on
        """
        auditoryInputs = []
        auditoryOutputs = []
        vocalInputs = []
        vocalOutputs = []
        for i in range(len(animatInputs)):
            input = animatInputs[i]
            output = animatOutputs[i]
            auditoryInputs.append([input.hear1, input.hear2])
            auditoryOutputs.append([output.openMouth, output.hide])
            vocalInputs.append([input.fed, input.hurt])
            vocalOutputs.append([output.make1, output.make2])
        self.brain.trainAuditory(auditoryInputs, auditoryOutputs)
        self.brain.trainVocal(vocalInputs, vocalOutputs)


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

    def mouthOpen(self):
        return self.openMouth

    def hide(self):
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
        self.openMouth = openMouth
        self.hide = hide

        if openMouth == 1:
            self.energy -= 0.05
        if hide == 1:
            self.energy -= 0.05
        if make1 == 1:
            self.energy -= 0.05
        if make2 == 1:
            self.energy -= 0.05

        return [make1, make2]


#a = Animat()
#a.getTrainingData()