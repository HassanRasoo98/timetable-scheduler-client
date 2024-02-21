import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating

from utils import email_checker, store_feedback

st.set_page_config(
    page_title="Feedback",
    page_icon="💬",
    initial_sidebar_state="collapsed",
)

st.title("Feedback Page")
 
st.write("Rate your overall experience")
rating = st_star_rating('', size=30, maxValue=5, defaultValue=3, key="rating")

# Feedback Form Fields
name = st.text_input('Name (optional)', help='Your name (optional)')

# Arrange Batch and Department fields horizontally
col1, col2 = st.columns(2)
with col1:
    # Dropdown for Batch
    batches = ['16', '17', '18', '19', '20', '21', '22', '23']
    batch = st.selectbox('Batch (optional)', [''] + batches, help='Your batch (optional)')

with col2:
    # Dropdown for Department
    departments = ['AI', 'SE', 'CY', 'CS', 'DS']
    department = st.selectbox('Department (optional)', [''] + departments, help='Your department (optional)')

roll_num = st.text_input('Roll Number (optional)', help='Your roll number (optional)')

feedback_type = st.selectbox('Feedback Type', ['Bug Report', 'Feature Request', 'General Feedback'])
feedback_text = st.text_area('Please enter your feedback here:')    
contact_email = st.text_input('Email', help='Provide your email for further contact')

# Submit Button
submit_button = st.button('Submit Feedback')

if submit_button:
    if not feedback_text:
        st.warning('Please provide feedback before submitting.')
    if not email_checker(contact_email):
        st.error('Invalid Email Provided')
        
    if feedback_text and email_checker(contact_email):
        # Store Feedback
        store_feedback(feedback_type, rating, feedback_text, contact_email, 
                       name, batch, department, roll_num)
        
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
