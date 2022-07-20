import json
from tkinter import CURRENT

'''
Class to convert unit to another.
Currently there are 3 types of units : ISU, currency and temperature.
A JSON file is used as supply and contains what it's needed.
'''
class Converter:

    '''
    Save current result from conversion
    '''
    CURRENT = 0

    '''
    Save user inputs
    '''
    INPUTS = []

    '''
    Initialize by creating variable for json reading
    '''
    def __init__(self) -> None:
        self.__decoder = None

    '''
    Open and read json with utf-8 encoding (needed for special characters)
    '''
    def fetch_data(self):
        self.__decoder = json.load(open('sources/data.json', encoding='utf-8'))

    '''
    Get an item by its value and return it
    If not found, then None is returned
    '''
    def get_item(self, value):
        keys = self.__decoder.keys()
        for key in keys:
            sub_keys = self.__decoder[key]
            for k in sub_keys:
                if value in sub_keys[k]:
                    return k
        return None

    '''
    Get a value by an item and return it
    If not found, then None is returned
    '''
    def get_value(self, item):
        keys = self.__decoder.keys()
        for key in keys:
            sub_keys = self.__decoder[key]
            for k in sub_keys:
                if item == k:
                    return sub_keys[k]
        return None

    '''
    Get all child keys values from parent key and returned them as dict_series
    If not found, then empty array is returned'''
    def get_values_of(self, key):
        if key not in self.__decoder.keys():
            return []
        return self.__decoder[key].values()

    '''
    Get function in conversion key by giving a child key
    If found then it's evaluated in order to being usable
    If not found, then None is returned
    '''
    def get_func_from(self, key):
        ks = self.__decoder['conversion'].keys()
        for k in ks:
            if key == k:
                return eval(self.__decoder['conversion'][k])
        return None

    def save_inputs(self, inputs):
        for ipt in inputs:
            self.INPUTS.append(ipt)

    '''
    Do a conversion by giving dict
    The dict must have 3 keys : value, unit and to
    An error will be raised if keys are not found
    For value with different order of magnitude, the calculation is based on index position of both units
    If same order of magnitude, the calculation will result to 1
    Next to, a function is found in json to convert
    Finally, result is saved in messages array and is returned
    '''
    def do_conversion(self, arg={}):
        if arg['value'] in ['', None] or arg['unit'] in ['', None] or arg['to'] in ['', None]:
            return TypeError('None or empty value not allowed')

        key1 = self.get_item(arg['unit'])
        key2 = self.get_item(arg['to'])

        if (key1, key2) == (None or '', None or ''):
            raise TypeError('key error')

        index1 = self.get_value(key1).index(arg['unit'])
        index2 = self.get_value(key2).index(arg['to'])
        conversion = self.get_func_from('-'.join([key1, key2]))

        print(f"Converting {key1} into {key2}...")
        print(f"Entered value is ({arg['value']}{arg['unit']})")

        text = 'None'
        result = 0
        if(conversion is not None):
            if index1 < index2:
                calculation = conversion(arg['value'] / 10 ** (index2  - index1))
                result = round(calculation, 3)
                text = f"{result}{arg['to']}"
            elif index1 > index2:
                calculation = conversion(arg['value'] * 10 ** (index1  - index2))
                result = round(calculation, 3)
                text = f"{result}{arg['to']}"
            else:
                result = round(conversion(arg['value']), 3)
                text = f"{result}{arg['to']}"
        else:
            if index1 < index2:
                calculation = arg['value'] / 10 ** (index2  - index1 )
                result = round(calculation, 3)
                text = f"{result}{arg['to']}"
            elif index1 > index2:
                calculation = arg['value'] * 10 ** (index1  - index2 )
                result = round(calculation, 3)
                text = f"{result}{arg['to']}"
            else:
                result = round(conversion(arg['value']), 3)
                text = f"{result}{arg['to']}"

        self.CURRENT = result
        print(f'Result is ({result}{arg["to"]})')
        return text

    def __str__(self) -> str:
        ipts = f"Inputs: [{', '.join([str(ipt) for ipt in self.INPUTS])}]\n"
        cur = f"Current result: {self.CURRENT}"
        if self.__decoder is None:
            no_data = 'No read data\n'
            return no_data + ipts + cur
        return json.dumps(self.__decoder, indent=4) + '\n' + ipts + cur
        

def main():
    converter = Converter()
    converter.fetch_data()
    print(converter.do_conversion({'value': 27, 'unit': 'K', 'to': '°F'}))
    print(converter.do_conversion({'value': 27, 'unit': '£', 'to': '€'}))
    print(converter.do_conversion({'value': 1, 'unit': 'mm', 'to': 'cg'}))
    print(converter)
    

if __name__ == '__main__':
    main()