import requests
import streamlit as st
from utils import BASE_URL


def get_users_data():
    users_data = requests.get(f"{BASE_URL}/users/get-all")
    if users_data.status_code == 200:
        users_data = users_data.json()
        st.session_state["users_data"] = users_data


def get_meetings_data():
    meetings_data = requests.get(f"{BASE_URL}/meetings/get-all")
    if meetings_data.status_code == 200:
        meetings_data = meetings_data.json()
        st.session_state["meetings"] = meetings_data


def get_data():
    get_meetings_data()
    get_users_data()
