import streamlit as st
import os
import shutil
from pathlib import Path
import sys
import importlib

# Add user directory to Python path
user_path = str(Path(__file__).parent)
sys.path.append(user_path)

def get_user_pages():
    """Dynamically discover all user pages"""
    pages_dir = Path(__file__).parent / "pages"
    page_files = sorted([f for f in pages_dir.glob("[0-9]_*.py")])
    
    pages = []
    for page_file in page_files:
        pages.append({
            "name": page_file.stem.replace("_", " ").title(),
            "path": str(page_file),
            "module_name": f"pages.{page_file.stem}",
            "icon": "📄"  # Default icon
        })
    return pages

def load_page_module(module_name):
    """Safely import a page module"""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        st.error(f"Failed to load page module: {e}")
        return None

def main():
    """Main function to run the user dashboard"""
    # Page Configuration
    st.set_page_config(
        page_title="User Dashboard", 
        page_icon="👤",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for styling
    st.markdown("""
    <style>
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background-color: #f0f2f6;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        [data-testid="stSidebarNav"] {
            max-height: 100vh !important;
            overflow-y: auto !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Navigation
    with st.sidebar:
        st.subheader("User Navigation")
        
        # Get all available pages
        user_pages = get_user_pages()
        
        # Add navigation
        st.divider()
        if st.button("🏠 Dashboard", use_container_width=True, 
                    type="primary" if not st.session_state.get('current_page') else "secondary"):
            st.session_state.current_page = None
            st.rerun()
        
        for page in user_pages:
            if st.button(
                f"{page['icon']} {page['name']}", 
                use_container_width=True,
                key=f"nav_{page['path']}",
                type="primary" if st.session_state.get('current_page') == page['path'] else "secondary"
            ):
                st.session_state.current_page = page['path']
                st.rerun()
        
        st.divider()
        if st.button("🚪 Logout", key="logout_btn_sidebar", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # Page rendering logic
    if st.session_state.get('current_page'):
        # Dynamically render the selected page
        selected_page = next((p for p in get_user_pages() if p['path'] == st.session_state.current_page), None)
        if selected_page:
            module = load_page_module(selected_page['module_name'])
            if module:
                try:
                    if hasattr(module, 'main'):
                        module.main()
                    else:
                        st.error("Page module has no main() function")
                except Exception as e:
                    st.error(f"Error executing page: {e}")
    else:
        # Original dashboard content
        st.title("User Dashboard")
        
        # Define the folder to store images
        UPLOAD_FOLDER = "uploaded_images"
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Simulated User Session
        if "user_name" not in st.session_state:
            st.session_state["user_name"] = "Sam Malviya"
            st.session_state["role"] = "Associate Trainee"
            st.session_state["email"] = "sam.malviya@yash.com"
            st.session_state["last_login"] = "Updating..."
            st.session_state["profile_completed"] = False
            st.session_state["edit_mode"] = False

        # Header Section
        col1, col2 = st.columns([1.75, 4])  # Removed the third column for logout
        with col1:
            st.image(r"frontend\user\view.png")

        with col2:
            st.subheader(st.session_state["user_name"])
            st.markdown(f"""
            - **Role:** {st.session_state["role"]}
            - **Email:** {st.session_state["email"]}
            - **Last Login:** {st.session_state["last_login"]}
            """)

        # Get saved images from folder
        saved_images = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".png")]

        # Determine if profile is completed
        st.session_state["profile_completed"] = len(saved_images) == 5

        # If profile is completed, show the success message and Edit button
        if st.session_state["profile_completed"] and not st.session_state["edit_mode"]:
            st.success("✅ Profile completed successfully!")

            if st.button("✏️ Edit", key="edit_btn"):
                shutil.rmtree(UPLOAD_FOLDER)
                os.makedirs(UPLOAD_FOLDER)
                st.session_state["profile_completed"] = False
                st.session_state["edit_mode"] = True
                st.rerun()

        # Show file uploader only if the profile is not completed
        if not st.session_state["profile_completed"]:
            uploaded_files = st.file_uploader("Upload exactly 5 PNG images", type=["png","jpg","jpeg"], accept_multiple_files=True)

            if uploaded_files:
                if len(uploaded_files) == 5:
                    # Save uploaded images
                    for i, file in enumerate(uploaded_files):
                        file_path = os.path.join(UPLOAD_FOLDER, f"user_image_{i+1}.png")
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())

                    st.session_state["profile_completed"] = True
                    st.session_state["edit_mode"] = False
                    st.success("✅ Profile completed successfully!")
                    st.rerun()
                else:
                    st.error("❌ Please upload exactly 5 PNG images.")

        # Show uploaded images preview if images exist
        if saved_images:
            st.subheader("Uploaded Images Preview:")
            cols = st.columns(5)

            for i, image_name in enumerate(sorted(saved_images)):  
                image_path = os.path.join(UPLOAD_FOLDER, image_name)
                with cols[i]:
                    st.image(image_path, caption=f"Image {i+1}", use_container_width=True)

if __name__ == "__main__":
    main()