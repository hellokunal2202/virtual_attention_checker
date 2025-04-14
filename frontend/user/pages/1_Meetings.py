import streamlit as st
from datetime import datetime, timedelta

# Define page metadata at the top (used by the sidebar navigation)
PAGE_NAME = "Meetings"
PAGE_ICON = "📅"


def display_meeting_details(meeting, meeting_type):
    """Display meeting details with appropriate actions"""
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])

        with col1:
            # Ensure start_time is a datetime object before calling strftime
            if isinstance(meeting["start_time"], str):
                start_time_dt = datetime.strptime(
                    meeting["start_time"], "%Y-%m-%dT%H:%M:%S.%f"
                )
            else:
                start_time_dt = meeting["start_time"]

            st.markdown(
                f"""
                <div style="padding-top: 10px;">
                    Date & Time:<br>
                    {start_time_dt.strftime('%A, %b %d, %Y &nbsp;%I:%M %p')}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f"**Attendees:** \n{len(meeting['attendee_list'])} people")

            if meeting_type == "upcoming" and "meeting_url" in meeting:
                st.markdown(
                    f"""
                    <a href="{meeting['meeting_url']}" target="_blank">
                        <button style="background-color: #2196F3; color: white; padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer;">
                            ▶ Join Meeting
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )

        with col2:
            st.markdown(f"### {meeting['title']}")
            st.markdown(f"**Description:** \n{meeting['description']}")

            if meeting_type == "live":
                # Ensure meeting["start_time"] is a datetime object
                if isinstance(meeting["start_time"], str):
                    meeting_date = datetime.strptime(
                        meeting["start_time"], "%Y-%m-%dT%H:%M:%S.%f"
                    )
                else:
                    meeting_date = meeting["start_time"]

                duration = datetime.now() - meeting_date
                hours, remainder = divmod(duration.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                st.markdown(f"**Status** \n🟢 Live ({hours}h {minutes}m)")


def main():
    """Main function that renders the meetings page content"""
    # Loading Data
    MEETINGS = []
    if "meetings" in st.session_state:
        MEETINGS = st.session_state["meetings"]

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    # Categorize meetings
    now = datetime.now()

    past_meetings = [
        m
        for m in MEETINGS
        if datetime.strptime(m["start_time"], DATE_FORMAT) < now - timedelta(hours=1)
    ]

    upcoming_meetings = [
        m for m in MEETINGS if datetime.strptime(m["start_time"], DATE_FORMAT) > now
    ]

    live_meetings = [
        m
        for m in MEETINGS
        if now - timedelta(minutes=30)
        <= datetime.strptime(m["start_time"], DATE_FORMAT)
        <= now + timedelta(hours=1)
    ]

    # Page title
    st.title(f"{PAGE_ICON} {PAGE_NAME}")

    # Meeting tabs
    tab1, tab2, tab3 = st.tabs(["Past Meetings", "Upcoming Meetings", "Live Meetings"])

    with tab1:
        if past_meetings:
            selected = st.selectbox(
                "Select a past meeting:", [m["title"] for m in past_meetings]
            )
            meeting = next(m for m in past_meetings if m["title"] == selected)
            display_meeting_details(meeting, "past")
        else:
            st.info("No past meetings found.")

    with tab2:
        if upcoming_meetings:
            selected = st.selectbox(
                "Select an upcoming meeting:", [m["title"] for m in upcoming_meetings]
            )
            meeting = next(m for m in upcoming_meetings if m["title"] == selected)
            display_meeting_details(meeting, "upcoming")
        else:
            st.info("No upcoming meetings scheduled.")

    with tab3:
        if live_meetings:
            for meeting in live_meetings:
                # Ensure 'date' key exists and is a datetime object for live meetings
                if "start_time" not in meeting:
                    meeting["start_time"] = datetime.strptime(
                        meeting["start_time"], DATE_FORMAT
                    )
                elif isinstance(meeting["start_time"], str):
                    meeting["start_time"] = datetime.strptime(
                        meeting["start_time"], DATE_FORMAT
                    )
                display_meeting_details(meeting, "live")
        else:
            st.info("No live meetings currently happening.")
