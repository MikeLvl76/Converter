class Converter:

    units = {
        'meter': ['mm', 'cm', 'dm', 'm', 'dam', 'hm', 'km'],
        'liter': ['ml', 'cl', 'dl', 'l', 'dal', 'hl', 'kl'],
        'gram': ['mg', 'cg', 'dg', 'g', 'dag', 'hg', 'kg']
    }

    def convert(self, arg = {}):
        print(f"Converting {arg['value']}{arg['unit']} into {arg['to']}...")
        if arg['unit'] in self.units['meter']:
            if arg['to'] in self.units['meter']:
                unit_index = self.units['meter'].index(arg['unit'])
                to_index = self.units['meter'].index(arg['to'])
                if unit_index < to_index :
                    print(f"Result : {arg['value'] / 10 ** (to_index - unit_index)}{arg['to']}")
                elif unit_index > to_index:
                    print(f"Result : {arg['value'] * 10 ** (unit_index - to_index)}{arg['to']}")
                else:
                    print(f"Result : {arg['value']}{arg['to']}")

converter = Converter()
converter.convert({'value': 1.2, 'unit': 'm', 'to': 'dam'})