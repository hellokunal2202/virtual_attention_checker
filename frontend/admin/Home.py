import streamlit as st
from datetime import datetime, timedelta, timezone
from .utils.get_data import get_data
from pathlib import Path
import sys
import pandas as pd
import importlib
import traceback

# Add admin directory to Python path
admin_path = str(Path(__file__).parent)
sys.path.append(admin_path)

# Import from pages.utils
from pages.views.ui_components import persistent_logout

# Define ist_timezone at the top level
ist_timezone = timezone(timedelta(hours=5, minutes=30))


def parse_meeting_time(time_str):
    if isinstance(time_str, str):
        formats_to_try = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"]
        for fmt in formats_to_try:
            try:
                return (
                    datetime.strptime(time_str, fmt)
                    .replace(tzinfo=timezone.utc)
                    .astimezone(ist_timezone)
                )
            except ValueError:
                continue
        return None
    elif isinstance(time_str, datetime):
        return time_str.astimezone(ist_timezone)
    return None


def initialize_session_data():
    """Initialize all session state data"""
    get_data()

    if "system_logs" not in st.session_state:
        st.session_state.system_logs = [
            {
                "timestamp": datetime.now(tz=ist_timezone) - timedelta(hours=2),
                "action": "System initialized",
                "details": "Admin dashboard loaded",
            },
            {
                "timestamp": datetime.now(tz=ist_timezone) - timedelta(hours=1),
                "action": "Meeting scheduled",
                "details": "Quarterly Review scheduled for 2023-11-15",
            },
            {
                "timestamp": datetime.now(tz=ist_timezone) - timedelta(minutes=45),
                "action": "Report generated",
                "details": "Monthly analytics report",
            },
        ]


def get_admin_pages():
    """Dynamically discover all admin pages without importing them immediately"""
    pages_dir = Path(__file__).parent / "pages"
    page_files = sorted([f for f in pages_dir.glob("[0-9]_*.py")])

    pages = []
    for page_file in page_files:
        pages.append(
            {
                "name": page_file.stem.replace("_", " ").title(),
                "path": str(page_file),
                "module_name": f"pages.{page_file.stem}",
                "icon": "📄",  # Default icon
            }
        )
    return pages


def load_page_module(module_name):
    """Safely import a page module"""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        st.error(f"Failed to load page module: {e}")
        return None


