import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, PhotoImage
import csv
import symb
import os
import numpy as np
from dollarpy import Recognizer, Template, Point
import json

class SymbolRecognizer:
    default_width = 400
    default_height = 400
    file_name = None

     # or 'add'

    points = []
    training_set = []
    templateList = []

    def __init__(self, parent, title):
        
        self.create_symbol_dict()
        self.parent = parent
        self.create_gui()
        self.bind_mouse()
        self.title = title
    
    def create_symbol_dict(self):
        with open('./symbol.json') as json_file:
            self.json_decoded = json.load(json_file)

        for key, value in self.json_decoded.items():
            pointList = []
            for point in value:
                pointList.append(Point(*point))
            self.templateList.append(Template(key, pointList))
        
        self.recognizer = Recognizer(self.templateList)
            


    def create_gui(self):
        self.create_top_bar()
        self.create_drawing_canvas()
       
    def create_top_bar(self):
        self.top_bar = tk.Frame(self.parent, height=30, relief='raised', padx=2, pady=2, bg="light gray")
        
        add_symbol_name_lb = tk.Label(self.top_bar, text="add symbol name: ", bg="light gray")
        add_symbol_name_lb.pack(side="left")

        self.add_symbol_name_var = tk.IntVar()
        # self.add_symbol_name_var.set(20)
        self.add_symbol_name_en = tk.Entry(self.top_bar, width="3", text=self.add_symbol_name_var, justify="center")
        self.add_symbol_name_en.pack(side="left", padx=2)


        
        recognized_number_lb = tk.Label(self.top_bar, text="Recognized Number: ", bg="light gray")
        recognized_number_lb.pack(side="left")

        self.recognized_result = tk.StringVar()
        #self.recognized_result.set('10')
        self.recognized_result_en = tk.Entry(self.top_bar, width="3", text=self.recognized_result, justify="center", state='readonly')
        self.recognized_result_en.pack(side="left", padx=2)

        self.add_b = tk.Button(self.top_bar, text="add", command=self.save_symbol, state=tk.DISABLED )
        self.add_b.pack(side="right")

        self.clear_b = tk.Button(self.top_bar, text="clear", command=self.reset_canvas)
        self.clear_b.pack(side="right")

        self.mode = tk.StringVar()
        self.mode.set('recog mode')
        self.mode_b = tk.Button(self.top_bar, textvariable=self.mode, command=self.change_mode)
        self.mode_b.pack(side="right")

        self.top_bar.pack(expand="yes", fill="both")

    def create_drawing_canvas(self):
        self.canvas_frame = tk.Frame(self.parent)
        self.canvas_frame.pack(expand="yes", fill="both")
        self.canvas = tk.Canvas(self.canvas_frame, width=self.default_width, height=self.default_height)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
 
    def bind_mouse(self):
        self.canvas.bind("<Button-1>", self.on_mouse_button_pressed)
        self.canvas.bind("<Button1-Motion>", self.on_mouse_button_pressed_motion)
        self.canvas.bind("<Button1-ButtonRelease>", self.on_mouse_button_released)
    
    def save_symbol(self):

        print('save')
    
    def change_mode(self):
        if  self.mode.get() == 'recog mode':
            self.mode.set('add mode')
            self.add_b['state'] = 'normal'
        else:
            self.mode.set('recog mode')
            self.add_b['state'] = 'disable'


    def on_mouse_button_pressed(self, event):
        if (self.mode.get() == "add mode"):
            self.points.append([event.x, event.y, 0])
        else:
            self.points.append(Point(event.x, event.y, 0))

    def on_mouse_button_pressed_motion(self, event):
        if (self.mode.get() == "add mode"):
            self.points.append([event.x, event.y, 0])
        else:
            self.points.append(Point(event.x, event.y, 0))
        color = 'red'
        x1, y1 = (event.x-1), (event.y-1)
        x2, y2 = (event.x+1), (event.y+1)
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
    

    def on_mouse_button_released(self, event):
        print('release')
        
        if len(self.points) > 0 and self.mode.get():  # prevent canvas frame from grabbing filedialog mouse button events
           
            if self.mode.get() == "add mode":
                self.add_symbol(self.points)
            elif self.mode.get() == "recog mode":
                self.recognized_result.set(self.recognizer.recognize(self.points)[0])

    def reset_canvas(self):
        self.canvas.delete("all")
        self.points = []
        
        
    def add_symbol(self, points):

        with open('./symbol.json') as json_file:
            self.json_decoded = json.load(json_file)

        self.json_decoded[self.add_symbol_name_var.get()] = points

        with open('./symbol.json', 'w') as json_file:
            json.dump(self.json_decoded, json_file)



if __name__ == '__main__':
    root = tk.Tk()
    title = "Unistroke symbol recognition"
    root.title(title)
    app = SymbolRecognizer(root, title)
    root.mainloop()