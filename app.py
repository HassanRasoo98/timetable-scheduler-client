# run command
# streamlit run app.py

import os
import streamlit as st
import requests
import pandas as pd
from streamlit_star_rating import st_star_rating
from utils import get_last_update_time, initialize_session_state, read_csv_files, order_files, \
        create_file, results_handler, update_timetable, send_rating_to_server, fetch_current_rating

# API base URL
base_url = "http://127.0.0.1:5000/" # development url
# base_url = "https://hassanrasool.pythonanywhere.com/" # production url

# Fetch the current rating from the server
current_rating, total = fetch_current_rating(base_url)

# Display the fetched rating on the top left corner using st.sidebar
with st.sidebar:
    st.write("Current Rating:")
    st.write(current_rating)
    
    st.write("Total Votes")
    st.write(total)

# Define the Streamlit app
st.title("FAST Spring 2024 Timetable Viewer")

st.divider()
st.markdown('Update Timetable')
can_update, time_difference = get_last_update_time(base_url)

if can_update:
    # Checkbox for getting the latest timetable
    get_latest_timetable = st.checkbox("Get Latest Timetable")
else:
    st.markdown(f"TimeTable was updated {time_difference} ago. Max waiting time to update is more than 30 minutes. The above modification time is according to server timezone (GMT).")

if can_update and get_latest_timetable:
    update_timetable(base_url)  # Call the function to update the timetable
    
st.divider()

tab1, tab2 = st.tabs(['Make TimeTable', 'Find Empty Classrooms (NEW!)'])
with tab1:
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
                    
with tab2:        
    # Fetch a list of all files
    all_files_url = base_url + "get_files"
    response = requests.get(all_files_url)
    files = None
    
    if response.status_code == 200:
        files = response.json()
    else:
        st.error(f"Failed to fetch files. Status code: {response.status_code}")
        st.stop()
        
     # Create a multi-select widget for selecting subjects
    selected_file = st.selectbox("Select Day:", files)   
    # print('selected file : ', selected_file)
    
    # Create two radio buttons side by side
    stype = st.radio('Find in : ', ('Room', 'Lab'))
    url = base_url + "selected-file"
    payload = {"file": selected_file, "selection_type": stype}
    response1 = requests.post(url, json=payload)    
    timeslots = response1.json()
    # print(timeslots)
    
    with st.form(key="form"):
        selected_timeslot = st.selectbox("Select a timeslot:", timeslots)
        submit_button = st.form_submit_button(label="Find Empty Rooms")
        # print(f'selected_timeslot {selected_timeslot}')  
        
    if submit_button:
        # print(f'selected_timeslot after clicking button {selected_timeslot}') 
        # print('button clicked')
        free_room_url = base_url + "get-free-room"
        # print(free_room_url)
        payload = {"timeslot": selected_timeslot}
        free_room_url_response = requests.post(free_room_url, json=payload)
        
        if free_room_url_response.status_code == 200:
            result = free_room_url_response.json()
            df = pd.DataFrame(result, columns=['Free Rooms'])

            st.table(df)
            
        else:
            st.error(f"Failed to fetch timetable. Status code: {free_room_url_response.status_code}")
            # print(free_room_url_response)            

st.divider()
stars = st_star_rating("Please rate your experience", size = 20, maxValue=5, defaultValue=None, key="rating")
# print(stars)
st.divider()
send_rating_to_server(stars, base_url)

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




