from tkinter import *
from tkinter.ttk import *

class Output_Widgets():

    def __init__(self, total_rows, sorted_toys, canvas):
        
        self.canvas = canvas
        self.total_rows = total_rows
        self.sorted_toys = sorted_toys
        
        self.is_input_file = False
        self.addresses = None
        self.is_address = False

        self.category = None

    def set_category(self, category):
        
        self.category = category

    def set_is_input_file(self, bool_value):
        
        self.is_input_file = bool_value

    def set_address(self, addresses):

        if(addresses is not None):
            self.is_address = True
        self.addresses = addresses

    def assign_headings(self):

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="S.NO")
        self.tree.heading("#2", text="TYPE")
        self.tree.heading("#3", text="PRODUCT NAME")
        self.tree.heading("#4", text="AVERAGE RATING")
        self.tree.heading("#5", text="N0. OF REVIEWS")
        
        if(self.is_address):
            self.tree.heading("#6", text="ADDRESSES")

    def assign_attributes(self):

        self.tree.column("#1", stretch=NO, width=50)
        self.tree.column("#2", stretch=NO, width=150)
        self.tree.column("#3", stretch=YES, minwidth=100, width=400)
        self.tree.column("#4", stretch=YES)
        self.tree.column("#5", stretch=NO, width=100)
        
        if(self.is_address):
            self.tree.column("#6",stretch=YES, minwidth=100, width=400)
        
    #treeview for holding the outputs as a table
    def create_tree(self, column_names):
        
        if(self.is_address):
            column_names.append("addresses")
        
        self.tree = Treeview(self.canvas, selectmode="extended")
        self.tree["columns"] = tuple(column_names)
        self.tree["height"] = "15"
        self.tree["show"] = "headings"
        self.tree.pack(side=LEFT, expand=YES, fill=BOTH)
        self.tree.place(x=10, y=50)
        
        self.assign_headings()
        
        self.assign_attributes()

    def result_label_widget(self):

        results_label = Label(self.canvas, text = "RESULTS:")
        results_label.place(x=10, y=20)

    def assign_category_from_toys(self, row_num):
        
        category = self.sorted_toys.iloc[row_num-1]["amazon_category_and_sub_category"]
        category_list = category.split(" >", 1)
        self.category = category_list[0]

    def append_toy_data(self, data, row_num, column_names):
        
        for i in range(2, 5):
            data.append(self.sorted_toys.iloc[row_num-1][column_names[i]])
    
    def insert_rows(self, column_names):

        for i in range(1, self.total_rows+1):
            
            if self.is_input_file: #since toys from multiple category are requested with input.csv   
                self.assign_category_from_toys(i)
            
            column_values = [str(i), self.category]
            self.append_toy_data(column_values, i, column_names)
            
            if self.is_address:
                column_values.append(self.addresses.iloc[i-1]["VALUE"])
                self.tree.insert("","end",iid=i+1, text=str(i-1), values=tuple(column_values))
            else:
                self.tree.insert("","end",iid=i+1, text=str(i-1), values=tuple(column_values))
    
    def create_table_layout(self):
        
        self.result_label_widget()

        column_names = [
            "serial_num", "amazon_category",
            "product_name", "average_review_rating", "number_of_reviews"
        ]
        self.create_tree(column_names)

        self.insert_rows(column_names)
                
        self.canvas.pack()