def render_header():
    ADMIN_PROFILE = {
        "name": "Admin User",
        "role": "System Administrator",
        "email": st.session_state["user"]["email"],
        "last_login": datetime.now(tz=ist_timezone).strftime("%Y-%m-%d %H:%M"),
        "photo_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkiIFjCOZ-mMeqxd2ryrneiHedE8G9S0AboA&s",
    }

    with st.container():
        st.markdown("<div class='header'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            try:
                st.image(ADMIN_PROFILE["photo_url"], width=190)
            except:
                st.warning("Profile image not found")
        with col2:
            st.subheader(ADMIN_PROFILE["name"])
            st.markdown(
                f"""
    - **Role:** {ADMIN_PROFILE["role"]}
    - **Email:** {ADMIN_PROFILE["email"]}
    - **Last Login:** {ADMIN_PROFILE["last_login"]}
    """
            )
        st.markdown("</div>", unsafe_allow_html=True)


def render_stats_cards():
    """Render the quick stats cards"""
    st.subheader("📊 System Overview")
    cols = st.columns(4)

    with cols[0]:
        with st.container(border=True):
            if "users_data" in st.session_state:
                st.metric("Total Users", len(st.session_state["users_data"]))

    with cols[1]:
        with st.container(border=True):
            upcoming_meetings = [
                m
                for m in st.session_state.get("meetings", [])
                if (meeting_time := parse_meeting_time(m.get("start_time")))
                and meeting_time > datetime.now(tz=ist_timezone)
            ]
            st.metric(
                "Upcoming Meetings",
                len(upcoming_meetings),
            )

    with cols[2]:
        with st.container(border=True):
            active_meetings = [
                m
                for m in st.session_state.get("meetings", [])
                if (meeting_time := parse_meeting_time(m.get("start_time")))
                and meeting_time - timedelta(hours=1)
                <= datetime.now(tz=ist_timezone)
                <= meeting_time + timedelta(hours=1)
            ]
            st.metric(
                "Active Meetings",
                len(active_meetings),
            )

    with cols[3]:
        with st.container(border=True):
            past_meetings = [
                m
                for m in st.session_state.get("meetings", [])
                if (meeting_time := parse_meeting_time(m.get("start_time")))
                and meeting_time < datetime.now(tz=ist_timezone) - timedelta(hours=1)
            ]
            st.metric(
                "Past Meetings",
                len(past_meetings),
            )


def render_recent_activity():
    """Render the recent activity section"""
    st.subheader("🔄 Recent Activity")
    with st.container(border=True):
        tab1, tab2 = st.tabs(["📅 Recent Meetings", "📝 System Logs"])

        with tab1:
            recent_meetings = sorted(
                st.session_state.get("meetings", []),
                key=lambda x: (
                    parse_meeting_time(x.get("start_time"))
                    if x.get("start_time")
                    else datetime.min.replace(tzinfo=ist_timezone)
                ),
                reverse=True,
            )[:5]

            for meeting in recent_meetings:
                start_time = parse_meeting_time(meeting.get("start_time"))
                if start_time:
                    with st.expander(
                        f"{meeting['title']} - {start_time.strftime('%b %d, %Y')}"
                    ):
                        st.write(
                            f"**When:** {start_time.strftime('%A, %B %d at %I:%M %p')}"
                        )
                        st.write(f"**Attendees:** {len(meeting['attendee_list'])}")

                        if st.button(
                            "📊 View Report",
                            key=f"report_{meeting.get('id')}_{meeting['title']}",
                        ):
                            report_data = {
                                "Meeting Title": [meeting["title"]],
                                "Date": [start_time.strftime("%Y-%m-%d %H:%M")],
                                "Attendees": [len(meeting["attendee_list"])],
                                "Duration": ["1 hour"],
                                "Status": [
                                    (
                                        "Completed"
                                        if start_time < datetime.now(tz=ist_timezone)
                                        else "Upcoming"
                                    )
                                ],
                            }
                            df = pd.DataFrame(report_data)

                            st.session_state.system_logs.insert(
                                0,
                                {
                                    "timestamp": datetime.now(tz=ist_timezone),
                                    "action": "Report generated",
                                    "details": f"Meeting: {meeting['title']}",
                                },
                            )

                            st.download_button(
                                label="⬇️ Download Report",
                                data=df.to_csv(index=False),
                                file_name=f"{meeting['title']}_report.csv",
                                mime="text/csv",
                                key=f"download_{meeting['title']}",
                            )

        with tab2:
            st.write("**Recent System Activities**")
            for log in sorted(
                st.session_state.system_logs, key=lambda x: x["timestamp"], reverse=True
            )[:10]:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.caption(log["timestamp"].strftime("%Y-%m-%d %H:%M"))
                    with col2:
                        st.markdown(f"**{log['action']}**")
                        st.caption(log["details"])


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
                st.session_state.system_logs.insert(
                    0,
                    {
                        "timestamp": datetime.now(tz=ist_timezone),
                        "action": "Bulk report generation",
                        "details": "Generated reports for all meetings",
                    },
                )
                st.toast("All reports generated!", icon="📊")
        with cols[2]:
            if st.button("🛠️ System Settings", use_container_width=True):
                st.toast("Redirecting to settings...", icon="⚙️")


def main():
    """Main function to run the admin dashboard"""
    # Initialize data
    get_data()

    # Set page config must be first
    st.set_page_config(
        page_title="Admin Dashboard",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for styling
    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

    # Initialize sidebar state
    if "sidebar_collapsed" not in st.session_state:
        st.session_state.sidebar_collapsed = False

    # Sidebar navigation
    with st.sidebar:
        cols = st.columns([4, 1])
        with cols[0]:
            st.subheader("Admin Navigation")
        with cols[1]:
            if st.button("≡", key="sidebar_toggle"):
                st.session_state.sidebar_collapsed = (
                    not st.session_state.sidebar_collapsed
                )

        if not st.session_state.sidebar_collapsed:
            # Get all available pages
            admin_pages = get_admin_pages()

            # Add navigation
            st.divider()
            if st.button(
                "🏠 Dashboard",
                use_container_width=True,
                type=(
                    "primary"
                    if not st.session_state.get("current_page")
                    else "secondary"
                ),
            ):
                st.session_state.current_page = None
                st.rerun()

            for page in admin_pages:
                if st.button(
                    f"{page['icon']} {page['name']}",
                    use_container_width=True,
                    key=f"nav_{page['path']}",
                    type=(
                        "primary"
                        if st.session_state.get("current_page") == page["path"]
                        else "secondary"
                    ),
                ):
                    st.session_state.current_page = page["path"]
                    st.rerun()

            st.divider()
            persistent_logout(
                position="sidebar", key_suffix="admin_dashboard"
            )  # Your existing logout button

    # Page rendering logic
    if st.session_state.get("current_page"):
        # Dynamically render the selected page
        selected_page = next(
            (
                p
                for p in get_admin_pages()
                if p["path"] == st.session_state.current_page
            ),
            None,
        )
        if selected_page:
            module = load_page_module(selected_page["module_name"])
            if module:
                try:
                    if hasattr(module, "main"):
                        module.main()
                    else:
                        st.error("Page module has no main() function")
                except Exception as e:
                    print(traceback.print_exception(e))
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
