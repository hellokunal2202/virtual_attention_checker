import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
import sys
import pandas as pd
import importlib

# Add admin directory to Python path
admin_path = str(Path(__file__).parent)
sys.path.append(admin_path)

# Import from pages.utils
from pages.utils.demo_data import initialize_demo_data
from pages.utils.ui_components import persistent_logout

# Initialize data
initialize_demo_data()

def initialize_session_data():
    """Initialize all session state data"""
    initialize_demo_data()
   
    if 'system_logs' not in st.session_state:
        st.session_state.system_logs = [
            {"timestamp": datetime.now() - timedelta(hours=2), "action": "System initialized", "details": "Admin dashboard loaded"},
            {"timestamp": datetime.now() - timedelta(hours=1), "action": "Meeting scheduled", "details": "Quarterly Review scheduled for 2023-11-15"},
            {"timestamp": datetime.now() - timedelta(minutes=45), "action": "Report generated", "details": "Monthly analytics report"},
        ]

def get_admin_pages():
    """Dynamically discover all admin pages without importing them immediately"""
    pages_dir = Path(__file__).parent / "pages"
    page_files = sorted([f for f in pages_dir.glob("[0-9]_*.py")])
    
    pages = []
    for page_file in page_files:
        pages.append({
            "name": page_file.stem.replace("_", " ").title(),
            "path": str(page_file),
            "module_name": f"pages.{page_file.stem}",
            "icon": "📄"  # Default icon
        })
    return pages

def load_page_module(module_name):
    """Safely import a page module"""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        st.error(f"Failed to load page module: {e}")
        return None

def render_header():
    current_dir = Path(__file__).parent
    ADMIN_PROFILE = {
        "name": "Admin User",
        "role": "System Administrator",
        "email": "admin@meetingmanager.com",
        "last_login": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "photo_url": str(current_dir / "myimg.png")
    }
   
    with st.container():
        st.markdown("<div class='header'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            try:
                st.image(ADMIN_PROFILE["photo_url"], width=150)
            except:
                st.warning("Profile image not found")
        with col2:
            st.subheader(ADMIN_PROFILE["name"])
            st.markdown(f"""
            - **Role:** {ADMIN_PROFILE["role"]}
            - **Email:** {ADMIN_PROFILE["email"]}
            - **Last Login:** {ADMIN_PROFILE["last_login"]}
            """)
        st.markdown("</div>", unsafe_allow_html=True)
       
def render_stats_cards():
    """Render the quick stats cards"""
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

def render_recent_activity():
    """Render the recent activity section"""
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
                   
                    if st.button("📊 View Report", key=f"report_{meeting['title']}"):
                        report_data = {
                            "Meeting Title": [meeting['title']],
                            "Date": [meeting['date'].strftime('%Y-%m-%d %H:%M')],
                            "Attendees": [len(meeting['attendees'])],
                            "Duration": ["1 hour"],
                            "Status": ["Completed" if meeting['date'] < datetime.now() else "Upcoming"]
                        }
                        df = pd.DataFrame(report_data)
                       
                        st.session_state.system_logs.insert(0, {
                            "timestamp": datetime.now(),
                            "action": "Report generated",
                            "details": f"Meeting: {meeting['title']}"
                        })
                       
                        st.download_button(
                            label="⬇️ Download Report",
                            data=df.to_csv(index=False),
                            file_name=f"{meeting['title']}_report.csv",
                            mime="text/csv",
                            key=f"download_{meeting['title']}"
                        )
       
        with tab2:
            st.write("**Recent System Activities**")
            for log in sorted(st.session_state.system_logs, key=lambda x: x['timestamp'], reverse=True)[:10]:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.caption(log['timestamp'].strftime('%Y-%m-%d %H:%M'))
                    with col2:
                        st.markdown(f"**{log['action']}**")
                        st.caption(log['details'])

def render_system_management():
    """Render the system management section"""
    st.subheader("⚙️ System Management")
    with st.container(border=True):
        st.write("Administrative tools will appear here")
        cols = st.columns(3)
        with cols[0]:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
        with cols[1]:
            if st.button("📊 Generate All Reports", use_container_width=True):
                st.session_state.system_logs.insert(0, {
                    "timestamp": datetime.now(),
                    "action": "Bulk report generation",
                    "details": "Generated reports for all meetings"
                })
                st.toast("All reports generated!", icon="📊")
        with cols[2]:
            if st.button("🛠️ System Settings", use_container_width=True):
                st.toast("Redirecting to settings...", icon="⚙️")

def main():
    """Main function to run the admin dashboard"""
    # Set page config must be first
    st.set_page_config(
        page_title="Admin Dashboard",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
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
        [data-testid="stSidebarNav"] {
            max-height: 100vh !important;
            overflow-y: auto !important;
        }
        .sidebar-collapse-control {
            position: absolute;
            right: 10px;
            top: 10px;
            z-index: 1;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize sidebar state
    if 'sidebar_collapsed' not in st.session_state:
        st.session_state.sidebar_collapsed = False
    
    # Sidebar navigation
    with st.sidebar:
        cols = st.columns([4, 1])
        with cols[0]:
            st.subheader("Admin Navigation")
        with cols[1]:
            if st.button("≡", key="sidebar_toggle"):
                st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
        
        if not st.session_state.sidebar_collapsed:
            # Get all available pages
            admin_pages = get_admin_pages()
            
            # Add navigation
            st.divider()
            if st.button("🏠 Dashboard", use_container_width=True, 
                        type="primary" if not st.session_state.get('current_page') else "secondary"):
                st.session_state.current_page = None
                st.rerun()
            
            for page in admin_pages:
                if st.button(
                    f"{page['icon']} {page['name']}", 
                    use_container_width=True,
                    key=f"nav_{page['path']}",
                    type="primary" if st.session_state.get('current_page') == page['path'] else "secondary"
                ):
                    st.session_state.current_page = page['path']
                    st.rerun()
            
            st.divider()
            persistent_logout(position="sidebar", key_suffix="admin_dashboard")  # Your existing logout button
    
    # Page rendering logic
    if st.session_state.get('current_page'):
        # Dynamically render the selected page
        selected_page = next((p for p in get_admin_pages() if p['path'] == st.session_state.current_page), None)
        if selected_page:
            module = load_page_module(selected_page['module_name'])
            if module:
                try:
                    if hasattr(module, 'main'):
                        module.main()
                    else:
                        st.error("Page module has no main() function")
                except Exception as e:
                    st.error(f"Error executing page: {e}")
        else:
            st.error("Page not found")
            st.session_state.current_page = None
            st.rerun()
    else:
        # Your existing dashboard content
        initialize_session_data()
        st.title("Admin Dashboard")
        render_header()
        render_stats_cards()
        render_recent_activity()
        render_system_management()

if __name__ == "__main__":
    main()