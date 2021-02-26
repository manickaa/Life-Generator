import os
import threading
import pandas as pd

class Start_Communication:

    def __init__(self):
        
        self.addresses = None
        self.start_person_generator()

    def get_directory(self):
        current_directory = os.getcwd()
        parent_directory = os.path.split(current_directory)[0]
        return (current_directory, parent_directory + "/Person_Generator")

    def monitor_csv(self):
        
        print("Thread started")
        directories = self.get_directory()
        person_generator_directory = directories[1]
        file_name = person_generator_directory + "/output.csv"
        
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

    def start_person_generator(self):
        
        t1 = threading.Thread(target=self.monitor_csv, name="t1")
        t1.start()
        
        life_generator_directory, person_generator_directory = self.get_directory()

        os.chdir(person_generator_directory)
        command = "python3 person-generator.py"
        os.system(command)
        t1.join()
        os.chdir(life_generator_directory)
        return