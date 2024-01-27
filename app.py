# run command
# streamlit run app.py

import os
import streamlit as st
import requests
import pandas as pd
from utils import get_last_update_time, initialize_session_state, read_csv_files, \
                    order_files, create_file, results_handler, update_timetable

# API base URL
# base_url = "http://127.0.0.1:5000/" # development url
base_url = "https://hassanrasool.pythonanywhere.com/" # production url

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
        
can_update, time_difference = get_last_update_time(base_url)

if can_update:
    # Checkbox for getting the latest timetable
    get_latest_timetable = st.checkbox("Get Latest Timetable")
else:
    st.markdown(f"TimeTable was updated {time_difference} ago. Max waiting time to update is more than 30 minutes. The above modification time is according to server timezone (GMT).")

# Create a multi-select widget for selecting subjects
selected_subjects = st.multiselect("Select Subjects:", all_subjects)
if '05:20 - 08:05 (inc. 10 min. break)' in selected_subjects:
  selected_subjects.remove('05:20 - 08:05 (inc. 10 min. break)')

# Fetch and display the time table for selected subjects
if st.button("Fetch Time Table"):    
    if not selected_subjects:
        st.warning("Please select at least one subject.")
    else:
        # selected_subjects = ['Fund of NLP (AI-JK)', 'PPIT (AI-J)', 'Art Neural Net (AI-J)', 'Info Sec (AI-J)', 'Game Theory (AI-JK)']
        # print('Selected Subjects : ', selected_subjects)
        
        if can_update and get_latest_timetable:
            update_timetable(base_url)  # Call the function to update the timetable

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
                    
            create_file()      

            with open("combined_data.docx", "rb") as file:
                btn=st.download_button(
                label="click me to download timetable",
                data=file,
                file_name="timetable.docx",
                mime="application/octet-stream"
            )


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


