import pandas as pd 

class Toys_Database_Handler():

    def __init__(self):
        
        self.toys_csv = self.read_kaggle_csv()

    def read_kaggle_csv(self):

        return pd.read_csv("./amazon_co-ecommerce_sample.csv", delimiter= ",")

    def map_categories(self, data):
        
        if pd.isnull(data):
            return []
        else:
            return[cat.strip() for cat in data.split(">")]

    #function creates a unique set of main categories from nested categories
    def create_categories(self):

        category_lists = self.toys_csv["amazon_category_and_sub_category"].apply(self.map_categories)
        return set(category_lists[category_lists.map(lambda c: len(c) > 0)].map(lambda l: l[0]))