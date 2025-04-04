import streamlit as st
import os
import shutil  # For deleting all images at once

def main():
# Page Configuration
    st.set_page_config(page_title="User Dashboard", layout="wide")
    st.title("User Dashboard")

    # Define the folder to store images
    UPLOAD_FOLDER = "uploaded_images"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  # Create the folder if it doesn't exist

    # Simulated User Session
    if "user_name" not in st.session_state:

        st.session_state["user_name"] = "Sam Malviya"
        st.session_state["role"] = "Associate Trainee"
        st.session_state["email"] = "sam.malviya@yash.com"
        st.session_state["last_login"] = "Updating..."
        st.session_state["profile_completed"] = False  # Track profile completion
        st.session_state["edit_mode"] = False  # Track if user is in edit mode

    # Header Section with Logout Button
    col1, col2, col3 = st.columns([1.75 , 4 ,  1])  # Define three columns
    with col1:
        st.image("view.png")

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

    # Get saved images from folder
    saved_images = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".png")]

    # Determine if profile is completed
    st.session_state["profile_completed"] = len(saved_images) == 5

    # If profile is completed, show the success message and Edit button
    if st.session_state["profile_completed"] and not st.session_state["edit_mode"]:
        st.success("✅ Profile completed successfully!")

        if st.button("✏️ Edit", key="edit_btn"):
            shutil.rmtree(UPLOAD_FOLDER)  # Delete all uploaded images
            os.makedirs(UPLOAD_FOLDER)  # Recreate the folder
            st.session_state["profile_completed"] = False
            st.session_state["edit_mode"] = True
            st.rerun()  # Refresh the page

    # Show file uploader only if the profile is not completed
    if not st.session_state["profile_completed"]:
        uploaded_files = st.file_uploader("Upload exactly 5 PNG images", type=["png","jpg","jpeg"], accept_multiple_files=True)

        if uploaded_files:
            if len(uploaded_files) == 5:

                # Save uploaded images
                for i, file in enumerate(uploaded_files):
                    file_path = os.path.join(UPLOAD_FOLDER, f"user_image_{i+1}.png")
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())  # Save file to disk

                st.session_state["profile_completed"] = True
                st.session_state["edit_mode"] = False
                st.success("✅ Profile completed successfully!")
                st.rerun()  # Refresh the page
            else:
                st.error("❌ Please upload exactly 5 PNG images.")

    # Show uploaded images preview if images exist
    if saved_images:
        st.subheader("Uploaded Images Preview:")
        cols = st.columns(5)  # Create 5 columns for the images

        for i, image_name in enumerate(sorted(saved_images)):  
            image_path = os.path.join(UPLOAD_FOLDER, image_name)
            with cols[i]:  # Assign each image to a column
                st.image(image_path, caption=f"Image {i+1}", use_container_width=True) 

if __name__ == "__main__":
    main() 