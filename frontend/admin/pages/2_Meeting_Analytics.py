import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pages.utils.demo_data import DEMO_EMPLOYEES,initialize_demo_data
from pages.utils.ui_components import persistent_logout

def main():
    st.set_page_config(page_title="Meeting Analytics", layout="wide")
    initialize_demo_data()
    persistent_logout()
    
    st.title("Meeting Analytics")
    if 'meetings_db' not in st.session_state or not st.session_state.meetings_db:
        st.warning("No meetings available for analytics")
        return
    
    # Create DataFrame from meetings data
    meetings_df = pd.DataFrame(st.session_state.meetings_db)
    meetings_df['date'] = pd.to_datetime(meetings_df['date'])
    
    # Meeting selection
    meeting_options = {
        idx: f"{row['title']} ({row['date'].strftime('%Y-%m-%d')})" 
        for idx, row in meetings_df.iterrows()
    }
    
    selected_idx = st.selectbox(
        "Select Meeting",
        options=list(meeting_options.keys()),
        format_func=lambda x: meeting_options[x],
        key="meeting_selector"
    )
    
    if selected_idx is not None:
        meeting = st.session_state.meetings_db[selected_idx]
        st.subheader(f"Meeting: {meeting['title']}")
        
        # Generate analytics data (mock - replace with real data)
        duration_minutes = 60  # Default duration
        base_date = meeting['date']
        time_points = []
        
        for minute in range(0, duration_minutes + 1, 10):
            time_points.append({
                "timestamp": (base_date + timedelta(minutes=minute)),
                "engagement": max(40, min(95, 70 + (minute % 20) - 10))
            })
        
        df = pd.DataFrame(time_points)
        
        # Display metrics
        avg_engagement = round(df['engagement'].mean(), 1)
        participants = len(meeting['attendees'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Engagement", f"{avg_engagement}%")
        with col2:
            st.metric("Participants", participants)
        
        # Display attendees
        with st.expander("View Attendees"):
            for attendee_id in meeting['attendees']:
                emp = next((e for e in DEMO_EMPLOYEES if e['id'] == attendee_id), None)
                if emp:
                    st.write(f"- {emp['name']} ({emp['department']})")
        
        # Engagement chart
        st.subheader("Engagement Over Time")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['timestamp'], df['engagement'], 
                marker='o', color='#4CAF50', linewidth=2)
        ax.set_xlabel("Time", fontsize=10)
        ax.set_ylabel("Engagement (%)", fontsize=10)
        ax.set_ylim(0, 100)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        st.pyplot(fig)
        
if __name__ == "__main__":
    main()