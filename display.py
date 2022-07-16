import re
from tkinter import ttk
from tkinter.ttk import Combobox
from converters.classic_converter import ClassicConverter
from converters.temperature_converter import TemperatureConverter
from converters.currency_converter import CurrencyConverter
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
            width = int(self.root.winfo_screenwidth() / 4)
            height = int(self.root.winfo_screenheight() / 4)
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

    def add_button(self, master, **args):
        button = Button(master, **args)
        button.pack()
        return button

    def add_combobox(self, master, values = [], **args):
        combobox = Combobox(master, values=values, **args)
        combobox.pack()
        return combobox

    def add_label(self, master, **args):
        label = Label(master, **args)
        label.pack()
        return label

    def add_frame(self, master, **options):
        return ttk.Frame(master, **options)

    def add_notebook(self, master, **options):
        return ttk.Notebook(master, **options)

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

    def validate(self, regex, text):
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

    def save_result(self, converter, values):
        self.result = converter.convert(values)
        print(f'{self.result}')

def switch_selected_values(c1, c2):
    if c1.get() != '' and c2.get() != '':
        temp = c1.get()
        c1.set(c2.get())
        c2.set(temp)

def fill_canvas(tools, canvas, converter, values):
    valueInput = tools.add_stringvar()
    entryInput = tools.add_entry(canvas, valueInput)
    entryInput.insert(0, 'put value here')
    entryInput.event_add('<<end_input>>', '<Leave>')

    units = list(values)
    unit = []
    for sub in units:
        if isinstance(sub, (list, tuple)):
            for elt in sub:
                unit.append(elt)
        else:
            unit.append(sub)

    comboboxClassicInput = tools.add_combobox(canvas, unit)
    comboboxClassicOutput = tools.add_combobox(canvas, unit)
    tools.change_state(comboboxClassicInput, 'readonly')
    tools.change_state(comboboxClassicOutput, 'readonly')
    buttonConvert = tools.add_button(canvas, text='Convert',
        command=lambda : (tools.saveInputs(float(valueInput.get()), comboboxClassicInput.get(), comboboxClassicOutput.get()), 
        tools.save_result(converter, tools.save), text.set(f"Result : {tools.result}")), justify='center',
        background='#00349A', foreground='white')
    buttonSwitch = tools.add_button(canvas, text='Switch', command=lambda: switch_selected_values(comboboxClassicInput, comboboxClassicOutput), background='#009000', foreground='white')
    
    tools.bind(entryInput, '<<end_input>>', lambda event: tools.validate('^[+-]?(\d*[.])?\d+$', valueInput.get()))
    tools.bind(entryInput, '<FocusIn>', lambda event: entryInput.delete(0, END))
    tools.bind(comboboxClassicInput, "<<ComboboxSelected>>", lambda event: print(f"\"{comboboxClassicInput.get()}\" selected !"))
    tools.bind(comboboxClassicOutput, "<<ComboboxSelected>>", lambda event: print(f"\"{comboboxClassicOutput.get()}\" selected !"))

    label1 = tools.add_label(canvas, text='value'.upper(), background='black', foreground='white', justify='left', font=('Arial', 9))
    label2 = tools.add_label(canvas, text='unit'.upper(), background='black', foreground='white', justify='left', font=('Arial', 9))
    label3 = tools.add_label(canvas, text='to'.upper(), background='black', foreground='white', justify='left', font=('Arial', 9))
    text = tools.add_stringvar()
    text.set('Awaiting result')
    result = tools.add_label(canvas, textvariable=text, background='black', foreground='white', justify='center', font=('Arial', 9), relief="solid", highlightcolor="white", highlightthickness=2)

    x_offset = 50

    items = {
        '0': (label1, 5, 10, 50, 30),
        '1': (entryInput, tools.dimensions[0] - x_offset * 2, 10, 90, 30),
        '2': (label2, 5, 50, 50, 30),
        '3': (comboboxClassicInput, tools.dimensions[0] - x_offset * 2, 50, 55, 30),
        '4': (label3, 5, 90, 50, 30),
        '5': (comboboxClassicOutput, tools.dimensions[0] - x_offset * 2, 90, 55, 30),
        '6': (result, tools.dimensions[0] - x_offset * 4.5, 130, 200, 30),
        '7': (buttonConvert, 5, 130, 90, 30),
        '8': (buttonSwitch, 100, 130, 55, 30)
    }
    tools.place(items)

def main():
    classic = ClassicConverter()
    temperature = TemperatureConverter()
    currency = CurrencyConverter()
    tools = Tools()
    tools.create_window('Converter')
    tools.root.resizable(0, 0)
    
    notebook = tools.add_notebook(tools.root)
    tabClassic = tools.add_frame(notebook)
    tabTemperature = tools.add_frame(notebook)
    tabCurrency = tools.add_frame(notebook)

    notebook.add(tabClassic, text='Classic')
    notebook.add(tabTemperature, text='Temperature')
    notebook.add(tabCurrency, text='Currency')
    notebook.pack(expand=1, fill="both")

    canvas = tools.create_canvas(tabClassic, (), background='black')
    canvas2 = tools.create_canvas(tabTemperature, (), background='black')
    canvas3 = tools.create_canvas(tabCurrency, (), background='black')
    fill_canvas(tools, canvas, classic, classic.units.values())
    fill_canvas(tools, canvas2, temperature, temperature.temp.values())
    fill_canvas(tools, canvas3, currency, currency.currency.values())

    tools.loop()

if __name__ == '__main__':
    main()