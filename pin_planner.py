import tableview 

def listify(x):
    if isinstance(x, str) or isinstance(x, unicode):
        return [x]
    else:
        try:
            iter(x)
            return list(x)
        except:
            return [x]

class PinMap(object):
    '''
    The PinMap represents a mapping of IC pins to a set of functions.  It is
    meant to be used in situations where IC functions must be mapped to pins
    that potentially have multiple functions.  A PinMap is loaded from a text/csv
    file (See the load() function for details) and the pins are 'claimed' by name.
    The PinMap object maintains a registry of pins, keeping track of which pins
    have been claimed, and for what purposes.
    '''
    def __init__(self, data):
        self.data = data
        self.peripherals = set()
        self.name = ''
        for functions, remap_functions in self.data.values():
            for f in functions:
                self.peripherals.add(f.strip().lower())
            for f in remap_functions:
                self.peripherals.add(f.strip().lower())
        self.reset()


    def reset(self):
        '''
        Clear any claims on pins or functions.  (Fresh new PinMap)
        '''
        self.__claimed_functions = set()
        self.__claimed_pins = set()
        self.__purposes = {}

    def has(self, function):
        '''
        True if this pin map has the provided function
        '''
        return function.strip().lower() in self.peripherals

    def pins_for(self, *functions):
        '''
        Return a list of all possible pins that can be used for the provided functions (including remapping)
        '''
        retval = []
        for p in functions:
            retval.extend(self.__pins_for(p))
        return retval

    def __pins_for(self, peripheral):
        p = []
        peripheral = peripheral.strip().lower()
        if self.has(peripheral):
            for k,(f,af) in self.data.items():
                if peripheral in f or peripheral in af:
                    p.append(k)
        return p

    def who_shares(self, *functions):
        '''
        Given some functions, what other functions use the same pins?
        '''
        return self.functions_of(*self.pins_for(*functions))

    def functions_of(self, *pins):
        '''
        Return a list of all the functions that use the provided pins
        '''
        retval = []
        for pin in pins:
            retval.extend(self.data[pin][0])
            retval.extend(self.data[pin][1])
        return retval

    def functions_like(self, function):
        '''
        Given a partial function name, return all the functions that match it.
        For example: 'spi1' -> ['spi1_miso','spi1_mosi','spi1_sck','spi1_cs']
        '''
        retval = []
        function = function.strip().lower()
        for f in self.functions:
            if function in f:
                retval.append(f)
        return retval

    def claim_like(self, func, purpose=None):
        '''
        Works like claim, but with claims all functions that contain the provided string
        For exampls: 'spi1' claims spi1_miso, spi1_mosi, spi1_sck, etc.
        '''
        funcs = self.functions_like(func)
        self.claim(funcs, purpose=purpose)
        return funcs

    @property
    def functions(self):
        return sorted(self.peripherals)

    @property
    def pins(self):
        return sorted(self.data.keys())

    def claim(self, functions, purpose=None):
        '''
        Claim all the functions provided.  Raises an exception if function does not exist or is unclaimable
        '''
        functions = listify(functions)
        for function in functions:
            if self.has(function):
                for pin in self.pins_for(function):
                    if pin not in self.claimed_pins:
                        self.__claimed_functions.add(function)
                        self.__claimed_pins.add(pin)
                        if purpose:
                            self.__purposes[pin] = purpose
                if function not in self.__claimed_functions:
                    raise ValueError("Can't claim function %s: You've already claimed these pins" % function)
            else:
                raise ValueError("Can't claim function %s: Function does not exist." % function)

    def available_like(self, func):
        '''
        Returns all the functions available that contain the string provided
        '''
        return [x for x in self.available_functions if func.lower() in x]

    @property
    def unclaimed_functions(self):
        return [f for f in self.functions if f not in self.__claimed_functions]

    @property
    def claimed_pins(self):
        return sorted(self.__claimed_pins)

    @property
    def available_functions(self):
        retval = []
        claimed_pins = set(self.claimed_pins)
        for function in self.functions:
            pins = set(self.pins_for(function))
            if not pins <= claimed_pins:
                retval.append(function)
        return retval

    @property
    def unavailable_functions(self):
        return sorted(set(self.unclaimed_functions) - set(self.available_functions))

    @property
    def unclaimed_pins(self):
        return sorted([p for p in self.pins if p not in self.__claimed_pins])

    @property
    def claimed_functions(self):
        return sorted(self.__claimed_functions)

    def _table(self):
        d = []
        d.append(['Device:',self.name])
        d.append(['Pins:', len(self.pins)])
        d.append(['Pin','Claimed','Purpose','Functions'])
        
        for pin in self.claimed_pins:
            purpose = self.__purposes.get(pin, None)
            d.append([pin, 'Y', purpose] + list(self.functions_of(pin)))
        for pin in self.unclaimed_pins:
            d.append([pin, 'N', None] + list(self.functions_of(pin)))
        
        return tableview.TableView(d)

    def pretty(self):
        return self._table().pretty()
    
    @staticmethod
    def load(filename, package):
        '''
        Load a pin map from a csv file.
        See the documentation for load() at the module level for more info.
        '''
        def parse_cell(s):
            s = s.lower()
            seps='/ '
            res = [s]
            for sep in seps:
                s, res = res, []
                for seq in s:
                    res += seq.split(sep)
            return [x for x in res if x.strip()]

        table = tableview.load(filename)
        pin_map = {}
        header = table[0]
        func_cols = []
        remap_cols = []
        pin_col = None
        for i, cell in enumerate(header):
            if package.strip().lower() in cell.strip().lower():
                pin_col = i
            if "func" in cell.strip().lower():
                func_cols.append(i)
            if "remap" in cell.strip().lower():
                remap_cols.append(i)
        if pin_col == None:
            raise Exception("Couldn't find the package requested")
        for row in table:
            try:
                pin = int(row[pin_col])
            except:
                continue

            l = [parse_cell(row[i]) for i in func_cols if row[i].strip() != '']
            funcs = []
            for f in l:
                funcs.extend(f)

            l = [parse_cell(row[i]) for i in remap_cols if row[i].strip() != '']
            remap_funcs = []
            for f in l:
                remap_funcs.extend(f)
            pin_map[pin] = (funcs, remap_funcs)
        p = PinMap(pin_map)
        p.name = filename
        p.package = package
        return p
    '''
    def pretty(self):
        retval = ''
        for key in sorted(self.data.keys()):
            functions = self.data[key]
            retval += '%3d : %s\n' % (key, ' | '.join([', '.join(f) for f in functions]))
        return retval
    '''
    def __str__(self):
        return "<PinMap '%s': %d pins %d claimed>" % (self.name,len(self.data), len(self.claimed_pins))
    def __repr__(self):
        return str(self)

