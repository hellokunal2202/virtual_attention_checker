import streamlit as st
from datetime import datetime
from .demo_data import DEMO_EMPLOYEES

def edit_meetings():
    """Edit existing meetings"""
    st.subheader("Edit Meetings")
    
    if 'meetings_db' not in st.session_state or not st.session_state.meetings_db:
        st.info("No meetings available to edit")
        return
    
    # Meeting selector
    meeting_options = {
        idx: f"{m['title']} ({m['date'].strftime('%Y-%m-%d')})" 
        for idx, m in enumerate(st.session_state.meetings_db)
    }
    selected_idx = st.selectbox(
        "Select meeting to edit",
        options=list(meeting_options.keys()),
        format_func=lambda x: meeting_options[x],
        key="meeting_selector"
    )
    
    if selected_idx is not None:
        meeting = st.session_state.meetings_db[selected_idx]
        
        with st.form(f"edit_form_{selected_idx}"):
            st.markdown("### Edit Meeting Details")
            
            col1, col2 = st.columns(2)
            with col1:
                new_title = st.text_input(
                    "Meeting Title*", 
                    value=meeting['title'],
                    help="Required field"
                )
                
                # Fix: Ensure default date is within valid range
                min_date = datetime.today()
                meeting_date = meeting['date']
                default_date = meeting_date if meeting_date >= min_date else min_date
                
                new_date = st.date_input(
                    "Date*",
                    value=default_date,
                    min_value=min_date,
                    help="Required field"
                )
            
            with col2:
                new_desc = st.text_area(
                    "Description", 
                    value=meeting['description'],
                    height=100
                )
                
                new_attendees = st.multiselect(
                    "Attendees*",
                    options=[emp['id'] for emp in DEMO_EMPLOYEES],
                    format_func=lambda x: f"{next(e['name'] for e in DEMO_EMPLOYEES if e['id'] == x)} ({next(e['department'] for e in DEMO_EMPLOYEES if e['id'] == x)})",
                    default=meeting['attendees'],
                    help="Select at least one attendee"
                )
            
            # Action buttons
            cols = st.columns([1,1,2])
            with cols[0]:
                save_btn = st.form_submit_button(
                    "💾 Save",
                    help="Save changes to this meeting"
                )
            with cols[1]:
                del_btn = st.form_submit_button(
                    "🗑️ Delete",
                    help="Permanently delete this meeting"
                )
            with cols[2]:
                if st.form_submit_button("❌ Cancel"):
                    st.rerun()
            
            if save_btn:
                if not new_title:
                    st.error("Please provide a meeting title!")
                elif not new_attendees:
                    st.error("Please select at least one attendee!")
                else:
                    st.session_state.meetings_db[selected_idx] = {
                        "title": new_title,
                        "description": new_desc,
                        "date": datetime.combine(new_date, meeting['date'].time()),
                        "attendees": new_attendees
                    }
                    st.success("Meeting updated successfully!")
                    st.rerun()
            
            if del_btn:
                del st.session_state.meetings_db[selected_idx]
                st.success("Meeting deleted successfully!")
                st.rerun()