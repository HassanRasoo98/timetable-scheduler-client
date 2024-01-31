
import streamlit as st
from utils import get_base_url, get_last_update_time, update_timetable

base_url = get_base_url()

st.title('Update Timetable')

st.write('''It is preferred to use the latest timetable especially in the first 
            2 weeks of classes to accommodate for any changes.''')

can_update, time_difference = get_last_update_time(base_url)

if can_update:
    # Button for getting the latest timetable
    get_latest_timetable = st.button("Get Latest Timetable")
else:
    st.markdown(f"TimeTable was updated {time_difference} ago. Max waiting time to update is more than 30 minutes. The above modification time is according to server timezone (GMT).")

if can_update and get_latest_timetable:
    update_timetable(base_url)  # Call the function to update the timetable
    
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




                      
