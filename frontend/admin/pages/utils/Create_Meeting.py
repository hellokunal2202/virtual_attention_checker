import streamlit as st
from datetime import datetime, time, date, timedelta
from pages.utils.demo_data import DEMO_EMPLOYEES
from pages.utils.View_Meetings import get_employee


# Initialize session state variables
if 'draft_meeting' not in st.session_state:
    st.session_state.draft_meeting = {
        'title': '',
        'description': '',
        'date': datetime.today().date(),
        'time': time(10, 0),
        'attendees': []
    }

if 'demo_employees' not in st.session_state:
    st.session_state.demo_employees = DEMO_EMPLOYEES

# Message states
if 'message' not in st.session_state:
    st.session_state.message = {'text': '', 'type': None}

def create_meeting():
    """Create new meeting form with draft and submit functionality"""
    st.header("Create New Meeting")
    
    # If we have a submitted meeting to show
    if 'submitted_meeting' in st.session_state:
        meeting = st.session_state.submitted_meeting
        st.success("Meeting created successfully!")
        
        # Display meeting details
        st.subheader("Meeting Details")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Title", meeting['title'])
            st.metric("Date", meeting['datetime'].strftime('%Y-%m-%d %H:%M'))
            st.metric("Attendees", len(meeting['attendees']))
        
        with col2:
            st.write(f"**Description:** {meeting['description']}")
            st.write("**Attendees:**")
            for attendee_id in meeting['attendees']:
                emp = get_employee(attendee_id)
                st.write(f"- {emp['name']} ({emp['department']})")
        
        # Add button to create another meeting
        if st.button("Create Another Meeting"):
            del st.session_state.submitted_meeting
            st.session_state.draft_meeting = {
                'title': '',
                'description': '',
                'date': datetime.today().date(),
                'time': time(10, 0),
                'attendees': []
            }
            st.rerun()
        return
    
    # Meeting creation form
    with st.form(key="create_meeting_form"):
        # Meeting details - initialized from draft
        title = st.text_input(
            "Meeting Title*",
            value=st.session_state.draft_meeting['title'],
            placeholder="Enter meeting title"
        )
        description = st.text_area(
            "Meeting Description",
            value=st.session_state.draft_meeting['description'],
            placeholder="Enter meeting agenda and details"
        )
        
        # Date and time selection
        col1, col2 = st.columns(2)
        with col1:
            date_val = st.date_input(
                "Meeting Date*",
                value=st.session_state.draft_meeting['date'],
                min_value=datetime.today().date()
            )
        with col2:
            time_val = st.time_input(
                "Meeting Time*",
                value=st.session_state.draft_meeting.get('time', time(10, 0)),
                step=timedelta(minutes=30)
            )
        
        # Attendee selection
        employee_options = {
            emp['id']: f"{emp['name']} ({emp['department']})"
            for emp in st.session_state.demo_employees
        }
        attendees = st.multiselect(
            "Select Attendees*",
            options=list(employee_options.keys()),
            format_func=lambda x: employee_options[x],
            default=st.session_state.draft_meeting['attendees']
        )
        
        # Form submission buttons - arranged in columns
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            draft_saved = st.form_submit_button("💾 Save Draft")
        
        with col2:
            submitted = st.form_submit_button("✅ Submit Meeting")
        
        with col3:
            cancelled = st.form_submit_button("❌ Cancel", type="secondary")
        
        # Process form submissions
        if draft_saved:
            # Update draft in session state
            st.session_state.draft_meeting = {
                "title": title,
                "description": description,
                "date": date_val,
                "time": time_val,
                "attendees": attendees
            }
            st.session_state.message = {
                'text': "Draft saved successfully!",
                'type': 'success'
            }
            st.rerun()
        
        if submitted:
            if not title:
                st.error("Please provide a meeting title!")
            elif not attendees:
                st.error("Please select at least one attendee!")
            else:
                # Combine date and time into a datetime object
                meeting_datetime = datetime.combine(date_val, time_val)
                
                # Create new meeting and add to database
                new_meeting = {
                    "title": title,
                    "description": description,
                    "datetime": meeting_datetime,
                    "date": meeting_datetime.date(),
                    "time": meeting_datetime.time(),
                    "attendees": attendees
                }
                
                # Initialize meetings_db if not exists
                if 'meetings_db' not in st.session_state:
                    st.session_state.meetings_db = []
                
                st.session_state.meetings_db.append(new_meeting)
                
                # Store in session state to show confirmation
                st.session_state.submitted_meeting = new_meeting
                
                # Clear the draft
                st.session_state.draft_meeting = {
                    'title': '',
                    'description': '',
                    'date': datetime.today().date(),
                    'time': time(10, 0),
                    'attendees': []
                }
                st.session_state.message = {'text': '', 'type': None}
                st.rerun()

        if cancelled:
            # Clear the draft
            st.session_state.draft_meeting = {
                'title': '',
                'description': '',
                'date': datetime.today().date(),
                'time': time(10, 0),
                'attendees': []
            }
            st.session_state.message = {
                'text': "Meeting creation canceled successfully!",
                'type': 'success'
            }
            st.rerun()

    # Display message below the form if exists
    if st.session_state.message['text']:
        if st.session_state.message['type'] == 'success':
            st.success(st.session_state.message['text'])
        elif st.session_state.message['type'] == 'error':
            st.error(st.session_state.message['text'])
        
        # Clear message after displaying
        st.session_state.message = {'text': '', 'type': None}

def main():
    """Main function"""
    create_meeting()

if __name__ == "__main__":
    main()