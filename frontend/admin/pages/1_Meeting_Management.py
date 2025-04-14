import streamlit as st
from pages.views.edit_meetings import edit_meetings
from pages.views.create_meeting import create_meeting
from pages.views.view_meetings import view_meetings_data


def main():
    st.title("Meeting Management")
    tab1, tab2, tab3 = st.tabs(["Create Meeting", "View Meetings", "Edit Meetings"])

    with tab1:
        create_meeting()
    with tab2:
        view_meetings_data()
    with tab3:
        edit_meetings()


if __name__ == "__main__":
    main()
