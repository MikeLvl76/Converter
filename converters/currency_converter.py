class CurrencyConverter:

    '''
    Dict for currency, each key contains a string representation of currency unit
    Currently, there are three units : euro, dollar, pound
    '''

    currency = {
        'euro': '€',
        'dollar': '$',
        'pound': '£'
    }

    '''
    Dict for conversion between two currencies.
    Lambda function is better for easy and fast use.
    '''

    conversion = {
        'dollar-euro': lambda x: x * 0.992000,
        'euro-dollar': lambda x: x * 1.008065,
        'dollar-pound': lambda x: x * 0.843526,
        'pound-dollar': lambda x: x * 1.185500,
        'euro-pound': lambda x: x * 0.850329,
        'pound-euro': lambda x: x * 1.176016
    }

    '''
    By one measure we get associated currency.
    If not, None is returned.
    '''

    def get_currency(self, measure=str):
        keys = self.currency.keys()
        for key in keys:
            if measure in self.currency[key]:
                return key
        return None

    '''
    The same goes for it but with conversion.
    If not, None is returned
    '''

    def get_conversion(self, measures=str):
        keys = self.conversion.keys()
        for key in keys:
            if measures == key:
                return self.conversion[key]
        return None

    '''
    Get keys from unit inputs and make conversion.
    All is returned as tuple.
    '''

    def __make(self, arg={}):
        unit_key = self.get_currency(arg['unit'])
        to_key = self.get_currency(arg['to'])
        if unit_key is None or to_key is None:
            raise TypeError('incorrect temperature unit')
        conversion = self.get_conversion('-'.join([unit_key, to_key]))
        print(f"Converting {unit_key} into {to_key}...")
        print(f"{arg['value']}{arg['unit']}")
        return (arg['value'], arg['to'], conversion)

    '''
    Make the conversion happen.
    An empty text is returned if nothing happen.
    '''

    def convert(self, arg={}):
        text = ''
        if arg['value'] in ['', None] or arg['unit'] in ['', None] or arg['to'] in ['', None]:
            return text
        tools = self.__make(arg)
        conversion = tools[2]
        text = f"{round(conversion(tools[0]), 4)}{tools[1]}"
        return text
        
def main():
    converter = CurrencyConverter()
    print(converter.convert({'value': 27, 'unit': '£', 'to': '€'}))

if __name__ == '__main__':
    main()