def load(filename, package):
    '''
    Loads a pin map file and returns a PinMap object.

    A pinmap file is a csv file that describes the pinout of a microcontroller or other IC:

     * The first row of the file must be a header row that titles each column.
     * A function column contains the text 'func' in the header cell and describes functions for the pins in each row.
     * A remap column contains the text 'remap' in the header cell and describes alternate functions, available through pin re-mapping.
     * A package column is any other column in the file with a nonempty header cell.  A file may describe any number of packages
       for the same microcontroller, and the package returned by the load function must be specified with the `package` argument.
     * For pins with multiple functions, function descriptors can be separated by the slash character '/'

    Below is an example of an 8-pin microcontroller with 2 packages: soic8, and bga9
     * Note that some pins do not have remap functionality (VCC, GND)
     * Note that even without remap, some pins have multiple functions (GP0/AIN1, et al)
     * Note that the bga package has an extra pin (GP3/T1).  The soic package pin for that row is blank, and this is fine.

    soic8,bga9,func,remap
    1,a1,VCC,
    2,a2,OSC,T0
    3,a3,GP0/AIN1,PWM1
    4,b1,GP1/AIN2,PWM2
    5,b2,GP2/AIN3,PWM3
    6,b3,RESET,SDA
    7,c1,GP3/INT,SCL
    8,c2,GND,
     ,c3,GP3,T1
    '''
    return PinMap.load(filename, package)

