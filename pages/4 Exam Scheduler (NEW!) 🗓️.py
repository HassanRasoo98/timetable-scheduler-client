# Define the Streamlit app
import os
import pandas as pd
import requests
import streamlit as st
from utils import create_file, get_base_url, initialize_session_state, read_csv_files, results_handler, \
    get_draft_version
    

st.set_page_config(
    page_title="Exam Scheduler (NEW!)",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Examination Scheduler")

try:
    filename = get_draft_version()
    st.info(f"Currently using file : {filename}")
    
except Exception as e:
    st.error("Failed to fetch current draft version!")
    
st.markdown("""
Enter your subjects in box below and click on 'Make Schedule' to retrieve your personal exam schedule.       
""")

base_url = get_base_url()

# Fetch a list of all subjects
all_subjects_url = base_url + "all_exam_subjects"
response = requests.get(all_subjects_url)
if response.status_code == 200:
    data = response.json()
    all_subjects = data.get('all_subjects')
else:
    st.error(f"Failed to fetch subjects. Status code: {response.status_code}, Message : {response.text}")
    st.stop()

# Create a multi-select widget for selecting subjects
selected_subjects = st.multiselect("Select Subjects:", all_subjects)
# Fetch and display the time table for selected subjects
if st.button("Make Schedule"):    
    if not selected_subjects:
        st.warning("Please select at least one subject.")
    else:
        time_table_url = base_url + "exam_scheduler"
        payload = {"selected_subjects": selected_subjects}
        response = requests.post(time_table_url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            time_table = data.get('processed_result')
            # Create a DataFrame for the time table
            results = pd.DataFrame(time_table)
            results_handler(results, 'exam_files')

            # Get all CSV files in a folder
            csv_folder = 'exam_files'
            csv_data = read_csv_files(csv_folder)

            initialize_session_state()
            # Create tabs for each CSV file
            days = [file_name.split('.')[0] for file_name in csv_data.keys()]
            # days = sorted(days, key=get_day_order)
            
            tabs = st.tabs(days)
            
            # fetch name of the available days
            available_days = os.listdir(csv_folder)
            available_days = sorted(available_days) # , key=order_files)
            
            i=0
            for tab in tabs:
                with tab:
                    st.dataframe(csv_data[available_days[i]])      
                    i+=1        
                    
            create_file('exam_files')      

            with open("combined_data.docx", "rb") as file:
                btn=st.download_button(
                label="click me to download timetable",
                data=file,
                file_name="exam schedule.docx",
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

