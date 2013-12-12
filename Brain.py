from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection, BiasUnit
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.tools.shortcuts import buildNetwork

class BrainController:
    def __init__(self):
        self.auditoryNetwork = FeedForwardNetwork('auditory')
        self._initializeNetwork(self.auditoryNetwork)
        self.vocalNetwork = FeedForwardNetwork('vocal')
        self._initializeNetwork(self.vocalNetwork)


    def _initializeNetwork(self, net):
        #bias = BiasUnit('bias')
        net.addInputModule(LinearLayer(2,'in'))
        net.addOutputModule(SigmoidLayer(2,'out'))
        net.addModule(BiasUnit('bias'))
        net.addConnection(FullConnection(net['in'], net['out']))
        net.addConnection(FullConnection(net['bias'],net['out']))

        net.sortModules()

    def _train(self, inputs, outputs, net, **kwargs):
        if(len(inputs[0]) != 2):
            raise Exception("Need 2 inputs for each data sample, received " + str(len(inputs[0])))
        if(len(outputs[0]) != 2):
            raise Exception("Need 2 outputs for each data sample, received " + str(len(outputs[0])))

        ds = SupervisedDataSet(2,2)
        for i in range(len(inputs)):
            ds.addSample(inputs[i],outputs[i])

        trainer = BackpropTrainer(net, ds, **kwargs)
        return trainer.train()

    def trainAuditory(self, inputs, targets, **kwargs):
        """

        @param inputs: a list of lists. The inner list of length 2, the inputs to the network (hear1, hear2)
        @param targets: a list of lists. The inner lists of length 2, the target outputs. (openMouth, hide)
        @param kwargs:
        @return:
        """
        return self._train(inputs, targets, self.auditoryNetwork, **kwargs)

    def trainVocal(self, inputs, targets, **kwargs):
        """

        @param inputs: list of training inputs (fed, hurt)
        @param targets: list of training targets (make1, make2)
        @param kwargs:
        @return:
        """
        return self._train(inputs, targets, self.vocalNetwork, **kwargs)

    def activateNetworks(self, inputs):
        """

        @param inputs: a list of 4 floats (hear1, hear2, fed, hurt)
        @return: a list of 4 integers (openMouth, hide, make1, make2)
        """
        return map(lambda x: int(round(x)), self.auditoryNetwork.activate(inputs[0:2]).tolist() +
                                            self.vocalNetwork.activate(inputs[2:4]).tolist())

    def activateVocal(self, inputs): # inputs is a list of 2 numbers
        return map(lambda x: int(round(x)), self.vocalNetwork.activate(inputs))

    def activateAuditory(self, inputs): # inputs is a list of 2 numbers
        return map(lambda x: int(round(x)), self.auditoryNetwork.activate(inputs))

sampleInputData = ((0,0),(1,0),(0,1),(1,1))
sampleOutputData = ((0,0),(1,0),(0,1),(1,1))

b = BrainController()

def testTraining():
    b = BrainController()
    b.trainAuditory(sampleInputData*100,sampleOutputData*100)

"""
x = Brain()
net = x.auditoryNetwork

for mod in net.modules:
  print "Module:", mod.name
  if mod.paramdim > 0:
    print "--parameters:", mod.params
  for conn in net.connections[mod]:
    print "-connection to", conn.outmod.name
    if conn.paramdim > 0:
       print "- parameters", conn.params
  if hasattr(net, "recurrentConns"):
    print "Recurrent connections"
    for conn in net.recurrentConns:
       print "-", conn.inmod.name, " to", conn.outmod.name
       if conn.paramdim > 0:
          print "- parameters", conn.params
"""