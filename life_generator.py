from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import pandas as pd 
import re
import sys
import os
import threading

class Life_Generator(Frame):

    def __init__(self, input_file, pg_addresses, wrapper1=None, wrapper2=None):
        
        Frame.__init__(self, wrapper1)
        Frame.__init__(self, wrapper2)
        
        #canvas to wrap the input area in GUI
        self.canvas1 = Canvas(wrapper1, height=500, width=1500)
        self.canvas1.pack()
        
        #canvas to wrap the output area in GUI
        self.canvas2 = Canvas(wrapper2, height=1500, width=1500)
        self.canvas2.pack()

        self.input_csv = self.read_input_file(input_file)
        
        self.addresses = pg_addresses

        self.category_items = None
        self.num_item = None
        self.toys = None
        
        self.program_control()

    def program_control(self):

        self.read_kaggle_csv()
        main_categories = self.create_categories()
        self.create_widgets(main_categories)

        if self.check_input_csv():
            self.generate_results_for_input_csv()

    def read_input_file(self, input_file):
        
        if(input_file is not None):
            return pd.read_csv(input_file, delimiter=",")
        else:
            return None

    def check_person_generator_data(self):
        if self.addresses is not None:
            return True
        else:
            return False

    def check_input_csv(self):
        
        if self.input_csv is not None:
            return True
        else:
            return False
    
    def read_kaggle_csv(self):
        
        self.toys = pd.read_csv("./amazon_co-ecommerce_sample.csv", delimiter= ",")

    #function splits the nested categories
    def map_categories(self, data):
        
        if pd.isnull(data):
            return []
        else:
            return[cat.strip() for cat in data.split(">")]

    #function creates a unique set of main categories from nested categories
    def create_categories(self):

        category_lists = self.toys["amazon_category_and_sub_category"].apply(self.map_categories)
        return set(category_lists[category_lists.map(lambda c: len(c) > 0)].map(lambda l: l[0]))

    def intro_widget(self):
        
        introText = "Confused about what to buy? We have a bunch of categories to help with your search. \n\
Choose from the options to start your search. \n Also don't forget to enter the number of results you want ;)"

        label = Label(self.canvas1, text= introText)
        label.grid(row=1,column=0)

    def category_widget(self, main_categories):
        
        categoryLabel = Label(self.canvas1, text="Choose a toy category:")
        categoryLabel.grid(row=3, column=0)

        self.category_items = Combobox(self.canvas1)
        self.category_items.grid(row=3, column=1)
        self.category_items["values"] = tuple(option for option in main_categories) 
    
    def number_widget(self):

        number_label = Label(self.canvas1, text="Enter/Choose the number of results to generate:")
        number_label.grid(row=5, column=0)

        self.num_item = Spinbox(self.canvas1, from_=1, to=10000)
        self.num_item.grid(row=5, column=1)

    def button_widget(self):

        result_button = Button(self.canvas1, text="Get Output")
        result_button.grid(row=7, column=1)

        #button disabled when input.csv is not given by the user
        if not self.check_input_csv():
            result_button["command"] = self.handle_button_click
        else:
            result_button["state"] = DISABLED
    
    #function to create widgets for input in GUI #canvas1
    def create_widgets(self, main_categories):

        self.intro_widget()
        
        self.category_widget(main_categories)

        self.number_widget()

        self.button_widget()

        self.canvas1.grid_rowconfigure((0,2,4,6,8), minsize=50 )
        self.canvas1.pack()
    
    
    def filter_by_category(self, input_item_category):
        
        boolean = []
        for result in self.toys.amazon_category_and_sub_category:
            if re.search(input_item_category, str(result)): 
                boolean.append(True)
            else:
                boolean.append(False)
        
        filtered_category = pd.Series(boolean) #adds the boolean column for filtering

        self.toys_by_category = self.toys[filtered_category]
    
    #The data from average_review_rating is split, converted to float and assigned to the newly created ratings column
    def add_ratings(self):

        rating = []
        for result in self.toys_by_category.average_review_rating:
            if type(result) == str:
                splitList = result.split(" ", 1)
                rating.append(float(splitList[0]))
            else:
                rating.append(0)
        self.toys_with_ratings = self.toys_by_category.assign(ratings = rating)

    #message box pop-up when inputs are not given by the user
    def check_errors(self, input_item_category, input_number_to_generate):
        
        if ((not str(input_item_category)) or (not str(input_number_to_generate))):
            messagebox.showerror("Error", "Check if all inputs are entered")
            return True
        else:
            return False
    
    #assign rows based on the value(num to generate) given by user exceeds the number of results actually available or not
    def get_rows(self, user_input, sorted_toys):
        
        if sorted_toys.shape[0] >= int(user_input):
            return int(user_input)
        else:
            return sorted_toys.shape[0]
    
    def handle_button_click(self):

        input_item_category = self.category_items.get()
        input_number_to_generate = self.num_item.get()

        if(self.check_errors(input_item_category, input_number_to_generate)):
            return
        
        self.filter_by_category(input_item_category)
        self.add_ratings()
        sorted_toys = self.sort_results(input_number_to_generate)
        
        rows = self.get_rows(input_number_to_generate, sorted_toys)

        self.create_table_layout(rows, input_item_category, sorted_toys)
        self.export_csv(sorted_toys)
    
    #Function changes the reviews of type string to numeric and stores it in a new column
    def add_review_column(self):
        review = []
        for result in self.toys_with_ratings.number_of_reviews:
            if type(result) == str:
                number = int(result.replace(",", ""))
                review.append(number)
            else:
                review.append(0)
        self.toys_with_ratings = self.toys_with_ratings.assign(reviews = review)
    
    #Function sorts by unique id in ascending and then sorts by number of reviews in descending order
    def sort_by_review(self):
        
        self.add_review_column()    
        sorted_by_id = self.toys_with_ratings.sort_values(by=["uniq_id"])
        return sorted_by_id.sort_values(by=["reviews"], ascending=[False])

    #Function sorts by unique id in ascending and then sorts by ratings in descending order
    def sort_by_rating(self, filtered_toys):

        sorted_by_id = filtered_toys.sort_values(by=["uniq_id"])
        return sorted_by_id.sort_values(by=["ratings"], ascending=[False])

    #Take the X*10 results
    def get_ten_x_results(self, num_results, sorted_by_review):

        if(int(num_results)*10 > sorted_by_review.shape[0]): #Check to adjust if the X*10 qty exceeds the actual qty.
            rows = sorted_by_review.shape[0]
        else:
            rows = int(num_results)*10
        
        return sorted_by_review[0:rows]
    
    #sort the data based on the given algorithm
    def sort_results(self, num_results):
       
        sorted_by_review = self.sort_by_review()
        
        filtered_toys = self.get_ten_x_results(num_results, sorted_by_review)

        sorted_by_rating = self.sort_by_rating(filtered_toys)
        
        #Take X results
        return sorted_by_rating[0:int(num_results)]
    
    def generate_results_for_input_csv(self):
        
        num_rows = int(self.input_csv.shape[0])

        output_dataframe = pd.DataFrame()

        #For each input, filter by category, add rating column, sort the results and add it to the dataframe
        for i in range(0, num_rows):
            self.filter_by_category(self.input_csv["input_item_category"][i])
            self.add_ratings()
            num_results = self.input_csv["input_number_to_generate"][i]
            
            sorted_results = self.sort_results(num_results)

            output_dataframe = output_dataframe.append(sorted_results)

        #Get the number of rows of results generated
        total_results = int(output_dataframe.shape[0])
        
        self.create_table_layout(total_results, None, output_dataframe)
        self.export_csv(output_dataframe)
        return
    
    #creates treeview for holding the outputs as a table
    def create_tree(self, column_names):
        
        if(self.check_person_generator_data()):
            column_names.append("addresses")
        
        tree = Treeview(self.canvas2, selectmode="extended", columns=tuple(column_names), height="15", show="headings")
        tree.pack(side=LEFT, expand=YES, fill=BOTH)
        tree.place(x=10, y=50)
        
        #assign headings to the columns
        tree.heading("#0", text="")
        tree.heading("#1", text="S.NO")
        tree.heading("#2", text="TYPE")
        tree.heading("#3", text="PRODUCT NAME")
        tree.heading("#4", text="AVERAGE RATING")
        tree.heading("#5", text="N0. OF REVIEWS")
        
        if(self.check_person_generator_data()):
            tree.heading("#6", text="ADDRESSES")
        
        #specify the attributes of each column
        tree.column("#1", stretch=NO, width=50)
        tree.column("#2", stretch=NO, width=150)
        tree.column("#3", stretch=YES, minwidth=100, width=400)
        tree.column("#4", stretch=YES)
        tree.column("#5", stretch=NO, width=100)
        
        if(self.check_person_generator_data()):
            tree.column("#6",stretch=YES, minwidth=100, width=200)
        
        return tree

    #creates widgets for output in GUI #canvas2
    def create_table_layout(self, rows, category, toys):
        
        results_label = Label(self.canvas2, text = "RESULTS:")
        results_label.place(x=10, y=20)

        column_names = ["serial_num", "amazon_category","product_name", "average_review_rating", "number_of_reviews"]
        tree = self.create_tree(column_names)

        #insert each row into the treeview
        for i in range(1, rows+1):
            if self.check_input_csv():
                category = toys.iloc[i-1]["amazon_category_and_sub_category"]
                category_list = category.split(" >", 1)
                category = category_list[0]
            if self.check_person_generator_data():
                tree.insert("","end",iid=i+1, text=str(i-1), values=(str(i), category, toys.iloc[i-1][column_names[2]], toys.iloc[i-1][column_names[3]], toys.iloc[i-1][column_names[4]], self.addresses.iloc[i-1]["VALUE"]))
            else:
                tree.insert("","end",iid=i+1, text=str(i-1), values=(str(i), category, toys.iloc[i-1][column_names[2]], toys.iloc[i-1][column_names[3]], toys.iloc[i-1][column_names[4]]))
                
        self.canvas2.pack()

    #Function to write the results in csv file and download it in the same directory
    def export_csv(self, toys):
        
        rows = int(toys.shape[0])
        input_item_type = ["toys" for i in range(0, rows)]

        categories = []
        nums = []
        
        if self.check_input_csv():
            inputRows = int(self.input_csv.shape[0])
            #get category and number from input.csv
            for i in range(0, inputRows):
                num_to_gen = self.input_csv.iloc[i]["input_number_to_generate"]
                category = self.input_csv.iloc[i]["input_item_category"]
                for _ in range(0, num_to_gen):
                    categories.append(category)
                    nums.append(num_to_gen)
        else:
            #get category and number from GUI
            category = self.category_items.get()
            num = self.num_item.get()
            for i in range(0, rows):
                categories.append(category)
                nums.append(num)
        
        final_dataframe = pd.DataFrame({"input_item_type":input_item_type, "input_item_category":categories, "input_number_to_generate":nums})
        
        for i in range(0, rows):
            final_dataframe.at[i, "output_item_name"] = toys.iloc[i]["product_name"]
            final_dataframe.at[i, "output_item_rating"] = toys.iloc[i]["average_review_rating"]
            final_dataframe.at[i, "output_item_num_reviews"] = toys.iloc[i]["number_of_reviews"]

        final_dataframe.to_csv(r'./output.csv', index = False)
        
