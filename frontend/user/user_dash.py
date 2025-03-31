import streamlit as st
 
import os
 
# Page Configuration
 
st.set_page_config(page_title="User Dashboard", layout="wide")
st.title("User Dashboard")
 
# Define the folder to store images
 
UPLOAD_FOLDER = "uploaded_images"
 
if not os.path.exists(UPLOAD_FOLDER):
 
    os.makedirs(UPLOAD_FOLDER)  # Create the folder if it doesn't exist
 
# Simulated User Session
 
if "user_name" not in st.session_state:
 
    st.session_state["user_name"] = "Kunal Mali"
 
    st.session_state["role"] = "Associate Trainee"
 
    st.session_state["email"] = "kunal.mali@yash.com"
 
    st.session_state["last_login"] = "Updating..."
 
    st.session_state["profile_completed"] = False  # Track profile completion
 
# Header Section with Logout Button
 
col1, col2, col3 = st.columns([1.75, 4, 1])  # Define three columns
 
with col1:
 
    st.image("myimg.png")
 
with col2:
 
    st.subheader(st.session_state["user_name"])
 
    st.markdown(f"""
 
    - **Role:** {st.session_state["role"]}
 
    - **Email:** {st.session_state["email"]}
 
    - **Last Login:** {st.session_state["last_login"]}
 
    """)
 
with col3:
 
    if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
 
        st.session_state.clear()
 
        st.rerun()
 
# **Profile Completion Section**
 
if not st.session_state["profile_completed"]:
 
    st.warning("⚠️ Complete your profile by uploading exactly 5 PNG images.")
 
    # Upload images
 
    uploaded_files = st.file_uploader(
 
        "Upload exactly 5 PNG images", type=["png"], accept_multiple_files=True
 
    )
 
    if uploaded_files:
 
        if len(uploaded_files) == 5:
 
            # Save images in the folder
 
            for i, file in enumerate(uploaded_files):
 
                file_path = os.path.join(UPLOAD_FOLDER, f"user_image_{i+1}.png")
 
                with open(file_path, "wb") as f:
 
                    f.write(file.getbuffer())
 
            # Mark profile as completed
 
            st.session_state["profile_completed"] = True
 
            st.success("✅ Profile completed successfully!")
 
            st.rerun()  # Refresh to remove the warning
 
        else:
 
            st.error("❌ Please upload exactly 5 PNG images.")
 
else:
 
    st.success("✅ Profile completed successfully!")
 
 