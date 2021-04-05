import pandas as pd

class Input_CSV_Handler():

    def __init__(self, input_file):
        
        self.input_csv =  self.read_input_file(input_file)
    
    def read_input_file(self, input_file):
        
        if(input_file is not None):
            return pd.read_csv(input_file, delimiter=",")
        else:
            return None

    def has_input_csv(self):
        
        if self.input_csv is not None:
            return True
        else:
            return False