import re
from tkinter import Button, Canvas, Label, Tk, StringVar, Entry, messagebox
from tkinter import ttk

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
        combobox = ttk.Combobox(master, values=values, **args)
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
        self.result = converter.do_conversion(values)
        print(f'{self.result}')