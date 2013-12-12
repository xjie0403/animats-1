from random import randint

'''
----------------------------------
Perceptron Class

A perceptron, with randomized initial weights. Can be activated with a given input, or trained
with given input and output
----------------------------------
'''
class Perceptron:
    def __init__(self, numInputs):
        # initialize the network with random weights
        self.possibleWeights = [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5] #map(lambda x: x + 0.5, range(-4,4,1))
        self.weights = []
        for i in range(numInputs):
            ind = randint(0,len(self.possibleWeights) - 1)
            self.weights.append(self.possibleWeights[ind])
        self.biasWeight = self.possibleWeights[randint(0,len(self.possibleWeights)-1)]

    '''
    Activate the perceptron given the inputs, and return a polar output
    '''
    def activate(self,inputs):
        sum = 0;
        for i in range(len(self.weights)):
            sum += self.weights[i] * inputs[i]
        sum += self.biasWeight
        return -1 if sum < 0 else 1

    '''
    Train the perceptron with the given inputs and target output.
        Returns the new output based on the input given.
    '''
    def train(self, inputs, target):
        if(self.activate(inputs) == target): # if we don't need any training, return 0
            return 0
        else:
            # perform a standard weight update
            for i in range(len(self.weights)):
                self.weights[i] = self.weights[i] + target * inputs[i]
            self.biasWeight = self.biasWeight + target
            return self.activate(inputs)

'''
----------------------------------
BrainController Class

The brain of the animat
----------------------------------
'''
class BrainController:
    def __init__(self):
        self.mouthPerceptron = Perceptron(2)
        self.hidePerceptron = Perceptron(2)
        self.make1Perceptron = Perceptron(2)
        self.make2Perceptron = Perceptron(2)

    '''
    Train the auditory network

    @param inputs: a list of lists. The inner list of length 2, the inputs to the network (hear1, hear2)
    @param targets: a list of lists. The inner lists of length 2, the target outputs. (openMouth, hide)
    @param kwargs:
    @return:
    '''
    def trainAuditory(self, inputs, targets, **kwargs):
        sum = 0
        for i in range(len(inputs)):
            target = targets[i]
            sum += abs(self.mouthPerceptron.train(inputs[i],target[0]))
            sum += abs(self.hidePerceptron.train(inputs[i],target[1]))
        return sum
    '''
    Train the vocal network

    @param inputs: list of training inputs (fed, hurt)
    @param targets: list of training targets (make1, make2)
    @param kwargs:
    @return:
    '''
    def trainVocal(self, inputs, targets, **kwargs):
        sum = 0
        for i in range(len(inputs)):
            target = targets[i]
            sum += abs(self.make1Perceptron.train(inputs[i],target[0]))
            sum += abs(self.make2Perceptron.train(inputs[i],target[1]))
        return sum

    '''
    Activate both auditory and vocal networks
    Returns the output of the activation in a list

    @param inputs: a list of 4 floats (hear1, hear2, fed, hurt)
    @return: a list of 4 integers (openMouth, hide, make1, make2)
    '''
    def activateNetworks(self, inputs):
        return self.activateAuditory(inputs[0:2]) + self.activateVocal(inputs[2:4])

    '''
    Activate auditory network
    Returns the output of the activation in a list
    '''
    def activateAuditory(self, inputs): # inputs is a list of 2 numbers
        output = [self.mouthPerceptron.activate(inputs), self.hidePerceptron.activate(inputs)]
        return output

    '''
    Activate vocal network
    Returns the output of the activation in a list
    '''
    def activateVocal(self, inputs): # inputs is a list of 2 numbers
        output = [self.make1Perceptron.activate(inputs), self.make2Perceptron.activate(inputs)]
        return output