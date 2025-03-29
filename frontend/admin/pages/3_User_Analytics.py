import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import random
from pages.utils.demo_data import DEMO_EMPLOYEES  # Updated import path

def calculate_user_metrics(user_id):
    """Calculate user metrics based on meeting attendance"""
    if 'meetings_db' not in st.session_state:
        return 0, 0, 0
    
    # Get meetings attended by user
    user_meetings = [
        m for m in st.session_state.meetings_db 
        if user_id in m['attendees']
    ]
    meetings_attended = len(user_meetings)
    
    # Calculate average engagement (mock data - replace with real calculations)
    if meetings_attended > 0:
        avg_engagement = max(60, min(95, 75 + (user_id % 30)))
    else:
        avg_engagement = 0
    
    # Calculate trend based on recent meetings (mock calculation)
    trend = (user_id % 7) - 3  # Random trend between -3 and 3
    
    return meetings_attended, avg_engagement, trend

def main():
    """User Analytics main page"""
    st.set_page_config(page_title="User Analytics", layout="wide")
    
    if 'demo_employees' not in st.session_state:
        st.session_state.demo_employees = DEMO_EMPLOYEES
    
    st.title("User Analytics Dashboard")
    
    if not st.session_state.demo_employees:
        st.warning("No user data available")
        return
    
    # User selection dropdown
    selected_user = st.selectbox(
        "Select User",
        options=st.session_state.demo_employees,
        format_func=lambda emp: f"{emp['name']} ({emp['department']})",
        key="user_selector"
    )
    
    if selected_user:
        user_id = selected_user['id']
        user_name = selected_user['name']
        
        # Calculate metrics
        meetings, avg_score, trend = calculate_user_metrics(user_id)
        
        # Display metrics
        st.subheader(f"Analytics for {user_name}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Meetings Attended", meetings)
        with col2:
            st.metric("Average Engagement", f"{avg_score}%")
        with col3:
            trend_label = "↑ Improving" if trend >= 0 else "↓ Declining"
            st.metric("Weekly Trend", f"{abs(trend)}%", trend_label)
        
        # Engagement trend chart
        st.subheader("Engagement Trend")
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Generate mock trend data
        dates = pd.date_range(end=datetime.today(), periods=8, freq='W')
        scores = [max(50, min(100, avg_score + (i * trend) + random.randint(-5, 5))) 
                 for i in range(8)]
        
        ax.plot(dates, scores, marker='o', color='#FF6D00', linewidth=2)
        ax.set_ylim(0, 100)
        ax.set_xlabel("Week")
        ax.set_ylabel("Engagement Score")
        ax.grid(True, linestyle=':', alpha=0.5)
        st.pyplot(fig)
        
        # Recent meetings section
        if 'meetings_db' in st.session_state:
            user_meetings = [
                m for m in st.session_state.meetings_db 
                if user_id in m['attendees']
            ][-5:]  # Get last 5 meetings
            
            if user_meetings:
                st.subheader("Recent Meetings Attended")
                for meeting in reversed(user_meetings):
                    with st.expander(f"{meeting['title']} - {meeting['date'].strftime('%b %d')}"):
                        st.write(f"**Date:** {meeting['date'].strftime('%A, %B %d, %Y')}")
                        st.write(f"**Attendees:** {len(meeting['attendees'])}")

if __name__ == "__main__":
    main()