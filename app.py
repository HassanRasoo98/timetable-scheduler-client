# run command
# streamlit run app.py

import shutil
import streamlit as st
import requests
import pandas as pd
import json
import os

from utils import format_time, initialize_session_state, read_csv_files, order_files

# API base URL
# base_url = "http://127.0.0.1:5000/" # development url
base_url = "https://hassanrasool.pythonanywhere.com/"

# Define the Streamlit app
st.title("FAST Spring 2024 Timetable Viewer")

# Fetch a list of all subjects
all_subjects_url = base_url + "all-subjects"
response = requests.get(all_subjects_url)
if response.status_code == 200:
    all_subjects = response.json()
else:
    st.error(f"Failed to fetch subjects. Status code: {response.status_code}")
    st.stop()
    
# Function to update the timetable
def get_last_update_time():
    # st.info("Updating timetable...")  # You can customize the message
    update_url = base_url + "get_modification_time"
    response = requests.get(update_url)
    print(response.json())
    if response.status_code == 200:
        st.success("Timetable last updated on {}".format(response.json()))
    else:
        st.error(f"Failed to fetch timetable last update date. Status code: {response.status_code}")

# Load selected subjects from file
def load_selected_subjects():
    if os.path.exists("selected_subjects.json"):
        with open("selected_subjects.json", "r") as file:
            return json.load(file)
    else:
        return []

# Save selected subjects to file
def save_selected_subjects(selected_subjects):
    with open("selected_subjects.json", "w") as file:
        json.dump(selected_subjects, file)
        
get_last_update_time()
# Checkbox for getting the latest timetable
get_latest_timetable = st.checkbox("Get Latest Timetable")

# Create a multi-select widget for selecting subjects
selected_subjects = st.multiselect("Select Subjects:", all_subjects, default=load_selected_subjects())

# Save selected subjects to file
save_selected_subjects(selected_subjects)

def results_handler(result):
    # Create a subfolder named 'results' in the current working directory
    results_folder = 'results'
    
    # remove previouisly fetched results to make space for new ones
    if os.path.exists(os.path.join(os.getcwd(), results_folder)):
        shutil.rmtree(results_folder)
        # print('file removed')
        
    os.makedirs(results_folder, exist_ok=True)
    
    result.drop_duplicates(inplace=True, ignore_index=True)
    result['Start_Time'] = result['Start_Time'].apply(format_time)
    # result['End_Time'] = result['End_Time'].apply(format_time)
    result['Start_Time'] = pd.to_datetime(result['Start_Time'], format='%I:%M %p')

    # Group by 'Day', sort each group, and save as a separate CSV file in the 'results' subfolder
    for day, group in result.groupby('Day'):
        sorted_group = group.sort_values(by='Start_Time')
        csv_file_path = os.path.join(results_folder, f'{day.replace(".xlsx", "")}.csv')
        sorted_group.drop(['Day', 'Start_Time', 'End_Time'], axis=1, inplace=True)
        
        # Desired column order
        desired_order = ['Subject', 'Class', 'Time']

        # Rearrange columns
        sorted_group = sorted_group[desired_order]
        sorted_group.to_csv(csv_file_path, index=False)

    # print("CSV files saved successfully in the 'results' subfolder after sorting and converting time to datetime.")

# Function to update the timetable
def update_timetable():
    st.info("Updating timetable...")  # You can customize the message
    update_url = base_url + "update-timetable"
    response = requests.get(update_url)
    if response.status_code == 200:
        st.success("Timetable updated successfully.")
    else:
        st.error(f"Failed to update timetable. Fatching timetable from previous version. Status code: {response.status_code}")

# Fetch and display the time table for selected subjects
if st.button("Fetch Time Table"):    
    if not selected_subjects:
        st.warning("Please select at least one subject.")
    else:
        # selected_subjects = ['Fund of NLP (AI-JK)', 'PPIT (AI-J)', 'Art Neural Net (AI-J)', 'Info Sec (AI-J)', 'Game Theory (AI-JK)']
        # print('Selected Subjects : ', selected_subjects)
        
        if get_latest_timetable:
            update_timetable()  # Call the function to update the timetable

        time_table_url = base_url + "time-table"
        payload = {"subjects": selected_subjects}
        response = requests.post(time_table_url, json=payload)
        
        if response.status_code == 200:
            time_table = response.json()

            # Create a DataFrame for the time table
            results = pd.DataFrame(time_table)
            results_handler(results)

            # Get all CSV files in a folder
            csv_folder = 'results'
            csv_data = read_csv_files(csv_folder)

            initialize_session_state()
            # Create tabs for each CSV file
            days = [file_name.split('.')[0] for file_name in csv_data.keys()]
            # days = sorted(days, key=get_day_order)
            
            tabs = st.tabs(days)
            
            # fetch name of the available days
            available_days = os.listdir(csv_folder)
            available_days = sorted(available_days, key=order_files)
            
            i=0
            for tab in tabs:
                with tab:
                    st.dataframe(csv_data[available_days[i]])      
                    i+=1              

            # # Create a button for downloading the timetable data as a CSV file
            # csv_data = df.to_csv(index=False, encoding='utf-8-sig')
            # b64 = base64.b64encode(csv_data.encode()).decode()
            # button_label = "Download Timetable as CSV"
            # href = f'<a href="data:file/csv;base64,{b64}" download="timetable.csv">Download Timetable as CSV</a>'
            # st.markdown(href, unsafe_allow_html=True)

# Add an email link
st.markdown(
    """
    <div style="text-align: center; font-size: small; margin-top: 20px;">
        Feedback, complaints, and suggestions: hassanrasool1057@gmail.com
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div style="text-align: center; font-size: small; margin-top: 20px;">Credits: Hassan Rasool, Umar Waseem, and Talal Muzaffar 🚀</div>', unsafe_allow_html=True)