class Person_Generator:

    def __init__(self):
        
        self.addresses = None
        self.get_person_generator()


    def get_directory(self):
        current_directory = os.getcwd()
        parent_directory = os.path.split(current_directory)[0]
        return (current_directory, parent_directory + "/Person_Generator")

    def monitor_csv(self):
        
        print("Thread started")
        directories = self.get_directory()
        person_generator_directory = directories[1]
        file_name = person_generator_directory + "/output_PG.csv"
        
        stop_thread = False 
        while stop_thread is False:
            if(os.path.isfile(file_name)):
                current_time = os.path.getmtime(file_name)
                print(current_time)
                check = True
                while check:
                    updated_time = os.path.getmtime(file_name)
                    if updated_time != current_time:
                        self.addresses = pd.read_csv(file_name, delimiter= ",")
                        print(updated_time, current_time)
                        check = False
                stop_thread = True
                print(stop_thread)
        print("Thread terminated")

    def get_person_generator(self):
        
        t1 = threading.Thread(target=self.monitor_csv, name="t1")
        t1.start()
        
        life_generator_directory, person_generator_directory = self.get_directory()

        os.chdir(person_generator_directory)
        command = "python3 person-generator.py"
        os.system(command)
        t1.join()
        os.chdir(life_generator_directory)
        return

def prompt_user():
        
        user_choice = input("Would like to get data from Person Generator? (Y/N)")
        return user_choice

if __name__ == "__main__":
    
    input_file, addresses = None, None
    
    #get the input file name, if given
    if(len(sys.argv) >= 2):
        input_file =  sys.argv[1]
    else:
        user_choice = prompt_user()
        input_file = None
        if(user_choice == "Y"):
            microservice_two = Person_Generator()
            addresses = microservice_two.addresses
    
    #create a tkinter window
    root= Tk()
    root.title("Life Generator")
    root.geometry("1500x800")
    app = Life_Generator(input_file, addresses, root, root)
    root.resizable(False, False) #fixed window
    root.mainloop()