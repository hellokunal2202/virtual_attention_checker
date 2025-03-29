import streamlit as st
from pages.utils.ui_components import persistent_logout


st.set_page_config(page_title="Settings", layout="wide")
persistent_logout()