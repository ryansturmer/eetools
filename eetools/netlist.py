class Component(object):
    def __init__(self, type='', footprint=''):
        self.type = type
        self.footprint = footprint
        self.pins = set()
    def add_pin(self, pin):
        self.pins.add(str(pin).strip())

class Netlist(object):
    def __init__(self):
        self.__nets = {}
        self.__components = {}
    def add_component(self, designator, footprint='', type=''):
        designator, footprint, type = designator.strip(), footprint.strip(), type.strip()
        if designator in self.__components:
            raise Exception("Duplicate designator %s in netlist" % designator)
        self.__components[designator] = Component(type, footprint)

    def add_to_net(self, net_name, designator, pin):
        net_name, designator, pin = net_name.strip(), designator.strip(), pin.strip()
        if designator not in self.__components:
            print self.components
            raise Exception("Designator %s not found in attempt to add pins to net." % designator)
        component = self.__components[designator]
        component.add_pin(pin)
        if net_name not in self.__nets:
            self.__nets[net_name] = {}
        
        net = self.__nets[net_name]
        if designator not in net:
            net[designator] = []

        net[designator].append(pin)

    def on_net(self, net_name):
        return self.__nets[net_name]

    def what_net(self, designator, pin):
        designator, pin = str(designator).strip(), str(pin).strip()
        for net_name, net in self.__nets.items():
            if designator in net and pin in net[designator]:
                return net_name
    @property
    def nets(self):
        return self.__nets.keys()
    @property
    def designators(self):
        return self.__components.keys()
    
    @staticmethod
    def load(filename):
        netlist = Netlist()
        with open(filename) as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                if line.strip() == '[':
                    designator,footprint,type = [fp.readline() for i in range(3)]
                    [fp.readline() for i in range(3)]
                    line = fp.readline()
                    if line.strip() != ']':
                        raise Exception("Malformed netlist file.  Expected ']' but got '%s'" % line)
                    netlist.add_component(designator, footprint, type)

                elif line.strip() == '(':
                    net_name = fp.readline().strip()
                    line = fp.readline().strip()
                    while line != ')':
                        designator, pin = line.split(',')
                        netlist.add_to_net(net_name, designator, pin)
                        line = fp.readline().strip()
        return netlist

def load(filename):
    return Netlist.load(filename)
