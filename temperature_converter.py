class TemperatureConverter:

    temp = {
        'fahrenheit': '°F',
        'celsius': '°C',
        'kelvin': 'K'
    }

    conversion = {
        'celsius-fahrenheit': lambda x: (x * (9/5)) + 32, #
        'fahrenheit-celsius': lambda x: (x - 32) * (5/9), #
        'celsius-kelvin': lambda x: x + 273.15, #
        'kelvin-celsius': lambda x: x - 273.15, #
        'fahrenheit-kelvin': lambda x: (x + 459.67) * (5/9), #
        'kelvin-fahrenheit': lambda x: x * 9/5 - 459.67
    }

    def get_temp(self, measure=str):
        keys = self.temp.keys()
        for key in keys:
            if measure in self.temp[key]:
                return key
        return None

    def get_conversion(self, measures=str):
        keys = self.conversion.keys()
        for key in keys:
            if measures == key:
                return self.conversion[key]
        return None

    def __make(self, arg={}):
        unit_key = self.get_temp(arg['unit'])
        to_key = self.get_temp(arg['to'])
        if unit_key is None or to_key is None:
            raise TypeError('incorrect temperature unit')
        conversion = self.get_conversion('-'.join([unit_key, to_key]))
        print(f"Converting {unit_key} into {to_key}...")
        print(f"Input : {arg['value']}{arg['unit']}")
        return (arg['value'], arg['to'], conversion)

    def convert(self, arg={}):
        text = ''
        if arg['value'] in ['', None] or arg['unit'] in ['', None] or arg['to'] in ['', None]:
            return text
        tools = self.__make(arg)
        conversion = tools[2]
        text = f"Result : {conversion(tools[0])} {tools[1]}"
        return text
        
converter = TemperatureConverter()
print(converter.convert({'value': 27, 'unit': 'K', 'to': '°F'}))