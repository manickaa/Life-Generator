from tkinter import *
from tkinter.ttk import *

class Output_Widgets():

    def __init__(self, total_rows, sorted_toys, category, canvas):
        
        self.canvas = canvas
        self.total_rows = total_rows
        self.sorted_toys = sorted_toys
        self.category = category
        
        self.is_input_file = False
        self.addresses = None
        self.is_address = False

    def set_is_input_file(self, bool_value):
        
        self.is_input_file = bool_value

    def set_address(self, addresses):

        if(addresses is not None):
            self.is_address = True
        self.addresses = addresses

    #creates treeview for holding the outputs as a table
    def create_tree(self, column_names):
        
        if(self.is_address):
            column_names.append("addresses")
        
        tree = Treeview(self.canvas, selectmode="extended", columns=tuple(column_names), height="15", show="headings")
        tree.pack(side=LEFT, expand=YES, fill=BOTH)
        tree.place(x=10, y=50)
        
        #assign headings to the columns
        tree.heading("#0", text="")
        tree.heading("#1", text="S.NO")
        tree.heading("#2", text="TYPE")
        tree.heading("#3", text="PRODUCT NAME")
        tree.heading("#4", text="AVERAGE RATING")
        tree.heading("#5", text="N0. OF REVIEWS")
        
        if(self.is_address):
            tree.heading("#6", text="ADDRESSES")
        
        #specify the attributes of each column
        tree.column("#1", stretch=NO, width=50)
        tree.column("#2", stretch=NO, width=150)
        tree.column("#3", stretch=YES, minwidth=100, width=400)
        tree.column("#4", stretch=YES)
        tree.column("#5", stretch=NO, width=100)
        
        if(self.is_address):
            tree.column("#6",stretch=YES, minwidth=100, width=200)
        
        return tree

    #creates widgets for output in GUI #canvas2
    def create_table_layout(self):
        
        results_label = Label(self.canvas, text = "RESULTS:")
        results_label.place(x=10, y=20)

        column_names = ["serial_num", "amazon_category","product_name", "average_review_rating", "number_of_reviews"]
        tree = self.create_tree(column_names)

        #insert each row into the treeview
        for i in range(1, self.total_rows+1):
            if self.is_input_file:
                category = self.sorted_toys.iloc[i-1]["amazon_category_and_sub_category"]
                category_list = category.split(" >", 1)
                self.category = category_list[0]
            if self.is_address:
                tree.insert("","end",iid=i+1, text=str(i-1), values=(str(i), self.category, self.sorted_toys.iloc[i-1][column_names[2]], self.sorted_toys.iloc[i-1][column_names[3]], self.sorted_toys.iloc[i-1][column_names[4]], self.addresses.iloc[i-1]["VALUE"]))
            else:
                tree.insert("","end",iid=i+1, text=str(i-1), values=(str(i), self.category, self.sorted_toys.iloc[i-1][column_names[2]], self.sorted_toys.iloc[i-1][column_names[3]], self.sorted_toys.iloc[i-1][column_names[4]]))
                
        self.canvas.pack()