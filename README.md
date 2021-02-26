# Life-Generator
Simple python microservice which displays data based on the input.

Life Generator Software Overview:

Use case 1 - Input.csv is not given

The inputs - Toy category and number to generate are given via GUI
Output - Outputs are shown in a table in GUI and also downloaded as 'output.csv' in the same directory

Use case 2 - Input.csv is given

The inputs - Specified in the csv file
Output - Shown in GUI and also downloaded as 'output.csv' in the same directory

Use case 3 - When we want to get data from person generator

When ```python3 life_generator.py``` is run, the command line terminal prompts the user whether they would like to get data from person generator.

If user types "Y", data is requested to person-generator and response data is displayed in GUI [You would need to give life-generator inputs in GUI inorder to place the address data corresponding to toys data].

If user types "N", use case 1 is followed


Dependencies to install:
    
    - Pandas
    
    To install, run the following command:
    
    ```$ pip install pandas```


Software Architecture:
    
    Database - amazon_co-ecommerce_sample.csv
    Program control - life_generator.py

How to run the Software?

    For use case 1 - $ python3 life_generator.py
    For use case 2 - $ python3 life_generator.py input.csv