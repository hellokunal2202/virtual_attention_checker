import streamlit as st
from pages.utils.demo_data import initialize_demo_data
from pages.utils.view_meetings import view_meetings
from pages.utils.create_meeting import create_meeting
from pages.utils.edit_meetings import edit_meetings
from pages.utils.ui_components import persistent_logout

def main():
    st.set_page_config(page_title="Meeting Management", layout="wide")
    initialize_demo_data()
    persistent_logout()
    
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