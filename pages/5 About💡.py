import streamlit as st

from utils import email_checker, fetch_current_rating, get_base_url, subscribe_to_updates

st.set_page_config(
    page_title="About",
    page_icon="💡",
    initial_sidebar_state="collapsed",
)

st.title("About Page")

# show current rating
base_url = get_base_url()
current_rating = fetch_current_rating(base_url)
st.write("Rating: ", current_rating)

st.markdown("""
The Timetable Scheduler App was created to address the unique needs of the students of computing department of FAST National University, Islamabad Campus. The Timetable provided by the department is combined for all batches, departments and sections. Making it difficult for students to navigate the file to make their schedules. The purpose of this app is to simplify the process of making personalised timetable accurately and easily.
""")

st.subheader('Upcoming Features')

st.markdown("""
In this section, we'll highlight some of the exciting features we're working on for future updates. 
Check back often to see what's coming! You can request for features and give suggestions in the feedback section.
""")

# List of upcoming features
features = [
    "Examination Seating Plan Manager",
    "Clash Detection"
]

# Display upcoming features
for feature in features:
    st.write(f"- {feature}")
    
st.divider()
st.subheader('Newsletter')

st.markdown("""
**Stay Updated!**

Enter your email below to receive notifications about the latest updates and feature releases.
""")

email = st.text_input('Email')
if st.button('Subscribe'):
    # '''
    #     I need to integrate a Gmail API system that verifies the entered email
    # '''
    if email_checker(email):
        subscribe_to_updates(base_url, email)
    else:
        st.error('Invalid Email provided')


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
