import streamlit as st

st.set_page_config(
    page_title="User Dashboard",
    layout="wide"
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
    .admin-card {
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .stats-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .logout-btn {
        background-color: #ff4b4b !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Header with logout button
col1, col2 = st.columns([4, 1])
with col1:
    st.title("Your Profile")
with col2:
    if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# Admin Profile Section
with st.container():
    st.markdown("<div class='header'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("myimg.png", width=150)
    
    with col2:
        st.subheader("Kunal Mali")
        st.markdown(f"""
        - **Role:** Associate Trainee
        - **Email:** kunal.mali@yash.com
        - **Last Login:** updating
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)


