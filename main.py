import requests
import streamlit as st
from utils import BASE_URL
from frontend.admin.Home import main as admin_dash
from frontend.user.user_dash import main as user_dash


# Authenticate user
def authenticate_user(email, password):
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
    )

    if login_response.status_code == 200:
        st.success(
            f"Logged in Successfully as a {login_response.json()['role'].title()}"
        )
        return login_response.json()

    login_response = login_response.json()
    st.error(login_response["detail"])
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

    with st.form("login_form"):
        email = st.text_input(
            "Email", placeholder="Enter your email", value="admin@yash.com"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            value="Admin@123",
        )
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if not email or not password:
                st.error("Please fill in all fields")
            else:
                user = authenticate_user(email, password)
                if user:
                    st.session_state["user"] = user
                    st.session_state["page"] = (
                        "admin_dashboard"
                        if user["role"] == "admin"
                        else "user_dashboard"
                    )
                    st.rerun()


# Main app logic
def main():
    if "user" not in st.session_state:
        login_page()
    else:
        if st.session_state.get("page") == "admin_dashboard":
            admin_dash()
        else:
            user_dash(st.session_state["user"]["id"])


if __name__ == "__main__":
    main()
