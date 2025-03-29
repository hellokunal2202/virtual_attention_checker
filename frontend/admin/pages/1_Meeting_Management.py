import streamlit as st
from pages.utils.demo_data import initialize_demo_data
from pages.utils.View_Meetings import view_meetings
from pages.utils.Create_Meeting import create_meeting
from pages.utils.Edit_Meetings import edit_meetings


def main():
    st.set_page_config(page_title="Meeting Management", layout="wide")
    initialize_demo_data()
    
    st.title("Meeting Management")
    tab1, tab2, tab3 = st.tabs(["Create Meeting", "View Meetings", "Edit Meetings"])
    
    with tab1:
        create_meeting()
    with tab2:
        view_meetings()
    with tab3:
        edit_meetings()

if __name__ == "__main__":
    main()