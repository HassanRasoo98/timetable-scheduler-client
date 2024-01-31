import streamlit as st

from utils import tab1_empty_classroom_handler, tab2_empty_classroom_handler

st.title("Find Empty Classrooms")
st.markdown("""
Find free classrooms and labs. But be careful they might be locked! Especially if there isn't a lecture scheduled in the class/lab after the selected/current timeslot.            
""")

tab1, tab2 = st.tabs(['Specific Timeslot', 'Right Now'])

with tab1:
    tab1_empty_classroom_handler()
    
with tab2:
    tab2_empty_classroom_handler()
    
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


