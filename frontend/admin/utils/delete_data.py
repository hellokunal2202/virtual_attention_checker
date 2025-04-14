import requests
from utils import BASE_URL
from .get_data import get_meetings_data


def delete_meeting(meeting_id: int):
    meetings_data = requests.delete(
        f"{BASE_URL}/meetings/delete?meeting_id={meeting_id}"
    )
    if meetings_data.status_code == 200:
        meetings_data = meetings_data.json()
        get_meetings_data()
        return meetings_data

    return None
