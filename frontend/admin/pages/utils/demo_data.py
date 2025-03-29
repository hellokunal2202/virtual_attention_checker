import streamlit as st
from datetime import datetime

DEMO_EMPLOYEES = [
    {"id": 1, "name": "John Doe", "department": "Engineering"},
    {"id": 2, "name": "Jane Smith", "department": "Marketing"},
    {"id": 3, "name": "Alex Wong", "department": "Sales"},
    {"id": 4, "name": "Sarah Connor", "department": "Engineering"},
    {"id": 5, "name": "Mike Jones", "department": "HR"},
    {"id": 6, "name": "Emily Chen", "department": "Product"},
    {"id": 7, "name": "David Kim", "department": "Engineering"},
    {"id": 8, "name": "Lisa Ray", "department": "Marketing"}
]

DEMO_MEETINGS = [
    # Past Meetings (5)
    {
        "title": "Q3 Financial Review",
        "description": "Quarterly financial results discussion",
        "date": datetime(2023, 10, 15, 14, 0),
        "attendees": [1, 2, 3, 5],
        "report_url": "/reports/q3-financial.pdf"
    },
    {
        "title": "Product Roadmap",
        "description": "Planning next year's product features",
        "date": datetime(2023, 10, 20, 11, 30),
        "attendees": [1, 4, 6, 7],
        "report_url": "/reports/product-roadmap.pdf"
    },
    # ... (other past meetings)
    
    # Upcoming Meetings (6)
    {
        "title": "Quarterly Planning",
        "description": "Discuss Q2 goals and objectives",
        "date": datetime(2025, 11, 15, 9, 30),
        "attendees": [1, 3, 4, 7],
        "meeting_url": "/meet/q2-planning"
    },
    # ... (other upcoming meetings)
    
    # Live Meeting
    {
        "title": "Weekly Standup",
        "description": "Daily team sync meeting",
        "date": datetime.now(),
        "attendees": [1, 2, 4, 6, 7],
        "meeting_url": "/meet/daily-standup"
    }
]

def initialize_demo_data():
    """Initialize demo data in session state if not already present"""
    if 'meetings_db' not in st.session_state:
        st.session_state.meetings_db = DEMO_MEETINGS.copy()
    
    if 'demo_employees' not in st.session_state:
        st.session_state.demo_employees = DEMO_EMPLOYEES.copy()