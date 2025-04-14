import pytz
import streamlit as st
from datetime import datetime, timedelta
from frontend.admin.utils.delete_data import delete_meeting

# Define the Indian timezone
indian_timezone = pytz.timezone("Asia/Kolkata")


def get_employee_name(emp_id):
    """Get formatted employee name by ID"""
    emp = next(e for e in st.session_state["users_data"] if e["id"] == emp_id)
    return emp["username"]


def parse_datetime_utc(start_time_str):
    """Attempt to parse a string into a UTC datetime object."""
    if isinstance(start_time_str, datetime):
        return pytz.utc.localize(start_time_str)
    if isinstance(start_time_str, str):
        formats_to_try = [
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d-%m-%Y %H:%M",  # Added this format
            "%Y-%m-%d",  # Added this format to handle dates without time
            "%Y-%m-%dT%H:%M:%SZ",  # Added this format for strings ending with Z
            "%Y-%m-%dT%H:%M:%S",  # Added this format for YYYY-MM-DDTHH:MM:SS
        ]
        for fmt in formats_to_try:
            try:
                dt_obj = datetime.strptime(start_time_str, fmt)
                return pytz.utc.localize(dt_obj)
            except ValueError:
                continue
    return None


def display_meeting_details(meeting, meeting_type):
    """Display meeting details with appropriate actions"""
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])

        with col1:
            # Date and attendees info
            meeting_datetime_utc = parse_datetime_utc(meeting.get("start_time"))
            if meeting_datetime_utc:
                # Convert UTC datetime to Indian timezone
                meeting_datetime_indian = meeting_datetime_utc.astimezone(
                    indian_timezone
                )
                st.markdown(
                    f"**Date & Time** \n{meeting_datetime_indian.strftime('%A, %b %d, %Y  %I:%M %p %Z%z')}"
                )
            else:
                st.warning(
                    f"Could not parse meeting start time col1: {meeting.get('start_time')}"
                )
                return

            st.markdown(f"**Attendees** \n{len(meeting['attendee_list'])} people")

            # Action buttons
            if meeting_type == "past":
                if "report_url" in meeting:
                    st.markdown(
                        f"""
                        <a href="{meeting['report_url']}" target="_blank">
                            <button class="action-button" style="background-color: #4CAF50;">
                                📄 View Report
                            </button>
                        </a>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <button class="action-button" style="background-color: #cccccc; color: #666666;" disabled>
                            📄 No Report Available
                        </button>
                        """,
                        unsafe_allow_html=True,
                    )
            elif meeting_type == "upcoming" and "meeting_url" in meeting:
                st.markdown(
                    f"""
                    <a href="{meeting['meeting_url']}" target="_blank">
                        <button class="action-button" style="background-color: #2196F3;">
                            ▶ Start Meeting
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )

        with col2:
            col_title_delete = st.columns([3, 1])
            with col_title_delete[0]:
                # Meeting content
                st.markdown(f"### {meeting['title']}")
            with col_title_delete[1]:
                if st.button("🗑️ Delete", key=f"delete_button_{meeting['id']}"):
                    delete_resp = delete_meeting(meeting["id"])
                    if not delete_resp:
                        st.success("Meeting deleted successfully")

            st.markdown(f"**Description** \n{meeting['description']}")

            # Live meeting status
            if meeting_type == "live" and meeting_datetime_utc:
                now_utc = datetime.now(pytz.utc)
                duration = now_utc - meeting_datetime_utc
                hours, remainder = divmod(duration.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                st.markdown(f"**Status** \n🟢 Live ({hours}h {minutes}m)")

            # Attendees list
            st.markdown("**Attendees List**")
            for attendee_id in meeting["attendee_list"]:
                st.markdown(f"- {get_employee_name(attendee_id)}")


def get_meeting_datetime_utc(m):
    """Safely get and parse the meeting start time as a UTC datetime object."""
    start_time = m.get("start_time")
    return parse_datetime_utc(start_time)


def view_meetings_data():
    """Main meetings view function"""
    st.markdown(
        """
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
        .action-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Categorize meetings
    now_utc = datetime.now(pytz.utc)  # Define now_utc here
    past = []
    upcoming = []
    live = []

    if "meetings" not in st.session_state:
        st.warning("No meetings data available")
        return

    for meeting in st.session_state["meetings"]:
        meeting_datetime_utc = get_meeting_datetime_utc(meeting)

        if meeting_datetime_utc:
            # Calculate meeting window (30 mins before to 1 hour after) in UTC
            start_window = meeting_datetime_utc - timedelta(minutes=30)
            end_window = meeting_datetime_utc + timedelta(hours=1)

            # Categorize meetings based on current time in UTC
            if now_utc < start_window:
                upcoming.append(meeting)
            elif start_window <= now_utc <= end_window:
                live.append(meeting)
            else:
                past.append(meeting)
        else:
            st.warning(
                f"Could not parse start time for meeting for each: {meeting.get('title', 'Unknown')}"
            )

    # Sort meetings using datetime objects (aware of UTC)
    past.sort(key=get_meeting_datetime_utc, reverse=True)
    upcoming.sort(key=get_meeting_datetime_utc)

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Past Meetings", "Upcoming Meetings", "Live Meetings"])

    with tab1:
        if not past:
            st.info("No past meetings found")
        else:
            selected = st.selectbox(
                "Select meeting:",
                options=[
                    f"{m['title']} - {get_meeting_datetime_utc(m).astimezone(indian_timezone).strftime('%b %d %H:%M %Z%z') if isinstance(get_meeting_datetime_utc(m), datetime) else m.get('title', 'Unknown')}"
                    for m in past
                    if get_meeting_datetime_utc(m)
                ],
                key="past_select",
            )
            meeting = next(
                (
                    m
                    for m in past
                    if get_meeting_datetime_utc(m)
                    and f"{m['title']} - {get_meeting_datetime_utc(m).astimezone(indian_timezone).strftime('%b %d %H:%M %Z%z')}"
                    == selected
                ),
                None,
            )
            if meeting:
                display_meeting_details(meeting, "past")

    with tab2:
        if not upcoming:
            st.info("No upcoming meetings scheduled")
        else:
            selected = st.selectbox(
                "Select meeting:",
                options=[
                    f"{m['title']} - {get_meeting_datetime_utc(m).astimezone(indian_timezone).strftime('%b %d %H:%M %Z%z') if isinstance(get_meeting_datetime_utc(m), datetime) else m.get('title', 'Unknown')}"
                    for m in upcoming
                    if get_meeting_datetime_utc(m)
                ],
                key="upcoming_select",
            )
            meeting = next(
                (
                    m
                    for m in upcoming
                    if get_meeting_datetime_utc(m)
                    and f"{m['title']} - {get_meeting_datetime_utc(m).astimezone(indian_timezone).strftime('%b %d %H:%M %Z%z')}"
                    == selected
                ),
                None,
            )
            if meeting:
                display_meeting_details(meeting, "upcoming")

    with tab3:
        if not live:
            st.info("No live meetings currently happening")
        else:
            for meeting in live:
                display_meeting_details(meeting, "live")


def main():
    view_meetings_data()


if __name__ == "__main__":
    main()
