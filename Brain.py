from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection

class Brain:
    def __init__(self):
        self.auditoryNetwork = FeedForwardNetwork('auditory')
        self._initializeNetwork(self.auditoryNetwork)
        self.vocalNetwork = FeedForwardNetwork('vocal')
        self._initializeNetwork(self.vocalNetwork)


    def _initializeNetwork(self, net):
        inLayer = LinearLayer(2,'in')
        hiddenLayer = SigmoidLayer(2,'hidden')
        outLayer = SigmoidLayer(2,'out')
        net.addInputModule(inLayer)
        net.addModule(hiddenLayer)
        net.addOutputModule(outLayer)
        in_to_hidden = FullConnection(inLayer, hiddenLayer)
        hidden_to_out = FullConnection(hiddenLayer, outLayer)
        net.addConnection(in_to_hidden)
        net.addConnection(hidden_to_out)
        net.sortModules()
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