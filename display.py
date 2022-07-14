import re
from tkinter.ttk import Combobox
from converters.classic_converter import ClassicConverter
from converters.temperature_converter import TemperatureConverter
from tkinter import Button, Canvas, Tk, StringVar, Entry, messagebox

class Tools:

    def __init__(self) -> None:
        self.root = None
        self.dimensions = ()

    def create_window(self, title, dimensions = ()):
        self.root = Tk()
        self.root.title(title)
        if len(dimensions) == 2:
            width = dimensions[0]
            height = dimensions[1]
        else:
            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()
        self.dimensions = (width, height)
        self.root.geometry('x'.join((str(width), str(height))))
    
    def create_canvas(self, master, dimensions = (), **args):
        canvas = None
        if len(dimensions) == 2:
            canvas = Canvas(master, width=dimensions[0], height=dimensions[1], **args)
        else:
            canvas = Canvas(master, width=self.dimensions[0], height=self.dimensions[1], **args)
        canvas.pack()
        return canvas

    def add_stringvar(self):
        return StringVar()

    def add_entry(self, master, string_var, **args):
        entry = Entry(master, textvariable=string_var, **args)
        entry.pack()
        return entry

    def add_button(self, master, text, command, **args):
        button = Button(master, text=text, command=command, **args)
        button.pack()
        return button

    def add_combobox(self, master, values = [], **args):
        combobox = Combobox(master, values=values, **args)
        combobox.pack()
        return combobox

    def place_items(self, items, x_serie, y_serie, w_serie, h_serie):
        for item, x, y, w, h in zip(items, x_serie, y_serie, w_serie, h_serie):
            item.place(x=x, y=y, width=w, height=h)

    def bind(self, item, type, callback):
        item.bind(type, callback)

    def change_state(self, item, state):
        item['state'] = state

    def loop(self):
        self.root.mainloop()

def validate(event, text):
    if not re.match('^[+-]?(\d*[.])?\d+$', text):
        messagebox.showerror('Error', f'Text "{text}" does not match expected input')
    else:
        print(f"Written text : {text}")

def useValues(value, unit, to):
    return {
        'value': value,
        'unit': unit,
        'to': to
    }

def main():
    converter = ClassicConverter()
    tools = Tools()
    tools.create_window('Converter')
    canvas = tools.create_canvas(tools.root, (), background='gray')

    valueInput = tools.add_stringvar()
    entryInput = tools.add_entry(canvas, valueInput)
    entryInput.event_add('<<end_input>>', '<FocusOut>')

    units = list(converter.units.values())
    unit = []
    for sub in units:
        for elt in sub:
            unit.append(elt)

    comboboxClassicInput = tools.add_combobox(canvas, unit)
    comboboxClassicOutput = tools.add_combobox(canvas, unit)
    conversion = lambda : print(converter.convert(useValues(float(valueInput.get()), comboboxClassicInput.get(), comboboxClassicOutput.get())))
    buttonConvert = tools.add_button(canvas, 'Convert', conversion)
    

    tools.bind(entryInput, '<<end_input>>', lambda event: validate(event, valueInput.get()))
    tools.bind(comboboxClassicInput, "<<ComboboxSelected>>", lambda event: print(f"\"{comboboxClassicInput.get()}\" selected !"))
    tools.bind(comboboxClassicOutput, "<<ComboboxSelected>>", lambda event: print(f"\"{comboboxClassicOutput.get()}\" selected !"))
    tools.loop()

if __name__ == '__main__':
    main()