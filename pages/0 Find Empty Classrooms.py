import pandas as pd
import requests
import streamlit as st

from utils import get_base_url

base_url = get_base_url()

st.title("Find Empty Classrooms")

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




