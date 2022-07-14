from tkinter.ttk import Combobox
from converters.classic_converter import ClassicConverter
from converters.temperature_converter import TemperatureConverter
from tkinter import Canvas, Tk, StringVar, Entry

root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.title('Converter')
root.geometry('x'.join([str(width), str(height)]))

canvas = Canvas(root, width=width, height=height, background='gray')
canvas.pack()

value = StringVar()
entry = Entry(canvas, textvariable=value)
entry.pack()

units = list(ClassicConverter.units.values())
unit = []
for sub in units:
    for elt in sub:
        unit.append(elt)

comboboxClassic = Combobox(canvas, values=unit)
comboboxClassic.pack()

entry.event_add('<<end_input>>', '<Return>')
entry.bind('<<end_input>>', lambda event : print(f"Written text !"))
comboboxClassic.bind("<<ComboboxSelected>>", lambda event : print(f"An element is selected !"))

root.mainloop()