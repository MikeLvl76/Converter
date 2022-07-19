from tkinter import Button, Canvas, Label, Tk, StringVar, Entry, messagebox
from tkinter import ttk

'''
Class for GUI with Tkinter. All Tkinter packages are not used because it's unnecessary.
It enables creating application with canvas, button, label, entry & stringvar, combobox, frame and notebook.
Items can be binded, have their status changed and placed.
'''
class Tools:

    '''
    Initialize class with global variables
    '''
    def __init__(self) -> None:
        self.root = None
        self.dimensions = ()
        self.save = {}
        self.result = ''

    '''
    Create window with customized title and dimensions.
    If empty tuple is given for dimensions, then default size is set.
    '''
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
    
    '''
    Create Canvas object by linking it to Tk objet (master).
    Dimensions are treated like before.
    Many arguments can be added, read documentation for more details.
    '''
    def create_canvas(self, master, dimensions = (), **args):
        canvas = None
        if len(dimensions) == 2:
            canvas = Canvas(master, width=dimensions[0], height=dimensions[1], **args)
        else:
            canvas = Canvas(master, width=self.dimensions[0], height=self.dimensions[1], **args)
        canvas.pack()
        return canvas

    '''
    Create StringVar object and return it.
    '''
    def add_stringvar(self):
        return StringVar()

    '''
    Create Entry object and link it to parent (Canvas or Tk).
    Add StringVar object as textvariable to handle user input.
    Like Canvas, there are many arguments.'''
    def add_entry(self, master, string_var, **args):
        entry = Entry(master, textvariable=string_var, **args)
        entry.pack()
        return entry

    '''
    Create Button object and link it to parent (Canvas or Tk).
    Like other widgets, there are many arguments for it.
    '''
    def add_button(self, master, **args):
        button = Button(master, **args)
        button.pack()
        return button

    '''
    Create Combobox object and link it to parent (Canvas or Tk).
    A list of value is required if user wants to select one after.
    Like other widgets, there are many for it.
    '''
    def add_combobox(self, master, values = [], **args):
        combobox = ttk.Combobox(master, values=values, **args)
        combobox.pack()
        return combobox

    '''
    Create Label object and link it to parent (Canvas or Tk).
    Like other widgets, there are many arguments for it.
    '''
    def add_label(self, master, **args):
        label = Label(master, **args)
        label.pack()
        return label

    '''
    Create Frame object and link it to parent (Canvas or Tk).
    Like other widgets, there are many arguments for it.
    '''
    def add_frame(self, master, **options):
        return ttk.Frame(master, **options)

    '''
    Create Notebook object and link it to parent (Canvas or Tk).
    Like other widgets, there are many arguments for it.
    '''
    def add_notebook(self, master, **options):
        return ttk.Notebook(master, **options)

    '''
    Place items by giving dict.
    The dict must contains key and tuple, with widget as first item and x position, y position, width and height then.
    '''
    def place(self, arg={}):
        for key in arg.keys():
            value = arg[key]
            value[0].place(x=value[1], y=value[2], width=value[3], height=value[4])

    '''
    Bind an item with type as argument, for example a type can be "<FocusIn>" or something else like "<<event_type>>" or "<event_type>".
    A callback function is required, lambda or not.
    '''
    def bind(self, item, type, callback):
        item.bind(type, callback)

    '''
    Change widget state, the state arg must be a str.
    Useful to disable button or set combobox in read-only mode for example.
    '''
    def change_state(self, item, state):
        item['state'] = state

    '''
    Launch app.
    '''
    def loop(self):
        self.root.mainloop()