import re
from tkinter.ttk import Combobox
from converters.classic_converter import ClassicConverter
from converters.temperature_converter import TemperatureConverter
from tkinter import END, Button, Canvas, Label, Tk, StringVar, Entry, messagebox

class Tools:

    def __init__(self) -> None:
        self.root = None
        self.dimensions = ()
        self.save = {}
        self.result = ''

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

    def add_label(self, master, text, **args):
        label = Label(master, text=text, **args)
        label.pack()
        return label

    def place(self, arg={}):
        for key in arg.keys():
            value = arg[key]
            value[0].place(x=value[1], y=value[2], width=value[3], height=value[4])

    def bind(self, item, type, callback):
        item.bind(type, callback)

    def change_state(self, item, state):
        item['state'] = state

    def loop(self):
        self.root.mainloop()

    def validate(self, event, regex, text):
        if not re.match(regex, text):
            messagebox.showerror('Error', f'Text "{text}" does not match expected input')
        else:
            print(f"Written text : {text}")

    def saveInputs(self, *values):
        self.save = {
            'value': values[0],
            'unit': values[1],
            'to': values[2]
        }

    def saveResult(self, converter, values):
        self.result = converter.convert(values)
        print(f'{self.result}')

def main():
    converter = ClassicConverter()
    tools = Tools()
    tools.create_window('Converter')
    canvas = tools.create_canvas(tools.root, (), background='gray')

    valueInput = tools.add_stringvar()
    entryInput = tools.add_entry(canvas, valueInput)
    entryInput.insert(0, 'put value here')
    entryInput.event_add('<<end_input>>', '<FocusOut>')

    units = list(converter.units.values())
    unit = []
    for sub in units:
        for elt in sub:
            unit.append(elt)

    comboboxClassicInput = tools.add_combobox(canvas, unit)
    comboboxClassicOutput = tools.add_combobox(canvas, unit)
    buttonSave = tools.add_button(canvas, '✔️', lambda: tools.saveInputs(float(valueInput.get()), comboboxClassicInput.get(), comboboxClassicOutput.get()))
    buttonConvert = tools.add_button(canvas, 'Convert', lambda : tools.saveResult(converter, tools.save))
    
    tools.bind(entryInput, '<<end_input>>', lambda event: tools.validate(event, '^[+-]?(\d*[.])?\d+$', valueInput.get()))
    tools.bind(entryInput, '<FocusIn>', lambda event: entryInput.delete(0, END))
    tools.bind(comboboxClassicInput, "<<ComboboxSelected>>", lambda event: print(f"\"{comboboxClassicInput.get()}\" selected !"))
    tools.bind(comboboxClassicOutput, "<<ComboboxSelected>>", lambda event: print(f"\"{comboboxClassicOutput.get()}\" selected !"))

    items = {
        '0': (entryInput, 10, 10, 90, 30),
        '1': (comboboxClassicInput, 110, 10, 60, 30),
        '2': (comboboxClassicOutput, 180, 10, 60, 30),
        '3': (buttonSave, 10, 50, 40, 30),
        '4': (buttonConvert, 60, 50, 90, 30)
    }
    tools.place(items)

    tools.loop()

if __name__ == '__main__':
    main()