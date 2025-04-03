import streamlit as st
from datetime import datetime, time, date, timedelta
from .demo_data import DEMO_EMPLOYEES

def edit_meetings():
    """Edit existing meetings with draft and submit functionality"""
    st.subheader("Edit Meetings")
   
    if not st.session_state.get('meetings_db', []):
        st.info("No meetings available to edit")
        return
   
    # Meeting selector
    meeting_options = {
        idx: f"{m['title']} ({m.get('datetime', m['date']).strftime('%Y-%m-%d %H:%M')})"
        for idx, m in enumerate(st.session_state.meetings_db)
    }
    selected_idx = st.selectbox(
        "Select meeting to edit",
        options=list(meeting_options.keys()),
        format_func=lambda x: meeting_options[x]
    )
   
    if selected_idx is not None:
        meeting = st.session_state.meetings_db[selected_idx]
        
        # Initialize draft for this meeting if not exists
        if f'edit_draft_{selected_idx}' not in st.session_state:
            meeting_time = meeting.get('time', time(10, 0))
            if 'datetime' in meeting:
                meeting_date = meeting['datetime'].date()
                meeting_time = meeting['datetime'].time()
            else:
                meeting_date = meeting['date']
            
            st.session_state[f'edit_draft_{selected_idx}'] = {
                "title": meeting['title'],
                "description": meeting['description'],
                "date": meeting_date,
                "time": meeting_time,
                "attendees": meeting['attendees'],
                "link": meeting.get('meeting_url', '')  # Initialize with current meeting link
            }
       
        with st.form(key=f"edit_form_{selected_idx}"):
            # Editable fields - from draft
            draft = st.session_state[f'edit_draft_{selected_idx}']
            
            new_title = st.text_input("Meeting Title*", value=draft['title'])
            new_desc = st.text_area("Description", value=draft['description'])
            
            # Date and Time selection
            col1, col2 = st.columns(2)
            with col1:
                new_date = st.date_input("Date*", value=draft['date'])
            with col2:
                new_time = st.time_input("Time*", value=draft['time'], step=timedelta(minutes=30))
           
            # Attendee selection
            employee_options = {
                emp['id']: f"{emp['name']} ({emp['department']})"
                for emp in st.session_state.demo_employees
            }
            new_attendees = st.multiselect(
                "Attendees*",
                options=list(employee_options.keys()),
                format_func=lambda x: employee_options[x],
                default=draft['attendees']
            )
            
            # Meeting Link field - Shows current link by default
            #current_link = meeting.get('meeting_url', 'No link currently set')
            # st.markdown(f"**Current Meeting Link:** `{current_link}`")
            
            new_link = st.text_input(
                "Meeting Link*",
                value=draft.get('link', ''),
                placeholder='Enter Teams Meeting link',
                help="Paste the new meeting link here to update"
            )
           
            # Action buttons
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
           
            with col1:
                draft_saved = st.form_submit_button("💾 Save Draft")
           
            with col2:
                changes_submitted = st.form_submit_button("✅ Submit Changes")
           
            with col3:
                meeting_deleted = st.form_submit_button("🗑️ Delete")
           
            with col4:
                changes_cancelled = st.form_submit_button("❌ Cancel", type="secondary")
           
            if draft_saved:
                # Update draft
                st.session_state[f'edit_draft_{selected_idx}'] = {
                    "title": new_title,
                    "description": new_desc,
                    "date": new_date,
                    "time": new_time,
                    "attendees": new_attendees,
                    "link": new_link
                }
                st.session_state.show_draft_saved = True
                st.rerun()
           
            if changes_submitted:
                if not new_title:
                    st.error("Please provide a meeting title!")
                elif not new_attendees:
                    st.error("Please select at least one attendee!")
                else:
                    # Update the meeting in database
                    meeting_datetime = datetime.combine(new_date, new_time)
                    st.session_state.meetings_db[selected_idx] = {
                        "title": new_title,
                        "description": new_desc,
                        "datetime": meeting_datetime,
                        "date": meeting_datetime.date(),
                        "time": meeting_datetime.time(),
                        "attendees": new_attendees,
                        "link": new_link
                    }
                    # Clear the draft
                    if f'edit_draft_{selected_idx}' in st.session_state:
                        del st.session_state[f'edit_draft_{selected_idx}']
                    
                    st.session_state.show_update_success = True
                    st.rerun()

            if meeting_deleted:
                del st.session_state.meetings_db[selected_idx]
                # Clear any draft if exists
                if f'edit_draft_{selected_idx}' in st.session_state:
                    del st.session_state[f'edit_draft_{selected_idx}']
                
                st.session_state.show_delete_success = True
                st.rerun()
                
            if changes_cancelled:
                # Clear the draft and reset form
                if f'edit_draft_{selected_idx}' in st.session_state:
                    del st.session_state[f'edit_draft_{selected_idx}']
                st.session_state.show_cancel_success = True
                st.rerun()

        # Display messages below the form
        if st.session_state.get('show_draft_saved'):
            st.success("Draft saved successfully!")
            del st.session_state['show_draft_saved']
        
        if st.session_state.get('show_update_success'):
            st.success("Meeting updated successfully!")
            del st.session_state['show_update_success']
        
        if st.session_state.get('show_delete_success'):
            st.success("Meeting deleted successfully!")
            del st.session_state['show_delete_success']
        
        if st.session_state.get('show_cancel_success'):
            st.success("Changes canceled successfully!")
            del st.session_state['show_cancel_success']

def main():
    """Main function"""
    if 'demo_employees' not in st.session_state:
        st.session_state.demo_employees = DEMO_EMPLOYEES
    edit_meetings()

if __name__ == "__main__":
    main()