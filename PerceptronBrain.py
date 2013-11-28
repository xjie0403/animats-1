from random import randint

class Perceptron:

    def __init__(self, numInputs):
        self.possibleWeights = [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5] #map(lambda x: x + 0.5, range(-4,4,1))
        self.weights = []
        for i in range(numInputs):
            ind = randint(0,len(self.possibleWeights) - 1)
            self.weights.append(self.possibleWeights[ind])
        self.biasWeight = self.possibleWeights[randint(0,len(self.possibleWeights)-1)]

    def activate(self,inputs):
        sum = 0;
        for i in range(len(self.weights)):
            sum += self.weights[i] * inputs[i]
        sum += self.biasWeight
        return -1 if sum < 0 else 1

    def train(self, inputs, target):
        if(self.activate(inputs) == target):
            return 0
        else:
            for i in range(len(self.weights)):
                self.weights[i] = self.weights[i] + target * inputs[i]
            self.biasWeight = self.biasWeight + target
            return abs(self.activate(inputs) - target)

class BrainController:
    def __init__(self):
        self.mouthPerceptron = Perceptron(1)
        #self.hidePerceptron = Perceptron(2)
        self.make1Perceptron = Perceptron(1)
        self.make2Perceptron = Perceptron(1)
        self.scarePerceptron = Perceptron(1)
        #self.make2Perceptron = Perceptron(2)

    def trainAuditory(self, inputs, targets, **kwargs):
        """

        @param inputs: a list of lists. The inner list of length 2, the inputs to the network (hear1, hear2)
        @param targets: a list of lists. The inner lists of length 2, the target outputs. (openMouth, hide)
        @param kwargs:
        @return:
        """
        sum = 0
        for i in range(len(inputs)):
            target = targets[i]
            sum += abs(self.mouthPerceptron.train(inputs[i][0:1],target[0]))
            sum += abs(self.scarePerceptron.train(inputs[i][1:2],target[1]))
            #sum += abs(self.hidePerceptron.train(inputs[i],target[1]))
        return sum

    def trainVocal(self, inputs, targets, **kwargs):
        """

        @param inputs: list of training inputs (fed, hurt)
        @param targets: list of training targets (make1, make2)
        @param kwargs:
        @return:
        """
        sum = 0
        for i in range(len(inputs)):
            target = targets[i]
            sum += abs(self.make1Perceptron.train(inputs[i],target[0]))
            sum += abs(self.make2Perceptron.train(inputs[i],target[1]))
            #sum += abs(self.make2Perceptron.train(inputs[i],target[1]))
        return sum

    def activateNetworks(self, inputs):
        """

        @param inputs: a list of 4 floats (hear1, hear2, fed, hurt)
        @return: a list of 4 integers (openMouth, hide, make1, make2)
        """

        return self.activateAuditory(inputs[0:2]) + self.activateVocal(inputs[2:3])

    def activateAuditory(self, inputs): # inputs is a list of 2 numbers
        output = [self.mouthPerceptron.activate(inputs[0:1]), self.scarePerceptron.activate(inputs[1:2])]
        return output

    def activateVocal(self, inputs): # inputs is a list of 1 numbers
        output = [self.make1Perceptron.activate(inputs), self.make2Perceptron.activate(inputs)]
        return output