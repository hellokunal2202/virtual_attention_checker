import streamlit as st

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
    {"id": 12, "name": "Meera Choudhary", "department": "Customer Support"},
]


def initialize_demo_data():
    """Initialize demo data in session state if not already present"""

    if "users_data" in st.session_state:
        st.session_state.demo_employees = st.session_state["users_data"]
