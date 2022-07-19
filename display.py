import re
from tkinter import EW, NS, Text, ttk
from tkinter import END, Label, messagebox
from tools.tool import Tools
from tools.db_storage import DBManager
from tools.converter import Converter

def switch_selected_values(c1, c2):
    if c1.get() != '' and c2.get() != '':
        temp = c1.get()
        c1.set(c2.get())
        c2.set(temp)

def store(canvas, manager, db_name, table_name, columns=(), values=()):
    if '' in values or None in values:
        messagebox.showerror('Error', 'Some values are empty')
        return
    manager.connect_to(db_name)
    manager.create_table(table_name, columns)
    placeholder = ','.join(['?' for _ in range(len(values))])
    manager.make_query("INSERT INTO " + table_name + " VALUES (" + placeholder + ")", values)

    rows = manager.make_query(f"SELECT * FROM {table_name}")
    i = 0

    text = Text(canvas, height=10)
    text.grid(row=0, column=0, sticky=EW)
    scrollbar = ttk.Scrollbar(canvas, orient='vertical', command=text.yview)
    scrollbar.grid(row=0, column=1, sticky=NS)
    text['yscrollcommand'] = scrollbar.set
    text.configure(background="black", foreground="white")

    for row in rows:
        tup = map(str, row)
        label = Label(canvas, text='\t'.join(tup), font=('Arial', 9))
        position = f'{i + 1}.0'
        text.insert(position, f'{label.cget("text")}\n')
        i += 1

    position = '0.0'
    text.insert(position, '\t'.join(['value', 'unit', 'result', 'new_unit']) + '\n')

    manager.commit_and_close()

def make_conversion(converter, values):
    converter.save_inputs(values)
    items = {
        'value': values[0],
        'unit': values[1],
        'to': values[2]
    }
    return converter.do_conversion(items)

def validate(regex, text):
        if not re.match(regex, text):
            messagebox.showerror('Error', f'Text "{text}" does not match expected input')
        else:
            print(f"Written text : {text}")

def fill_canvas(tools, canvas, converter, values, manager, storage):

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
        command=lambda : text.set(f"Result is {make_conversion(converter, [float(valueInput.get()), comboboxClassicInput.get(), comboboxClassicOutput.get()])}"), justify='center',
        background='#00349A', foreground='white')

    buttonSwitch = tools.add_button(canvas, text='Switch', command=lambda: switch_selected_values(comboboxClassicInput, comboboxClassicOutput), background='#009000', foreground='white')

    buttonStore = tools.add_button(canvas, text='Store', 
        command=lambda: store(storage, manager, 'databases/conversion.db', 'conversion',
        ('value', 'unit', 'result', 'target_unit'), 
        (valueInput.get(), "'" + comboboxClassicInput.get() + "'", converter.CURRENT, "'" + comboboxClassicOutput.get() + "'")), 
        background='purple', foreground='white')
    
    tools.bind(entryInput, '<<end_input>>', lambda event: validate('[+-]?(\d*[.])?\d+', valueInput.get()))
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
        '6': (result, tools.dimensions[0] - x_offset * 4.5, 130, 215, 30),
        '7': (buttonConvert, 5, 130, 90, 30),
        '8': (buttonSwitch, 100, 130, 55, 30),
        '9': (buttonStore, 5, 165, tools.dimensions[0] - 15, 20)
    }
    tools.place(items)

def main():
    converter = Converter()
    converter.fetch_data()
    manager = DBManager()
    manager.fetch_data('sources/db.json')
    tools = Tools()
    tools.create_window('Converter')
    tools.root.resizable(0, 0)
    
    notebook = tools.add_notebook(tools.root)
    tabClassic = tools.add_frame(notebook)
    tabTemperature = tools.add_frame(notebook)
    tabCurrency = tools.add_frame(notebook)
    tabStorage = tools.add_frame(notebook)

    notebook.add(tabClassic, text='ISU')
    notebook.add(tabTemperature, text='Temperature')
    notebook.add(tabCurrency, text='Currency')
    notebook.add(tabStorage, text='Storage')
    notebook.pack(expand=1, fill="both")

    canvas = tools.create_canvas(tabClassic, (), background='black')
    canvas2 = tools.create_canvas(tabTemperature, (), background='black')
    canvas3 = tools.create_canvas(tabCurrency, (), background='black')
    canvasStorage = tools.create_canvas(tabStorage, (), background='black')
    
    fill_canvas(tools, canvas, converter, converter.get_values_of('ISU'), manager, canvasStorage)
    fill_canvas(tools, canvas2, converter, converter.get_values_of('temperature'), manager, canvasStorage)
    fill_canvas(tools, canvas3, converter, converter.get_values_of('currency'), manager, canvasStorage)

    tools.loop()

if __name__ == '__main__':
    main()