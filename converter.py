class Converter:

    units = {
        'meter': ['mm', 'cm', 'dm', 'm', 'dam', 'hm', 'km'],
        'liter': ['ml', 'cl', 'dl', 'l', 'dal', 'hl', 'kl'],
        'gram': ['mg', 'cg', 'dg', 'g', 'dag', 'hg', 'kg']
    }

    conversion = {
        'gram-liter' : lambda x: x / 1000,
        'liter-gram' : lambda x: x * 1000,
        'gram-meter' : lambda x: x / 1000,
        'meter-gram' : lambda x: x * 1000,
    }

    def get_unit(self, measure = str):
        keys = self.units.keys()
        for key in keys:
            if measure in self.units[key]:
                return key
        return None

    def get_conversion(self, measures = str):
        keys = self.conversion.keys()
        for key in keys:
            if measures == key:
                return self.conversion[key]
        return None

    def __make(self, arg = {}):
        unit_key = self.get_unit(arg['unit'])
        to_key = self.get_unit(arg['to'])
        unit_index = self.units[unit_key].index(arg['unit'])
        to_index = self.units[to_key].index(arg['to'])
        scale = self.get_conversion('-'.join([unit_key, to_key]))
        print(f"Converting {unit_key} into {to_key}...")
        print(f"Input : {arg['value']}{arg['unit']}")
        return (unit_index, to_index, scale)

    def convert(self, arg = {}):
        text = ''
        tools = self.__make(arg)
        if(tools[2] is not None):
            func = tools[2]
            if tools[0] < tools[1] :
                text = f"Result : {func(arg['value'] / 10 ** (tools[1]  - tools[0]))}{arg['to']}"
            elif tools[0]  > tools[1] :
                text = f"Result : {func(arg['value'] * 10 ** (tools[0]  - tools[1]))}{arg['to']}"
            else:
                text = f"Result : {func(arg['value'])}{arg['to']}"
        else:
            if tools[0] < tools[1] :
                text = f"Result : {arg['value'] / 10 ** (tools[1]  - tools[0] )}{arg['to']}"
            elif tools[0]  > tools[1] :
                text = f"Result : {arg['value'] * 10 ** (tools[0]  - tools[1] )}{arg['to']}"
            else:
                text = f"Result : {arg['value']}{arg['to']}"
        return text


converter = Converter()
print(converter.convert({'value': 1, 'unit': 'kg', 'to': 'l'}))
