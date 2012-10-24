class Component(object):
    def __init__(self, type='', footprint=''):
        self.type = type
        self.footprint = footprint
        self.pins = set()
    def add_pin(self, pin):
        self.pins.add(str(pin).strip())

class Netlist(object):
    def __init__(self):
        self.__nets = {} # Netname : dict(designator : list of pins) 
        self.__components = {} # Designator : Component Object
    def add_component(self, designator, footprint='', type=''):
        designator, footprint, type = designator.strip(), footprint.strip(), type.strip()
        if designator in self.__components:
            raise Exception("Duplicate designator %s in netlist" % designator)
        self.__components[designator] = Component(type, footprint)

    def remove_component(self, designator):
        del self.__components[designator]
        nets_to_remove = set() 
        for netname, net in self.__nets.items():
            for designator in net:
                if designator in self.designators:
                    break
                nets_to_remove.add(netname)
        for netname in nets_to_remove:
            del self.__nets[netname]

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

    def pins(self, designator):
        return self.__components[designator].pins

    def who_shares(self, designator, pin):
        net = self.what_net(designator, pin)
        if net:
            return self.on_net(net)
        else:
            return {}

    def get_map(self, c1, c2):
        retval = {}
        for pin in self.pins(c1):
            pins = self.who_shares(c1, pin).get(c2, None)
            if pins:
                retval[pin] = pins
        return retval 

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
