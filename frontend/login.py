import streamlit as st
import hashlib

# Page Configuration
st.set_page_config(
    page_title="Virtual Attention Checker - Login",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# Custom CSS with improvements
st.markdown("""
<style>
    /* Main container */
    .main {
        max-width: 280px;
        padding: 1.5rem;
        margin: 10px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background-color: var(--background-color);
    }
    
    /* Title styling */
    .title {
        text-align: center;
        color: var(--primary-text-color);
        margin-bottom: 1.2rem;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Input fields container - tighter and centered */
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
    }
    
    /* Input fields - prevent text overflow and scrolling */
    .stTextInput>div>div>input {
        border-radius: 6px;
        border: 1px solid var(--secondary-background-color);
        padding: 8px 30px 8px 10px !important;
        width: 120% !important;
        text-align: left;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Password toggle button - fixed positioning */
    .stTextInput>div>div>button {
        position: absolute !important;
        right: 10px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 10;
        background: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 24px !important;
        width: 24px !important;
    }
    
    /* Ensure password toggle button is on top of input */
    .stTextInput>div>div {
        position: relative !important;
    }
    
    /* Password field */
    .stTextInput>div>div>input[type="password"] {
        font-family: monospace;
        padding-right: 5px !important;
        letter-spacing: 1px;
    }
    
    /* Checkbox container - centered */
    .stCheckbox {
        display: flex;
        justify-content: center;
        width: 100%;
        margin: 0.5rem 0 1rem 0 !important;
    }
    
    .stCheckbox>label {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        max-width: 220px;
    }
    
    /* Button container - centered */
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
        margin: 1rem 0 0 0 !important;
    }
    
    /* Button styling with hover effect */
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
    
    /* Dark mode variables */
    [data-theme="light"] {
        --background-color: white;
        --primary-text-color: #2c3e50;
        --secondary-background-color: #dfe6e9;
        --primary-color: #3498db;
        --primary-hover: #2980b9;
        --button-text-color: white;
        --main-background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    [data-theme="dark"] {
        --background-color: #1e2227;
        --primary-text-color: #f0f2f6;
        --secondary-background-color: #2a323d;
        --primary-color: #1d6fa5;
        --primary-hover: #15567d;
        --button-text-color: #f0f2f6;
        --main-background: linear-gradient(135deg, #0f0c29 0%, #302b63 100%);
    }
</style>
""", unsafe_allow_html=True)

# Rest of the code remains the same as in the previous version
# (User database, authentication function, and login page content)

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
    if username in USER_DATABASE:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if USER_DATABASE[username]["password_hash"] == hashed_password:
            return True, USER_DATABASE[username]
    return False, None

# Login Page Content
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # App Title
    st.markdown('<h1 class="title">Virtual Attention Checker</h1>', unsafe_allow_html=True)
    
    # Login Form
    with st.form("login_form"):
        # Username Field
        
        username = st.text_input(
            "Username",
            #placeholder="Enter your username",
            help="Your registered username",
            key="username_input"
        )
        
        # Password Field
        password = st.text_input(
            "Password",
            type="password",
            #placeholder="Enter your password",
            help="Your account password",
            key="password_input"
        )
        
        # Remember Me checkbox (centered)
        cols = st.columns([3, 4, 3])  # Create columns for centering
        with cols[1]:
            remember_me = st.checkbox("Remember me", value=False)
        
        # Login Button (centered with hover tooltip)
        cols = st.columns([7, 4, 5])  # Create columns for centering
        with cols[1]:
            login_button = st.form_submit_button("Login", type="primary")
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
                    st.session_state["remember_me"] = remember_me
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Username and password do not match")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 1.2rem; color: var(--secondary-text-color); font-size: 0.8rem;">
        © 2023 Virtual Attention Checker | v1.0.0
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Redirect if already logged in
if st.session_state.get("authenticated"):
    st.switch_page("admin\Home.py")