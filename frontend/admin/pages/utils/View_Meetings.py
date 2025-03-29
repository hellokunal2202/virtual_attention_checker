import streamlit as st
from datetime import datetime, timedelta, date, time
from pages.utils.demo_data import DEMO_EMPLOYEES

# Helper functions
def get_employee(emp_id):
    """Get employee by ID"""
    return next(e for e in st.session_state.demo_employees if e['id'] == emp_id)
 
def get_employee_name(emp_id):
    """Get formatted employee name by ID"""
    emp = get_employee(emp_id)
    return f"{emp['name']} ({emp['department']})"

def display_meeting_details(meeting, meeting_type):
    """Display meeting details with appropriate actions"""
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Date and attendees info
            meeting_datetime = meeting.get('datetime') or datetime.combine(meeting['date'], meeting.get('time', time(0, 0)))
            st.markdown(f"**Date & Time**  \n{meeting_datetime.strftime('%A, %b %d, %Y  %I:%M %p')}")
            st.markdown(f"**Attendees**  \n{len(meeting['attendees'])} people")
            
            # Action buttons
            if meeting_type == "past" and 'report_url' in meeting:
                st.markdown(
                    f"""
                    <a href="{meeting['report_url']}" target="_blank">
                        <button class="action-button" style="background-color: #4CAF50;">
                            📄 View Report
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
            elif meeting_type == "upcoming" and 'meeting_url' in meeting:
                st.markdown(
                    f"""
                    <a href="{meeting['meeting_url']}" target="_blank">
                        <button class="action-button" style="background-color: #2196F3;">
                            ▶ Start Meeting
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
                
        with col2:
            # Meeting content
            st.markdown(f"### {meeting['title']}")
            st.markdown(f"**Description**  \n{meeting['description']}")
            
            # Live meeting status
            if meeting_type == "live":
                meeting_datetime = meeting.get('datetime') or datetime.combine(meeting['date'], meeting.get('time', time(0, 0)))
                duration = datetime.now() - meeting_datetime
                hours, remainder = divmod(duration.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                st.markdown(f"**Status**  \n🟢 Live ({hours}h {minutes}m)")
            
            # Attendees list
            st.markdown("**Attendees List**")
            for attendee_id in meeting['attendees']:
                st.markdown(f"- {get_employee_name(attendee_id)}")

def view_meetings():
    """Main meetings view function"""
    st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            justify-content: center;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 1.25rem;
            background-color: var(--secondary-background-color);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            transition: all 0.2s;
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-color) !important;
            color: white !important;
            border-color: var(--primary-color) !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: var(--background-color);
        }
        .action-button {
            color: white;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            margin-top: 1rem;
            transition: all 0.2s;
        }
        .action-button:hover {
            opacity: 0.8;
        }
    </style>
    """, unsafe_allow_html=True)

    # Categorize meetings
    now = datetime.now()
    past = []
    upcoming = []
    live = []
    
    if 'meetings_db' not in st.session_state:
        st.warning("No meetings data available")
        return
    
    for meeting in st.session_state.meetings_db:
        # Get meeting datetime - handle both old and new formats
        if 'datetime' in meeting:
            meeting_datetime = meeting['datetime']
        else:
            meeting_date = meeting['date']
            meeting_time = meeting.get('time', time(0, 0))
            meeting_datetime = datetime.combine(meeting_date, meeting_time)
        
        start_window = meeting_datetime - timedelta(minutes=30)
        end_window = meeting_datetime + timedelta(hours=1)
        
        if now > end_window:
            past.append(meeting)
        elif start_window <= now <= end_window:
            live.append(meeting)
        else:
            upcoming.append(meeting)
    
    # Sort meetings using datetime objects
    def get_meeting_datetime(m):
        if 'datetime' in m:
            return m['datetime']
        return datetime.combine(m['date'], m.get('time', time(0, 0)))
    
    past.sort(key=get_meeting_datetime, reverse=True)
    upcoming.sort(key=get_meeting_datetime)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Past Meetings", "Upcoming Meetings", "Live Meetings"])
    
    with tab1:
        if not past:
            st.info("No past meetings found")
        else:
            selected = st.selectbox(
                "Select meeting:",
                options=[f"{m['title']} - {get_meeting_datetime(m).strftime('%b %d %H:%M')}" for m in past],
                key="past_select"
            )
            meeting = next(m for m in past if f"{m['title']} - {get_meeting_datetime(m).strftime('%b %d %H:%M')}" == selected)
            display_meeting_details(meeting, "past")
    
    with tab2:
        if not upcoming:
            st.info("No upcoming meetings scheduled")
        else:
            selected = st.selectbox(
                "Select meeting:",
                options=[f"{m['title']} - {get_meeting_datetime(m).strftime('%b %d %H:%M')}" for m in upcoming],
                key="upcoming_select"
            )
            meeting = next(m for m in upcoming if f"{m['title']} - {get_meeting_datetime(m).strftime('%b %d %H:%M')}" == selected)
            display_meeting_details(meeting, "upcoming")
    
    with tab3:
        if not live:
            st.info("No live meetings currently happening")
        else:
            for meeting in live:
                display_meeting_details(meeting, "live")

def main():
    """Main function"""
    if 'demo_employees' not in st.session_state:
        st.session_state.demo_employees = DEMO_EMPLOYEES
    view_meetings()

if __name__ == "__main__":
    main()