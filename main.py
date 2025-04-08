import streamlit as st
import json
from pathlib import Path
from frontend.user import user_dash
from frontend.admin import Home
import importlib
from pathlib import Path

# Load employee data
def load_employee_data():
    employee_file = Path("models") / "employee.json"
    with open(employee_file, "r") as f:
        return json.load(f)

# Authenticate user
def authenticate_user(email, password, employees):
    for emp in employees:
        if emp["emp_email"] == email and emp["emp_password"] == password:
            return emp
    return None

# Admin Dashboard
def admin_dashboard():
    st.set_page_config(page_title="Admin Dashboard", layout="wide")
    st.title("Admin Dashboard")
    st.write(f"Welcome, {st.session_state['user']['emp_name']} (Admin)!")
    
    # Admin content here
    st.write("You have administrator privileges.")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# User Dashboard
def user_dashboard():
    st.set_page_config(page_title="User Dashboard", layout="wide")
    st.title("User Dashboard")
    st.write(f"Welcome, {st.session_state['user']['emp_name']}!")
    
    # User content here
    st.write("This is your personal dashboard.")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# Login page
def login_page():
    st.set_page_config(page_title="Login", page_icon="🔒", layout="centered")
    
    st.title("🔒 Employee Login")
    st.markdown("---")
    
    employees = load_employee_data()
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if not email or not password:
                st.error("Please fill in all fields")
            else:
                user = authenticate_user(email, password, employees)
                if user:
                    st.session_state["user"] = user
                    st.session_state["page"] = "admin_dashboard" if user["role"] == "admin" else "user_dashboard"
                    st.rerun()
                else:
                    st.error("Invalid email or password")

# Main app logic
def main():
    if "user" not in st.session_state:
        login_page()
    else:
        if st.session_state.get("page") == "admin_dashboard":
            Home.main()
        else:
            user_dash.main()

if __name__ == "__main__":
    main()