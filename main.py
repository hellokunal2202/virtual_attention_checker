import streamlit as st
from utils import helper
# Page configuration

st.set_page_config(page_title="Login Page", page_icon="🔐", layout="centered")
emp_data = helper.read_emp_data()

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main {
            background-color: #f4f4f4;
            text-align: center;
        }
        .login-container {
            max-width: 350px;
            padding: 2rem;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            margin: auto;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        input {
            border-radius: 5px !important;
        }
        .login-btn {
            background-color: #0078D4;
            color: white;
            font-weight: bold;
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }
        .login-btn:hover {
            background-color: #005a9e;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Login UI
st.markdown('<div class="title">Login</div>', unsafe_allow_html=True)

email = st.text_input("Email", placeholder="someone@yash.com")
password = st.text_input("Password", type="password")

if st.button("Login", help="Click to login"):
    if email and password:
        for emp in emp_data:
            if emp["emp_email"]==email and emp["emp_password"]==password:
                st.write(emp["emp_email"]==email)
                if emp["role"]=="admin":
                    #will redirect to admin
                    st.success("login as admin")
                    break
                else:
                    #will redirect to user
                    st.success("login as user")
                    break
                
        else:
            st.error("Please enter valid email and password.")

    else:
        st.error("Please enter email and password.")

st.markdown('</div>', unsafe_allow_html=True)
