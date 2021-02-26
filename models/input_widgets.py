from tkinter import *
from tkinter.ttk import *

class Input_Widgets():

    def __init__(self, main_categories, canvas):
        
        self.canvas = canvas
        self.create_widgets(main_categories)


    def intro_widget(self):
        
        introText = "Confused about what to buy? We have a bunch of categories to help with your search. \n\
Choose from the options to start your search. \n Also don't forget to enter the number of results you want ;)"

        label = Label(self.canvas, text= introText)
        label.grid(row=1,column=0)

    def category_widget(self, main_categories):
        
        categoryLabel = Label(self.canvas, text="Choose a toy category:")
        categoryLabel.grid(row=3, column=0)

        self.category_items = Combobox(self.canvas)
        self.category_items.grid(row=3, column=1)
        self.category_items["values"] = tuple(option for option in main_categories) 
    
    def number_widget(self):

        number_label = Label(self.canvas, text="Enter/Choose the number of results to generate:")
        number_label.grid(row=5, column=0)

        self.num_item = Spinbox(self.canvas, from_=1, to=10000)
        self.num_item.grid(row=5, column=1)

    def button_widget(self):

        self.result_button = Button(self.canvas, text="Get Output")
        self.result_button.grid(row=7, column=1)

    
    def create_widgets(self, main_categories):

        self.intro_widget()
        
        self.category_widget(main_categories)

        self.number_widget()

        self.button_widget()

        self.canvas.grid_rowconfigure((0,2,4,6,8), minsize=50 )
        
        self.canvas.pack()