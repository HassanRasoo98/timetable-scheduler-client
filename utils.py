import os
import re
import pandas as pd
import streamlit as st

# Function to read CSV files from a folder
def read_csv_files(folder_path):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    # sort the files according to the day names
    csv_files = sorted(csv_files, key=order_files)
    
    print('csv files : ', csv_files)
    dfs = {file: pd.read_csv(os.path.join(folder_path, file)) for file in csv_files}
    
    return dfs

# Initialize session_state
def initialize_session_state():
    if 'selected_tab' not in st.session_state:
        st.session_state.selected_tab = None
        
def order_files(file):
    order = {
        "Monday.csv": 1,
        "Tuesday.csv": 2,
        "Wednesday.csv": 3,
        "Thursday.csv": 4,
        "Friday.csv": 5,
        "Saturday.csv": 6,
        "Sunday.csv": 7
    }
    return order.get(file, 0)
  
def extract_numbers(input_string):
    # Use regex to find all numeric values in the string
    numbers = re.findall(r'\d+', input_string)
    return [int(number) for number in numbers]

def format_time(time):
    hour = extract_numbers(time)[0]

    if hour >= 8 and hour < 12:
        return time + ' AM'
        
    else:
        return time + ' PM'
         
# # Define a custom key function to get the order of days
# def get_day_order(day):
#     order = {
#         "Monday": 1,
#         "Tuesday": 2,
#         "Wednesday": 3,
#         "Thursday": 4,
#         "Friday": 5,
#         "Saturday": 6,
#         "Sunday": 7
#     }
#     return order.get(day, 0)
