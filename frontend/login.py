import streamlit as st
import hashlib
from pathlib import Path
import sys

# Page Configuration (must be first)
st.set_page_config(
    page_title="Virtual Attention Checker - Login",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# Add admin directory to Python path for imports
admin_path = str(Path(__file__).parent / "admin")
sys.path.append(admin_path)

# Custom CSS (your complete original CSS)
st.markdown("""
<style>
    /* Modified Main Container */
    .main {
        max-width: 280px;
        min-height: 10px;
        padding: 1.5rem;
        margin: 20px auto;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background-color: var(--background-color);
        display: flex;
        flex-direction: column;
    }

    /* Ensure form content uses available space */
    .main form {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    /* Title styling */
    .title {
        text-align: center;
        color: var(--primary-text-color);
        margin-bottom: 1.2rem;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Input fields container */
    .stTextInput {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    
    .stTextInput>div {
        width: 100% !important;
        max-width: 220px !important;
    }
    
    .stTextInput>div>div {
        width: 100% !important;
        margin: 0 auto 0.5rem auto !important;
        position: relative !important;
    }
    
    /* Input fields styling */
    .stTextInput>div>div>input {
        border-radius: 6px;
        border: 1px solid var(--secondary-background-color);
        padding: 8px 35px 8px 10px !important;
        width: 100% !important;
        text-align: left;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        box-sizing: border-box !important;
    }
    
    /* Password toggle button - improved positioning */
    .stTextInput>div>div>button {
        position: absolute !important;
        right: 8px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        background: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: 24px !important;
        min-width: 24px !important;
        height: 24px !important;
        width: 24px !important;
        cursor: pointer;
        color: var(--primary-text-color) !important;
    }
    
    /* Password field specific styles */
    .stTextInput>div>div>input[type="password"] {
        font-family: monospace;
        letter-spacing: 1px;
        padding-right: 35px !important;
    }
    
    /* Button container */
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
        margin: 1rem 0 0 0 !important;
    }
    
    /* Button styling */
    .stButton>button {
        width: 60%;
        border-radius: 6px;
        padding: 0.5rem;
        font-weight: 600;
        background-color: var(--primary-color);
        border: none;
        transition: all 0.2s ease;
        color: var(--button-text-color);
        cursor: pointer;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-hover);
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Error message */
    .stAlert {
        border-radius: 6px;
        max-width: 220px;
        margin: 0 auto 0.8rem auto !important;
        padding: 0.5rem !important;
        text-align: center;
    }
    
    /* Background */
    .stApp {
        background: var(--main-background);
        background-attachment: fixed;
        padding: 1rem !important;
    }
    
    /* Light mode variables */
    [data-theme="light"] {
        --background-color: white;
        --primary-text-color: #2c3e50;
        --secondary-background-color: #dfe6e9;
        --primary-color: #3498db;
        --primary-hover: #2980b9;
        --button-text-color: white;
        --main-background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Dark mode variables */
    [data-theme="dark"] {
        --background-color: #1e2227;
        --primary-text-color: #f0f2f6;
        --secondary-background-color: #2a323d;
        --primary-color: #1d6fa5;
        --primary-hover: #15567d;
        --button-text-color: #f0f2f6;
        --main-background: linear-gradient(135deg, #0f0c29 0%, #302b63 100%);
    }
    
    /* Hide input instructions */
    .stTextInput [data-testid="InputInstructions"] {
        display: none;
    }
    
    /* Label styling */
    .stTextInput label {
        margin-bottom: 8px !important;
        display: flex !important;
        align-items: center !important;
        gap: 4px !important;
        margin-right: 12px !important;
    }

    /* Input field spacing */
    .stTextInput>div>div {
        margin-top: 12px !important;
    }
    
    /* Fix for button hover state */
    .stTextInput>div>div>button:hover {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Mock user database
USER_DATABASE = {
    "admin": {
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "name": "Administrator",
        "role": "admin"
    },
    "user1": {
        "password_hash": hashlib.sha256("password1".encode()).hexdigest(),
        "name": "John Doe",
        "role": "user"
    }
}

def authenticate(username, password):
    """Authenticate user against the database"""
    username = username.lower().strip()
    if username in USER_DATABASE:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if USER_DATABASE[username]["password_hash"] == hashed_password:
            return True, USER_DATABASE[username]
    return False, None

# If already authenticated, redirect immediately
if st.session_state.get("authenticated"):
    role = st.session_state.get("user_info", {}).get("role")
    if role == "admin":
        from admin.Home import main as admin_main
        admin_main()
        st.stop()
    # elif role == "user":
    #     from user.Dashboard import main as user_main
    #     user_main()
    #     st.stop()

# Login Page Content
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="title">Virtual Attention Checker</h1>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input(
            "Username\u00A0\u00A0\u00A0",
            help="Your registered username",
            key="username_input",
            label_visibility="visible"
        )
        
        password = st.text_input(
            "Password\u00A0\u00A0\u00A0",
            type="password",
            help="Your account password",
            key="password_input",
            label_visibility="visible"
        )
        
        col1, col2, col3 = st.columns([4, 2, 3])
        with col2:
            login_button = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if login_button:
            if not username and not password:
                st.error("Please enter both username and password")
            elif not username:
                st.error("Please enter your username")
            elif not password:
                st.error("Please enter your password")
            else:
                authenticated, user_info = authenticate(username, password)
                if authenticated:
                    st.session_state["authenticated"] = True
                    st.session_state["user_info"] = user_info
                    st.session_state["username"] = username
                    st.success("Login successful! Redirecting...")
                    
                    # Force immediate redirect
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")

    st.markdown("""
    <div style="text-align: center; margin-top: 1.2rem; color: var(--secondary-text-color); font-size: 0.8rem;">
        © 2023 Virtual Attention Checker | v1.0.0
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Block back navigation
st.markdown("""
<script>
    history.pushState(null, null, location.href);
    window.onpopstate = function(event) {
        history.go(1);
    };
</script>
""", unsafe_allow_html=True)