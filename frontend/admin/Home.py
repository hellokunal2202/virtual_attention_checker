import streamlit as st
import streamlit as st
from datetime import datetime,timedelta
from pages.utils.demo_data import initialize_demo_data

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
    }
</style>
""", unsafe_allow_html=True)

# Admin profile data (customize with your admin details)
ADMIN_PROFILE = {
    "name": "Admin User",
    "role": "System Administrator",
    "email": "admin@meetingmanager.com",
    "last_login": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "photo_url": "myimg.png"  # Replace with actual photo
}

# Header with logout button
col1, col2 = st.columns([4, 1])
with col1:
    st.title("Admin Dashboard")
with col2:
    if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
        st.session_state.clear()
        st.rerun()

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
    tab1, tab2 = st.tabs(["📅 Recent Meetings", "👥 User Activity"])
    
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
                st.write(f"**Description:** {meeting['description']}")
    
    with tab2:
        # Mock user activity data
        activity_data = [
            {"user": "John Doe", "action": "Created meeting", "time": "2 hours ago"},
            {"user": "Jane Smith", "action": "Joined meeting", "time": "4 hours ago"},
            {"user": "Alex Wong", "action": "Updated profile", "time": "1 day ago"},
            {"user": "Sarah Connor", "action": "Downloaded report", "time": "1 day ago"},
            {"user": "Mike Jones", "action": "Scheduled meeting", "time": "2 days ago"},
        ]
        
        for activity in activity_data:
            st.markdown(f"""
            - **{activity['user']}** {activity['action']} ({activity['time']})
            """)

# System Management Section
st.subheader("⚙️ System Management")
with st.container(border=True):
    st.write("Administrative tools will appear here")
    cols = st.columns(3)
    with cols[0]:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    with cols[1]:
        if st.button("📊 Generate Reports", use_container_width=True):
            st.toast("Report generation started!", icon="📊")
    with cols[2]:
        if st.button("🛠️ System Settings", use_container_width=True):
            st.toast("Redirecting to settings...", icon="⚙️")