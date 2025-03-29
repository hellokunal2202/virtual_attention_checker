import streamlit as st
import hashlib
from utils import helper

# Page Configuration
st.set_page_config(
    page_title="Virtual Attention Checker - Login",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load employee data
emp_data = helper.read_emp_data()

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main container */
    .login-container {
        max-width: 300px;
        padding: 2rem;
        margin: auto;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background-color: #fff;
        text-align: center;
    }

    /* Title */
    .title {
        color: #2c3e50;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Input fields */
    .stTextInput>div>div {
        width: 100%;
        margin: auto;
    }

    /* Login button */
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        padding: 0.6rem;
        font-weight: 600;
        background-color: #0078D4;
        border: none;
        color: white;
        cursor: pointer;
        transition: 0.2s;
    }

    .stButton>button:hover {
        background-color: #005a9e;
        transform: translateY(-1px);
    }

    /* Error messages */
    .stAlert {
        text-align: center;
        max-width: 250px;
        margin: auto;
    }

</style>
""", unsafe_allow_html=True)

# If user is logged in, display success message
if st.session_state.authenticated:
    st.success(f"Logged in as {st.session_state.user_role}")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.rerun()
else:
    # Login Form
    with st.form("login_form"):
        # st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="title">Virtual Attention Checker</h1>', unsafe_allow_html=True)

        email = st.text_input("Email", placeholder="someone@yash.com")
        password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login")

        st.markdown('</div>', unsafe_allow_html=True)

    # Authentication
    if login_submit:
        if email and password:
            for emp in emp_data:
                if emp["emp_email"] == email and emp["emp_password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Admin" if emp["role"] == "admin" else "User"
                    st.success(f"Logged in as {st.session_state.user_role}")
                    st.rerun()
                    break
            else:
                st.error("Invalid email or password.")
        else:
            st.error("Please enter email and password.")
