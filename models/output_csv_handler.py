import pandas as pd

class Output_CSV_Hander():

    def __init__(self, sorted_toys, input_csv):
        
        self.toys = sorted_toys
        self.input_csv = input_csv
        self.is_input_csv = False

        self.selected_category = None
        self.selected_number = None
    
    def set_is_input_csv(self, bool_value):
        
        self.is_input_csv = bool_value
    
    def set_category(self, category):
        
        self.selected_category = category

    def set_number(self, number):

        self.selected_number = number

    def export_csv(self):
        
        rows = int(self.toys.shape[0])
        input_item_type = ["toys" for i in range(0, rows)]

        categories = []
        nums = []
        
        if self.is_input_csv:
            input_rows = int(self.input_csv.shape[0])
            #get category and number from input.csv
            for i in range(0, input_rows):
                num_to_gen = self.input_csv.iloc[i]["input_number_to_generate"]
                category = self.input_csv.iloc[i]["input_item_category"]
                for _ in range(0, num_to_gen):
                    categories.append(category)
                    nums.append(num_to_gen)
        else:
            #get category and number from GUI
            category = self.selected_category
            num = self.selected_number
            for i in range(0, rows):
                categories.append(category)
                nums.append(num)
        
        final_dataframe = pd.DataFrame({"input_item_type":input_item_type, "input_item_category":categories, "input_number_to_generate":nums})
        
        for i in range(0, rows):
            final_dataframe.at[i, "output_item_name"] = self.toys.iloc[i]["product_name"]
            final_dataframe.at[i, "output_item_rating"] = self.toys.iloc[i]["average_review_rating"]
            final_dataframe.at[i, "output_item_num_reviews"] = self.toys.iloc[i]["number_of_reviews"]

        final_dataframe.to_csv(r'./output.csv', index = False)