from converters.classic_converter import ClassicConverter
from converters.temperature_converter import TemperatureConverter
from tkinter import Canvas, Tk

root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.title('Converter')
root.geometry('x'.join([str(width), str(height)]))

canvas = Canvas(root, width=width, height=height, background='gray')
canvas.pack()

root.mainloop()