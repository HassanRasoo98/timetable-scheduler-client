import os
import re
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta, timezone

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
         
def allow_update(provided_datetime_str):
    print(provided_datetime_str)
    provided_datetime = datetime.strptime(provided_datetime_str, "%a, %d %b %Y %H:%M:%S %Z")
    provided_datetime = datetime.strptime(provided_datetime_str, "%a, %d %b %Y %H:%M:%S %Z")
    provided_datetime = provided_datetime.replace(tzinfo=timezone.utc)

    # Current datetime with timezone
    current_datetime = datetime.now(timezone.utc)
    print(current_datetime)

    # Calculate the difference
    time_difference = current_datetime - provided_datetime
    # Convert to total seconds
    total_seconds = time_difference.total_seconds()

    # Format the time in a human-readable way
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    print("Time difference:", time_difference)
    
    time_string = "{} h, {} m, {} s".format(hours, minutes, seconds)

    # Specify the maximum allowed duration (30 minutes)
    max_allowed_duration = timedelta(minutes=30)

    # Check if the difference is less than half an hour
    if time_difference < max_allowed_duration:
        return False, time_string # do not allow update, last update was less than 30 minutes ago
    else:
        return True, time_string
