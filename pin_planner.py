import tables

class PinMap(object):
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
        self.__function_map = {}

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

    def claim_like(self, func):
        '''
        Works like claim, but with claims all functions that contain the provided string
        For exampls: 'spi1' claims spi1_miso, spi1_mosi, spi1_sck, etc.
        '''
        funcs = self.functions_like(func)
        self.claim(*funcs)
        return funcs

    @property
    def functions(self):
        return sorted(self.peripherals)

    @property
    def pins(self):
        return sorted(self.data.keys())

    def claim(self, *functions):
        for function in functions:
            if self.has(function):
                for pin in self.pins_for(function):
                    if pin not in self.claimed_pins:
                        self.__claimed_functions.add(function)
                        self.__claimed_pins.add(pin)
                if function not in self.__claimed_functions:
                    raise ValueError("Can't claim function %s: You've already claimed these pins" % function)
            else:
                raise ValueError("Can't claim function %s: Function does not exist." % function)

    def available_like(self, func):
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

    @staticmethod
    def load(filename, package):
        def parse_cell(s):
            s = s.lower()
            seps='/ '
            res = [s]
            for sep in seps:
                s, res = res, []
                for seq in s:
                    res += seq.split(sep)
            return [x for x in res if x.strip()]

        table = tables.load(filename)
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
        return p

    def __str__(self):
        return "<PinMap '%s': %d pins %d claimed>" % (self.name,len(self.data), len(self.claimed_pins))
    def __repr__(self):
        return str(self)

def load(filename, package):
    return PinMap.load(filename, package)

