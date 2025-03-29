import streamlit as st
from datetime import datetime, timedelta
from pages.utils.demo_data import initialize_demo_data
from pages.utils.ui_components import persistent_logout
import pandas as pd

# Initialize session state data
initialize_demo_data()

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard",
    layout="wide",
    page_icon="🛡️"
)

# Custom CSS for styling
st.markdown("""
<style>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .admin-card {
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .stats-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .logout-btn {
        background-color: #ff4b4b !important;
        color: white !important;
        margin-top: 2rem !important;
    }
    .report-btn {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize logs if not exists
if 'system_logs' not in st.session_state:
    st.session_state.system_logs = [
        {"timestamp": datetime.now() - timedelta(hours=2), "action": "System initialized", "details": "Admin dashboard loaded"},
        {"timestamp": datetime.now() - timedelta(hours=1), "action": "Meeting scheduled", "details": "Quarterly Review scheduled for 2023-11-15"},
        {"timestamp": datetime.now() - timedelta(minutes=45), "action": "Report generated", "details": "Monthly analytics report"},
    ]

# Admin profile data
ADMIN_PROFILE = {
    "name": "Admin User",
    "role": "System Administrator",
    "email": "admin@meetingmanager.com",
    "last_login": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "photo_url": "myimg.png"  # Replace with actual photo
}

persistent_logout()
# Header without logout button
st.title("Admin Dashboard")

# Admin Profile Section
with st.container():
    st.markdown("<div class='header'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(ADMIN_PROFILE["photo_url"], width=150)
    
    with col2:
        st.subheader(ADMIN_PROFILE["name"])
        st.markdown(f"""
        - **Role:** {ADMIN_PROFILE["role"]}
        - **Email:** {ADMIN_PROFILE["email"]}
        - **Last Login:** {ADMIN_PROFILE["last_login"]}
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Quick Stats Cards
st.subheader("📊 System Overview")
cols = st.columns(4)
with cols[0]:
    with st.container(border=True):
        st.metric("Total Users", len(st.session_state.demo_employees))
with cols[1]:
    with st.container(border=True):
        st.metric("Upcoming Meetings", 
                 len([m for m in st.session_state.meetings_db 
                     if m['date'] > datetime.now()]))
with cols[2]:
    with st.container(border=True):
        st.metric("Active Meetings", 
                 len([m for m in st.session_state.meetings_db 
                     if (m['date'] - timedelta(hours=1)) <= datetime.now() <= (m['date'] + timedelta(hours=1))]))
with cols[3]:
    with st.container(border=True):
        st.metric("Past Meetings", 
                 len([m for m in st.session_state.meetings_db 
                     if m['date'] < datetime.now() - timedelta(hours=1)]))

# Recent Activity Section
st.subheader("🔄 Recent Activity")
with st.container(border=True):
    tab1, tab2 = st.tabs(["📅 Recent Meetings", "📝 System Logs"])
    
    with tab1:
        recent_meetings = sorted(
            st.session_state.meetings_db, 
            key=lambda x: x['date'], 
            reverse=True
        )[:5]
        
        for meeting in recent_meetings:
            with st.expander(f"{meeting['title']} - {meeting['date'].strftime('%b %d, %Y')}"):
                st.write(f"**When:** {meeting['date'].strftime('%A, %B %d at %I:%M %p')}")
                st.write(f"**Attendees:** {len(meeting['attendees'])}")
                
                # Generate report button - only visible when expanded
                if st.button("📊 View Report", key=f"report_{meeting['title']}"):
                    # Create a sample report
                    report_data = {
                        "Meeting Title": [meeting['title']],
                        "Date": [meeting['date'].strftime('%Y-%m-%d %H:%M')],
                        "Attendees": [len(meeting['attendees'])],
                        "Duration": ["1 hour"],
                        "Status": ["Completed" if meeting['date'] < datetime.now() else "Upcoming"]
                    }
                    df = pd.DataFrame(report_data)
                    
                    # Add to logs
                    st.session_state.system_logs.insert(0, {
                        "timestamp": datetime.now(),
                        "action": "Report generated",
                        "details": f"Meeting: {meeting['title']}"
                    })
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Report",
                        data=df.to_csv(index=False),
                        file_name=f"{meeting['title']}_report.csv",
                        mime="text/csv",
                        key=f"download_{meeting['title']}"
                    )
    
    with tab2:
        # System logs display
        st.write("**Recent System Activities**")
        for log in sorted(st.session_state.system_logs, key=lambda x: x['timestamp'], reverse=True)[:10]:
            with st.container(border=True):
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.caption(log['timestamp'].strftime('%Y-%m-%d %H:%M'))
                with col2:
                    st.markdown(f"**{log['action']}**")
                    st.caption(log['details'])

# System Management Section
st.subheader("⚙️ System Management")
with st.container(border=True):
    st.write("Administrative tools will appear here")
    cols = st.columns(3)
    with cols[0]:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    with cols[1]:
        if st.button("📊 Generate All Reports", use_container_width=True):
            # Add to logs
            st.session_state.system_logs.insert(0, {
                "timestamp": datetime.now(),
                "action": "Bulk report generation",
                "details": "Generated reports for all meetings"
            })
            st.toast("All reports generated!", icon="📊")
    with cols[2]:
        if st.button("🛠️ System Settings", use_container_width=True):
            st.toast("Redirecting to settings...", icon="⚙️")

def add_log_entry(action, details):
    """Helper function to add log entries"""
    st.session_state.system_logs.insert(0, {
        "timestamp": datetime.now(),
        "action": action,
        "details": details
    })