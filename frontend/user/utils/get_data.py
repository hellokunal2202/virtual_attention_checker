import requests
import streamlit as st
from utils import BASE_URL


def get_user_data(user_id: int):
    user_data = requests.get(f"{BASE_URL}/users/full-details?user_id={user_id}")
    if user_data.status_code == 200:
        st.session_state["user"] = user_data.json()


def get_meetings_data(user_id: int):
    meetings_data = requests.get(f"{BASE_URL}/meetings/get-all")
    if meetings_data.status_code == 200:
        meetings_data = meetings_data.json()
        meetings_data = [
            meeting for meeting in meetings_data if user_id in meeting["attendee_list"]
        ]
        st.session_state["meetings"] = meetings_data


def initialize_data(user_id: int):
    get_user_data(user_id)
    get_meetings_data(user_id)
