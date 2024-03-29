import pandas as pd

class Output_CSV_Hander():

    def __init__(self, sorted_toys, input_csv):
        
        self.toys = sorted_toys
        self.input_csv = input_csv
        self.is_input_csv = False

        self.rows = 0

        self.selected_category = None
        self.selected_number = None
    
    def set_is_input_csv(self, bool_value):
        
        self.is_input_csv = bool_value
    
    def set_category(self, category):
        
        self.selected_category = category

    def set_number(self, number):

        self.selected_number = number

    def get_types(self):

        return ["toys" for i in range(0, self.rows)]

    def create_lists_with_input_csv(self):
        
        categories, nums = [], []
        input_rows = int(self.input_csv.shape[0])    
        
        for i in range(0, input_rows):
            num_to_gen = self.input_csv.iloc[i]["input_number_to_generate"]
            category = self.input_csv.iloc[i]["input_item_category"]
            for _ in range(0, num_to_gen):
                categories.append(category)
                nums.append(num_to_gen)
        return categories, nums

    def create_lists_with_user_input(self):

        categories, nums = [], []
        
        category = self.selected_category
        num = self.selected_number
        
        for _ in range(0, self.rows):
            categories.append(category)
            nums.append(num)
        
        return categories, nums
        
    def get_inputs_as_list(self):
        
        if self.is_input_csv:
            return self.create_lists_with_input_csv()    
        else:
            return self.create_lists_with_user_input()
            
    
    def create_final_dataframe(self, types, categories, nums):

        final_dataframe = pd.DataFrame({"input_item_type":types, 
            "input_item_category":categories, "input_number_to_generate":nums
        })
        
        item_name, item_rating = "output_item_name","output_item_rating"
        item_reviews = "output_item_num_reviews"

        for i in range(0, self.rows):
            final_dataframe.at[i, item_name] = self.toys.iloc[i]["product_name"]
            final_dataframe.at[i, item_rating] = self.toys.iloc[i]["average_review_rating"]
            final_dataframe.at[i, item_reviews] = self.toys.iloc[i]["number_of_reviews"]

        return final_dataframe

    def prepare_to_export_csv(self):

        self.rows = int(self.toys.shape[0])

        types = self.get_types()
        categories, nums = self.get_inputs_as_list()

        return self.create_final_dataframe(types, categories, nums)

    def export_csv(self):
        
        final_dataframe = self.prepare_to_export_csv()

        final_dataframe.to_csv(r"./output.csv", index = False)