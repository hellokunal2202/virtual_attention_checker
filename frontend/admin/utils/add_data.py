import requests
import traceback
import streamlit as st
from utils import BASE_URL
from .get_data import get_meetings_data


def add_meeting_data(json_data):
    try:
        meeting_respose = requests.post(f"{BASE_URL}/meetings/create", json=json_data)
        if meeting_respose.status_code == 200:
            meeting_respose = meeting_respose.json()
            get_meetings_data()
            return meeting_respose
        else:
            return None
    except Exception as e:
        print(traceback.print_exception(e))
        return None
