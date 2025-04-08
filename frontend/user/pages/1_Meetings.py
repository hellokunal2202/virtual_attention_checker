import streamlit as st
from datetime import datetime, timedelta

# Define page metadata at the top (used by the sidebar navigation)
PAGE_NAME = "Meetings"
PAGE_ICON = "📅"

def main():
    """Main function that renders the meetings page content"""
    # Sample static data
    MEETINGS = [
        {
            "title": "Project Kickoff",
            "date": datetime.now() - timedelta(days=2),
            "description": "Discussion on project goals and deliverables.",
            "attendees": ["Alice", "Bob", "Charlie"],
            "report_url": "https://example.com/report1",
        },
        {
            "title": "Sprint Planning",
            "date": datetime.now() + timedelta(days=3),
            "description": "Planning the tasks for the next sprint.",
            "attendees": ["Alice", "David", "Eve"],
            "meeting_url": "https://example.com/meeting2",
        },
        {
            "title": "Team Standup",
            "date": datetime.now(),
            "description": "Daily team standup to discuss progress.",
            "attendees": ["Bob", "Charlie", "Eve"],
        },
    ]

    def display_meeting_details(meeting, meeting_type):
        """Display meeting details with appropriate actions"""
        with st.container(border=True):
            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown(f"**Date & Time**  \n{meeting['date'].strftime('%A, %b %d, %Y  %I:%M %p')}")
                st.markdown(f"**Attendees**  \n{len(meeting['attendees'])} people")

                if meeting_type == "upcoming" and 'meeting_url' in meeting:
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
                st.markdown(f"**Description**  \n{meeting['description']}")

                if meeting_type == "live":
                    duration = datetime.now() - meeting['date']
                    hours, remainder = divmod(duration.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)
                    st.markdown(f"**Status**  \n🟢 Live ({hours}h {minutes}m)")

                st.markdown("**Attendees List**")
                for attendee in meeting['attendees']:
                    st.markdown(f"- {attendee}")

    # Categorize meetings
    now = datetime.now()
    past_meetings = [m for m in MEETINGS if m['date'] < now - timedelta(hours=1)]
    upcoming_meetings = [m for m in MEETINGS if m['date'] > now]
    live_meetings = [m for m in MEETINGS if now - timedelta(minutes=30) <= m['date'] <= now + timedelta(hours=1)]

    # Page title
    st.title(f"{PAGE_ICON} {PAGE_NAME}")

    # Meeting tabs
    tab1, tab2, tab3 = st.tabs(["Past Meetings", "Upcoming Meetings", "Live Meetings"])

    with tab1:
        if past_meetings:
            selected = st.selectbox("Select a past meeting:", [m['title'] for m in past_meetings])
            meeting = next(m for m in past_meetings if m['title'] == selected)
            display_meeting_details(meeting, "past")
        else:
            st.info("No past meetings found.")

    with tab2:
        if upcoming_meetings:
            selected = st.selectbox("Select an upcoming meeting:", [m['title'] for m in upcoming_meetings])
            meeting = next(m for m in upcoming_meetings if m['title'] == selected)
            display_meeting_details(meeting, "upcoming")
        else:
            st.info("No upcoming meetings scheduled.")

    with tab3:
        if live_meetings:
            for meeting in live_meetings:
                display_meeting_details(meeting, "live")
        else:
            st.info("No live meetings currently happening.")

# This ensures the page can be imported without running main()
if __name__ == "__main__":
    main()