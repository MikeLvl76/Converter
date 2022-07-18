import json
from lib2to3.pytree import convert

class Converter:

    def __init__(self) -> None:
        self.__decoder = None

    def fetch_data(self):
        self.__decoder = json.load(open('converters/data.json'))

    def get_item(self, name):
        if self.__decoder[name] is None:
            return None
        return self.__decoder[name]

    def get_key_from(self, item, value):
        keys = item.keys()
        for key in keys:
            if value in item[key]:
                return key
        return None

    def get_func_from(self, item, key):
        ks = item.keys()
        for k in ks:
            if key == k:
                return item[k]
        return None

def main():
    converter = Converter()
    converter.fetch_data()
    item = converter.get_item('conversion')
    print(item)
    key = converter.get_key_from(converter.get_item('temperature'), "F")
    print(key)
    func = eval(converter.get_func_from(item, "gram-liter"))
    print(func(1))

if __name__ == '__main__':
    main()