import re
import pandas as pd 

class Sort_Handler():

    def __init__(self, toys, category, number):
        
        self.toys = toys.toys_csv
        self.selected_category = category
        self.selected_num = number
        self.prepare_for_sort()
    
    def prepare_for_sort(self):
        
        self.filter_by_category()
        self.add_ratings_column()
        self.add_review_column()
    
    def filter_by_category(self):
        
        boolean = []
        for result in self.toys.amazon_category_and_sub_category:
            if re.search(self.selected_category, str(result)): 
                boolean.append(True)
            else:
                boolean.append(False)
        
        filtered_category = pd.Series(boolean) #adds the boolean column for filtering

        self.toys_by_category = self.toys[filtered_category]
    
    #The data from average_review_rating is split, converted to float and assigned to the newly created ratings column
    def add_ratings_column(self):

        rating = []
        
        for result in self.toys_by_category.average_review_rating:
            if type(result) == str:
                split_list = result.split(" ", 1)
                rating.append(float(split_list[0]))
            else:
                rating.append(0)
        
        self.toys_with_ratings = self.toys_by_category.assign(ratings = rating)

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

    #Function sorts by unique id in ascending and then sorts by column in descending order
    def sort_by_column(self, toys, column):
        
        sorted_by_id = toys.sort_values(by=["uniq_id"])
        return sorted_by_id.sort_values(by=[column], ascending=[False])

    def get_ten_x_results(self, sorted_by_review):

        if(int(self.selected_num)*10 > sorted_by_review.shape[0]): #Check to adjust if the X*10 qty exceeds the actual qty.
            rows = sorted_by_review.shape[0]
        else:
            rows = int(self.selected_num)*10
        
        return sorted_by_review[0:rows]
    
    def sort_results(self):
       
        sorted_by_review = self.sort_by_column(self.toys_with_ratings, "reviews")
        
        filtered_toys = self.get_ten_x_results(sorted_by_review)

        sorted_by_rating = self.sort_by_column(filtered_toys, "ratings")
        
        #Take X results
        return sorted_by_rating[0:int(self.selected_num)]
    
