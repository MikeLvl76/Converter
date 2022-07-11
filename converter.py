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
        'liter-meter' : lambda x: 1 / (x ** 3),
        'meter-liter' : lambda x: (x ** 3) * 1000
    }

    def get_unit(self, measure):
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
        if unit_key == to_key:
            print(f"Result : {arg['value']}{arg['to']}")
            return None
        return (unit_index, to_index, scale)

    def convert(self, arg = {}):
        print(f"Converting {arg['value']}{arg['unit']} into {arg['to']}...")
        text = ''
        tools = self.__make(arg)
        if tools is None:
            return tools
        if(tools[2] is not None):
            func = tools[2]
            if tools[0] < tools[1] :
                text = f"Result : {func(arg['value'] / 10 ** (tools[1]  - tools[0] ))}{arg['to']}"
            elif tools[0]  > tools[1] :
                text = f"Result : {func(arg['value'] * 10 ** (tools[0]  - tools[1] ))}{arg['to']}"
        else:
            if tools[0] < tools[1] :
                text = f"Result : {arg['value'] / 10 ** (tools[1]  - tools[0] )}{arg['to']}"
            elif tools[0]  > tools[1] :
                text = f"Result : {arg['value'] * 10 ** (tools[0]  - tools[1] )}{arg['to']}"
        return text


converter = Converter()
print(converter.convert({'value': 2, 'unit': 'l', 'to': 'm'}))
print(converter.get_unit('ml'))
