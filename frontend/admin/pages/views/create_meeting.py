import traceback
import streamlit as st
from datetime import datetime, time, timedelta
from pages.views.demo_data import DEMO_EMPLOYEES
from pages.views.view_meetings import get_employee_name
from frontend.admin.utils.add_data import add_meeting_data


def initialize_session_state():
    """Initialize all required session state variables"""
    if "draft_meeting" not in st.session_state:
        st.session_state.draft_meeting = {
            "title": "",
            "description": "",
            "start_time": datetime.today().date(),
            "time": time(10, 0),
            "attendee_list": [],
            "link": "",
        }

    if "users_data" not in st.session_state:
        st.session_state["users_data"] = DEMO_EMPLOYEES

    if "message" not in st.session_state:
        st.session_state.message = {"text": "", "type": None}


def create_meeting():
    """Create new meeting form with draft and submit functionality"""
    initialize_session_state()  # Ensure session state is initialized

    st.header("Create New Meeting")

    # If we have a submitted meeting to show
    if "submitted_meeting" in st.session_state:
        meeting = st.session_state.submitted_meeting
        st.success("Meeting created successfully!")

        # Display meeting details
        st.subheader("Meeting Details")
        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric("Title", meeting["title"])
            # Ensure start_time is a datetime object before formatting
            if isinstance(meeting["start_time"], str):
                try:
                    meeting_datetime = datetime.fromisoformat(
                        meeting["start_time"].replace("Z", "+00:00")
                    )
                    st.metric("Date", meeting_datetime.strftime("%Y-%m-%d %H:%M"))
                except ValueError:
                    st.error(
                        f"Error: Could not parse date string: {meeting['start_time']}"
                    )
                    st.metric("Date", "Invalid Date")
            else:
                st.metric("Date", meeting["start_time"].strftime("%Y-%m-%d %H:%M"))
            st.metric("Attendees", len(meeting["attendee_list"]))

        with col2:
            st.write(f"**Description:** {meeting['description']}")
            st.write("**Attendees:**")
            for attendee_id in meeting["attendee_list"]:
                emp = get_employee_name(attendee_id)
                st.write(f"- {emp}")

            # Display meeting link if available
            st.write("**Meeting Link:**")
            if meeting.get("link"):
                st.markdown(f"[{meeting['link']}]({meeting['link']})")
            else:
                st.write("No meeting link provided")

        # Add button to create another meeting
        if st.button("Create Another Meeting"):
            del st.session_state.submitted_meeting
            st.session_state.draft_meeting = {
                "title": "",
                "description": "",
                "start_time": datetime.today().date(),
                "time": time(10, 0),
                "attendee_list": [],
                "link": "",
            }
            st.rerun()
        return

    # Meeting creation form
    with st.form(key="create_meeting_form"):
        # Meeting details - initialized from draft
        title = st.text_input(
            "Meeting Title*",
            value=st.session_state.draft_meeting["title"],
            placeholder="Enter meeting title",
        )
        description = st.text_area(
            "Meeting Description",
            value=st.session_state.draft_meeting["description"],
            placeholder="Enter meeting agenda and details",
        )

        # Date and time selection
        col1, col2 = st.columns(2)
        with col1:
            date_val = st.date_input(
                "Meeting Date*",
                value=st.session_state.draft_meeting["start_time"],
                min_value=datetime.today().date(),
            )
        with col2:
            time_val = st.time_input(
                "Meeting Time*",
                value=st.session_state.draft_meeting.get("time", time(10, 0)),
                step=timedelta(minutes=30),
            )

        # Attendee selection
        employee_options = {
            emp["id"]: f"{emp['username']}" for emp in st.session_state["users_data"]
        }
        attendees = st.multiselect(
            "Select Attendees*",
            options=list(employee_options.keys()),
            format_func=lambda x: employee_options[x],
            default=st.session_state.draft_meeting["attendee_list"],
        )

        # Meeting Link field
        # st.markdown("---")
        meeting_link = st.text_input(
            "Meeting Link",
            value=st.session_state.draft_meeting.get("link", ""),
            placeholder="Teams Meeting link",
            help="Optional link for virtual meetings or physical location",
        )

        # Form submission buttons - MOVED INSIDE THE FORM
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            draft_saved = st.form_submit_button("💾 Save Draft")
        with col2:
            submitted = st.form_submit_button("✅ Submit Meeting")
        with col3:
            cancelled = st.form_submit_button("❌ Cancel", type="secondary")

        # Process form submissions
        if draft_saved:
            st.session_state.draft_meeting = {
                "title": title,
                "description": description,
                "start_time": date_val,
                "time": time_val,
                "attendee_list": attendees,
                "link": meeting_link,
            }
            st.session_state.message = {
                "text": "Draft saved successfully!",
                "type": "success",
            }
            st.rerun()

        if submitted:
            if not title:
                st.error("Please provide a meeting title!")
            elif not attendees:
                st.error("Please select at least one attendee!")
            elif not meeting_link:
                st.error("Please provide a meeting link!")
            else:
                meeting_datetime = datetime.combine(date_val, time_val)
                # new_meeting = {
                #     "title": title,
                #     "description": description,
                #     "start_time": meeting_datetime.date(),
                #     "time": meeting_datetime.time(),
                #     "attendee_list": attendees,
                #     "link": meeting_link,
                # }

                create_meeting_resp = add_meeting_data(
                    {
                        "admin_id": st.session_state["user"]["id"],
                        "title": title,
                        "start_time": meeting_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"),
                        "description": description,
                        "meeting_link": meeting_link,
                        "attendees": attendees,
                    }
                )
                if not create_meeting_resp:
                    st.error("Some error occurred while creating meeting!")
                    return

                st.session_state.submitted_meeting = {
                    "title": create_meeting_resp["title"],
                    "description": create_meeting_resp["description"],
                    "start_timetime": create_meeting_resp["start_time"],
                    "start_time": datetime.fromisoformat(
                        create_meeting_resp["start_time"]
                    ).date(),
                    "time": datetime.fromisoformat(
                        create_meeting_resp["start_time"]
                    ).time(),
                    "attendee_list": create_meeting_resp["attendees"],
                    "link": create_meeting_resp["meeting_link"],
                }
                st.session_state.draft_meeting = {
                    "title": "",
                    "description": "",
                    "start_time": datetime.today().date(),
                    "time": time(10, 0),
                    "attendee_list": [],
                    "link": "",
                }
                st.rerun()

        if cancelled:
            st.session_state.draft_meeting = {
                "title": "",
                "description": "",
                "start_time": datetime.today().date(),
                "time": time(10, 0),
                "attendee_list": [],
                "link": "",
            }
            st.session_state.message = {
                "text": "Meeting creation canceled successfully!",
                "type": "success",
            }
            st.rerun()

    # Display message if exists
    if st.session_state.message["text"]:
        if st.session_state.message["type"] == "success":
            st.success(st.session_state.message["text"])
        elif st.session_state.message["type"] == "error":
            st.error(st.session_state.message["text"])
        st.session_state.message = {"text": "", "type": None}


def main():
    """Main function"""
    st.set_page_config(
        page_title="Meeting Management", page_icon="📅", layout="centered"
    )
    create_meeting()


if __name__ == "__main__":
    main()
