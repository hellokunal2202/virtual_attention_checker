# utils/ui_components.py
import streamlit as st

def persistent_logout():
    """Adds logout button that appears on all pages"""
    st.markdown("""
    <style>
        .persistent-logout {
            position: fixed;
            bottom: 20px;
            width: calc(100% - 40px);
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div class="persistent-logout">', unsafe_allow_html=True)
        if st.button("🚪 Logout", key="persistent_logout"):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)