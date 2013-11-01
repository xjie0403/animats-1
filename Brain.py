from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection, BiasUnit
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork

class Brain:
    def __init__(self):
        self.auditoryNetwork = FeedForwardNetwork('auditory')
        self._initializeNetwork(self.auditoryNetwork)
        self.vocalNetwork = FeedForwardNetwork('vocal')
        self._initializeNetwork(self.vocalNetwork)


    def _initializeNetwork(self, net):
        #bias = BiasUnit('bias')
        net.addInputModule(LinearLayer(2,'in'))
        net.addModule(SigmoidLayer(2,'hidden'))
        net.addOutputModule(SigmoidLayer(2,'out'))
        net.addModule(BiasUnit('bias'))
        net.addConnection(FullConnection(net['in'], net['hidden']))
        net.addConnection(FullConnection(net['hidden'], net['out']))
        net.addConnection(FullConnection(net['bias'],net['hidden']))
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

    """
    Most common kwargs are "verbose=True", "momentum=0.99"
    """
    def trainAuditory(self, inputs, outputs, **kwargs):
        return self._train(inputs, outputs, self.auditoryNetwork, **kwargs)

    def trainVocal(self, inputs, outputs, **kwargs):
        return self._train(inputs, outputs, self.auditoryNetwork, **kwargs)

sampleInputData = ((0,0),(1,0),(0,1),(1,1))
sampleOutputData = ((0,0),(1,0),(0,1),(1,1))

b = Brain()

def testTraining():
    b = Brain()
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