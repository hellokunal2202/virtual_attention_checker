import streamlit as st

def persistent_logout(position="sidebar", key_suffix=""):
    """
    Adds logout button that appears on all pages
    Args:
        position: "sidebar" or "main" (where to place the button)
        key_suffix: Unique string to make the button key unique
    """
    # CSS for positioning
    st.markdown(f"""
    <style>
        .persistent-logout {{
            position: {'fixed' if position == "main" else 'static'};
            bottom: 20px;
            width: calc(100% - 40px);
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Create unique key by combining base + suffix
    button_key = f"persistent_logout_{key_suffix}"
    
    container = st.sidebar if position == "sidebar" else st
    with container:
        st.markdown('<div class="persistent-logout">', unsafe_allow_html=True)
        if st.button("🚪 Logout", key=button_key):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)