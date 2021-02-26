from imports import *

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

        self.addresses = pg_addresses
        
        self.toys = Toys_Database_Handler()
        
        self.input = Input_CSV_Handler(input_file)

        main_categories = self.toys.create_categories()
        self.input_widgets = Input_Widgets(main_categories, self.canvas1)

        self.program_control()

    def program_control(self):

        if(not self.input.check_input_csv()):
            self.input_widgets.result_button["command"] = self.handle_button_click
        else:
            self.input_widgets.result_button["state"] = DISABLED
            self.generate_results_for_input_csv()

    def show_output(self, rows, toys, category):
        
        output_widgets = Output_Widgets(rows, toys, category, self.canvas2)
        output_widgets.set_is_input_file(self.input.check_input_csv())
        output_widgets.set_address(self.addresses)
        output_widgets.create_table_layout()

    def handle_output_csv(self, toys, category, number):

        output_csv = Output_CSV_Hander(toys, self.input.input_csv)
        output_csv.set_category(category)
        output_csv.set_number(number)
        output_csv.set_is_input_csv(self.input.check_input_csv())
        output_csv.export_csv()

    def handle_button_click(self):

        input_item_category = self.input_widgets.category_items.get()
        input_number_to_generate = self.input_widgets.num_item.get()

        if(self.check_errors(input_item_category, input_number_to_generate)):
            return
        
        sorted = Sort_Handler(self.toys, input_item_category, input_number_to_generate)
        
        sorted_toys = sorted.sort_results()
        
        rows = self.get_rows(input_number_to_generate, sorted_toys)

        self.show_output(rows, sorted_toys, input_item_category)
        
        self.handle_output_csv(sorted_toys, input_item_category, input_number_to_generate)

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

    def generate_results_for_input_csv(self):
        
        num_rows = int(self.input.input_csv.shape[0])

        output_dataframe = pd.DataFrame()

        for i in range(0, num_rows):
            
            category = self.input.input_csv["input_item_category"][i]
            number = self.input.input_csv["input_number_to_generate"][i]
            
            sorted = Sort_Handler(self.toys, category, number)
            sorted_toys = sorted.sort_results()
            output_dataframe = output_dataframe.append(sorted_toys)

        total_results = int(output_dataframe.shape[0])
        
        self.show_output(total_results, output_dataframe, None)
        
        self.handle_output_csv(output_dataframe, None, None)
        
        return
        

def create_tkinter(input_file, addresses):

    root= Tk()
    root.title("Life Generator")
    root.geometry("1500x800")
    Life_Generator(input_file, addresses, root, root)
    root.resizable(False, False) #fixed window
    root.mainloop()

def prompt_user():
        
    user_choice = input("Would like to get data from Person Generator? (Y/N)")
    return user_choice

def get_inputs(cli_arguments):

    input_file = None
    addresses = None

    if(len(cli_arguments) >= 2):
        input_file = cli_arguments[1]    
    else:
        user_choice = prompt_user()
        if(user_choice == "Y"):
            microservice_two = Start_Communication()
            addresses = microservice_two.addresses
    
    return (input_file, addresses)
    

if __name__ == "__main__":
    
    input_file, addresses = get_inputs(sys.argv)
    create_tkinter(input_file, addresses)
    