import streamlit as st
from datetime import datetime
from pages.utils.demo_data import DEMO_EMPLOYEES  # Import from utils

def create_meeting():
    """Create new meeting form"""
    st.header("Create New Meeting")
    
    with st.form("create_meeting_form"):
        # Meeting details
        title = st.text_input("Meeting Title*", placeholder="Enter meeting title")
        description = st.text_area("Meeting Description", placeholder="Enter meeting agenda and details")
        date = st.date_input("Meeting Date*", min_value=datetime.today())
        
        # Attendee selection
        employee_options = {
            emp['id']: f"{emp['name']} ({emp['department']})" 
            for emp in DEMO_EMPLOYEES  # Use imported DEMO_EMPLOYEES
        }
        attendees = st.multiselect(
            "Select Attendees*",
            options=list(employee_options.keys()),
            format_func=lambda x: employee_options[x]
        )
        
        # Form submission
        if st.form_submit_button("Create Meeting"):
            if not title:
                st.error("Please provide a meeting title!")
            elif not attendees:
                st.error("Please select at least one attendee!")
            else:
                # Initialize meetings_db if not exists
                if 'meetings_db' not in st.session_state:
                    st.session_state.meetings_db = []
                
                # Add new meeting
                st.session_state.meetings_db.append({
                    "title": title,
                    "description": description,
                    "date": datetime.combine(date, datetime.min.time()),  # Convert to datetime
                    "attendees": attendees
                })
                st.success("Meeting created successfully!")
                st.rerun()