import streamlit as st
from datetime import datetime

DEMO_EMPLOYEES = [
    {"id": 1, "name": "Arjun Sharma", "department": "Engineering"},
    {"id": 2, "name": "Priya Patel", "department": "Marketing"},
    {"id": 3, "name": "Rahul Gupta", "department": "Sales"},
    {"id": 4, "name": "Ananya Singh", "department": "Engineering"},
    {"id": 5, "name": "Vikram Joshi", "department": "HR"},
    {"id": 6, "name": "Neha Reddy", "department": "Product"},
    {"id": 7, "name": "Rohan Malhotra", "department": "Engineering"},
    {"id": 8, "name": "Divya Iyer", "department": "Marketing"},
    {"id": 9, "name": "Aditya Kapoor", "department": "Finance"},
    {"id": 10, "name": "Isha Nair", "department": "Operations"},
    {"id": 11, "name": "Kabir Verma", "department": "Design"},
    {"id": 12, "name": "Meera Choudhary", "department": "Customer Support"}
]

DEMO_MEETINGS = [
    # Past Meetings
    {
        "title": "Q3 Financial Review",
        "description": "Quarterly financial results discussion",
        "date": datetime(2023, 10, 15, 14, 0),
        "attendees": [1, 2, 3, 5],
        "report_url": "https://example.com/reports/q3-financial.pdf",
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    {
        "title": "Product Roadmap",
        "description": "Planning next year's product features",
        "date": datetime(2023, 10, 20, 11, 30),
        "attendees": [1, 4, 6, 7],
        "report_url": "https://example.com/reports/product-roadmap.pdf",
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    {
        "title": "Marketing Strategy",
        "description": "Annual marketing plan discussion",
        "date": datetime(2023, 11, 5, 10, 0),
        "attendees": [2, 3, 8, 12],
        "report_url": "https://example.com/reports/marketing-strategy.pdf",
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    {
        "title": "HR Policies Review",
        "description": "Discussion on updated company policies",
        "date": datetime(2023, 11, 12, 15, 30),
        "attendees": [5, 9, 10, 11],
        "report_url": "https://example.com/reports/hr-policies.pdf",
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    {
        "title": "Engineering Retrospective",
        "description": "Sprint retrospective meeting",
        "date": datetime(2023, 11, 18, 13, 0),
        "attendees": [1, 4, 7, 11],
        "report_url": "https://example.com/reports/eng-retrospective.pdf",
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    
    # Upcoming Meetings
    {
        "title": "Quarterly Planning",
        "description": "Discuss Q2 goals and objectives",
        "date": datetime(2025, 11, 15, 9, 30),
        "attendees": [1, 3, 4, 7],
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    {
        "title": "Product Launch",
        "description": "Finalizing launch plans for new product",
        "date": datetime(2025, 11, 20, 14, 0),
        "attendees": [2, 4, 6, 8, 10],
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    {
        "title": "Sales Training",
        "description": "New sales techniques workshop",
        "date": datetime(2025, 11, 25, 11, 0),
        "attendees": [3, 5, 8, 9, 12],
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    {
        "title": "All-Hands Meeting",
        "description": "Company-wide monthly meeting",
        "date": datetime(2025, 12, 1, 16, 0),
        "attendees": [x['id'] for x in DEMO_EMPLOYEES],
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    {
        "title": "Budget Planning",
        "description": "Next fiscal year budget discussion",
        "date": datetime(2025, 12, 5, 10, 30),
        "attendees": [1, 5, 9, 10],
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    {
        "title": "Customer Feedback Review",
        "description": "Analyzing recent customer feedback",
        "date": datetime(2025, 12, 10, 13, 30),
        "attendees": [2, 3, 6, 8, 12],
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    },
    
    # Live Meeting
    {
        "title": "Weekly Standup",
        "description": "Daily team sync meeting",
        "date": datetime.now(),
        "attendees": [1, 2, 4, 6, 7],
        "meeting_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDZlYzE1YjYtZDM5Yi00ZGU1LThiNTMtMjA1YzUyMWM1ZWE0%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%225e8b0f4d-2cd4-4e17-9467-b0f6e5c0b4e5%22%7d"
    }
]

def initialize_demo_data():
    """Initialize demo data in session state if not already present"""
    if 'meetings_db' not in st.session_state:
        st.session_state.meetings_db = DEMO_MEETINGS.copy()
    
    if 'demo_employees' not in st.session_state:
        st.session_state.demo_employees = DEMO_EMPLOYEES.copy()