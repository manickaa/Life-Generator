from tkinter import *
from tkinter.ttk import *

class Input_Widgets():

    def __init__(self, main_categories, canvas):
        
        self.canvas = canvas
        self.create_widgets(main_categories)

    def place_in_grid(self, widget, custom_row, custom_column):
        
        widget.grid(row=custom_row, column=custom_column)
    
    def create_label(self, custom_text, custom_row, custom_column):

        label = Label(self.canvas, text=custom_text)
        self.place_in_grid(label, custom_row, custom_column)

    def intro_widget(self):
        
        introText = "Confused about what to buy? We have a bunch of categories to help \
with your search. \n Choose from the options to start your search. \n Also don't forget \
to enter the number of results you want ;)"

        self.create_label(introText, 1, 0)

    def category_widget(self, main_categories):
        
        placeholder_text = "Choose a toy category:"
        self.create_label(placeholder_text, 3, 0)

        self.category_items = Combobox(self.canvas)
        self.place_in_grid(self.category_items, 3, 1)
        self.category_items["values"] = tuple(option for option in main_categories) 
    
    def number_widget(self):

        placeholder_text = "Enter/Choose the number of results to generate:"
        self.create_label(placeholder_text, 5, 0)

        self.num_item = Spinbox(self.canvas, from_=1, to=10000)
        self.place_in_grid(self.num_item, 5, 1)

    def button_widget(self):

        self.result_button = Button(self.canvas, text="Get Output")
        self.place_in_grid(self.result_button, 7, 1)

    def create_widgets(self, main_categories):

        self.intro_widget()
        
        self.category_widget(main_categories)

        self.number_widget()

        self.button_widget()

        self.canvas.grid_rowconfigure((0,2,4,6,8), minsize=50 )
        
        self.canvas.pack()