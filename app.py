# run command
# streamlit run Home.py

import os
import pandas as pd
import requests
import streamlit as st
from st_pages import Page, show_pages
from utils import create_file, get_base_url, initialize_session_state, order_files, \
    read_csv_files, results_handler
    
# Specify what pages should be shown in the sidebar, and what their titles
# and icons should be
show_pages([
    Page("app.py", "Home", "🏠"),
    Page("pages/page2.py", "Find Empty Classrooms", "🔎"),
    Page("pages/page3.py", "Update TimeTable", "🔃"),
    Page("pages/page4.py", "About", "💡"),
    Page("pages/page5.py", "Feedback", "💬")
])


base_url = get_base_url()

# show_rating(base_url)

# Define the Streamlit app
st.title("FAST Spring 2024 Timetable Viewer")

st.markdown("""
Enter your subjects in box below and click on 'Fetch Timetable' to retrieve your personal schedule.       
""")

# Fetch a list of all subjects
all_subjects_url = base_url + "all-subjects"
response = requests.get(all_subjects_url)
if response.status_code == 200:
    all_subjects = response.json()
else:
    st.error(f"Failed to fetch subjects. Status code: {response.status_code}")
    st.stop()

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
                
            st.markdown('''Disclaimer: It is advisable to compare this timetable once with the original 
                        one provided by the university to minimize any error. 
                        Please report any inconsistencies!''', )

st.divider()

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




