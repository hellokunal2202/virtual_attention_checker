import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
from pages.utils.demo_data import DEMO_EMPLOYEES  # Updated import path
from pages.utils.ui_components import persistent_logout

def generate_time_series_data(duration_minutes):
    """Generate realistic attention time series data for a meeting"""
    points = duration_minutes // 10  # Data point every 10 minutes
    base_score = random.randint(65, 85)
    time_series = []
   
    # Generate fluctuating attention scores
    for i in range(points):
        # Create natural fluctuations
        if i == 0:
            # Starting high
            score = base_score + random.randint(5, 15)
        elif i == points-1:
            # Ending dip
            score = base_score - random.randint(5, 15)
        else:
            # Middle fluctuations
            fluctuation = random.randint(-20, 20)
            score = base_score + fluctuation
       
        # Ensure score stays within reasonable bounds
        score = max(40, min(100, score))
        time_series.append(score)
   
    return time_series

def calculate_user_metrics(user_id, meeting_history=None):
    """Calculate user metrics based on meeting attendance"""
    if meeting_history is None:
        if 'meetings_db' not in st.session_state:
            return 0, 0, 0, []
        
        # Get meetings attended by user
        meeting_history = [
            m for m in st.session_state.meetings_db 
            if user_id in m['attendees']
        ]
    
    meetings_attended = len(meeting_history)
    
    # Calculate average engagement
    if meetings_attended > 0:
        avg_engagement = round(sum(m.get('final_score', 75) for m in meeting_history) / meetings_attended, 1)
    else:
        avg_engagement = 0
    
    # Calculate trend based on recent meetings
    if meetings_attended >= 2:
        recent_scores = [m.get('final_score', 75) for m in meeting_history[-2:]]
        trend = recent_scores[-1] - recent_scores[0]
    else:
        trend = 0
    
    return meetings_attended, avg_engagement, trend, meeting_history

def main():
    """User Analytics main page with enhanced features from new code"""
    st.set_page_config(page_title="User Analytics", layout="wide")
    persistent_logout()
    if 'demo_employees' not in st.session_state:
        st.session_state.demo_employees = DEMO_EMPLOYEES
    
    st.title("User Analytics Dashboard")
    
    if not st.session_state.demo_employees:
        st.warning("No user data available")
        return
    
    # User selection dropdown - using format from old code
    selected_user = st.selectbox(
        "Select User",
        options=st.session_state.demo_employees,
        format_func=lambda emp: f"{emp['name']} ({emp['department']})",
        key="user_selector"
    )
    
    if selected_user:
        user_id = selected_user['id']
        user_name = selected_user['name']
        
        # Generate demo meeting history for this user (from new code)
        meeting_history = []
        meeting_titles = [
            "Weekly Sync", "Project Kickoff", "Sprint Planning",
            "Client Review", "Retrospective", "Product Demo"
        ]
        
        # Create 8-12 random past meetings for the user
        num_meetings = random.randint(8, 12)
        for i in range(num_meetings):
            meeting_date = datetime.today() - timedelta(days=random.randint(1, 60))
            duration = 60
            meeting_history.append({
                "meeting_id": i+1,
                "title": random.choice(meeting_titles),
                "date": meeting_date,
                "duration": duration,
                "time_series": generate_time_series_data(duration),
                "final_score": random.randint(60, 95),
                "attendees": [user_id]  # Add user to attendees
            })
        
        # Create meeting selection dropdown options (from new code)
        meeting_options = {
            "all": "All Meetings",
            **{m["meeting_id"]: f"{m['title']} ({m['date'].strftime('%Y-%m-%d %H:%M')})"
               for m in meeting_history}
        }
        
        # Meeting selection (from new code)
        selected_meeting = st.selectbox(
            "Select Meeting",
            options=list(meeting_options.keys()),
            format_func=lambda x: meeting_options[x]
        )
        
        # Filter data based on selection
        if selected_meeting == "all":
            filtered_meetings = meeting_history
            display_title = "All Meetings"
        else:
            filtered_meetings = [m for m in meeting_history if m["meeting_id"] == int(selected_meeting)]
            display_title = meeting_options[selected_meeting]
        
        # Calculate metrics using both old and new approaches
        meetings_attended, avg_score, trend, user_meetings = calculate_user_metrics(user_id, filtered_meetings)
        
        # Display header with filtered context
        st.subheader(f"Analytics for {user_name} - {display_title}")
        
        # Metrics columns - dynamic based on selection (combined approach)
        col1, col2, col3 = st.columns(3)
        
        if selected_meeting == "all":
            with col1:
                st.metric("Meetings Attended", meetings_attended)
            with col2:
                st.metric("Average Engagement", f"{avg_score}%")
            with col3:
                trend_label = "↑ Improving" if trend >= 0 else "↓ Declining"
                st.metric("Weekly Trend", f"{abs(trend)}%", trend_label)
            
            # Line chart of scores over time for all meetings (from new code)
            st.subheader("Performance Across Meetings")
            chart_data = sorted(filtered_meetings, key=lambda x: x["date"])
            dates = [m["date"] for m in chart_data]
            scores = [m["final_score"] for m in chart_data]
            
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(dates, scores, marker='o', color='#2ca02c')
            ax.set_xlabel("Meeting Date")
            ax.set_ylabel("Final Score (%)")
            ax.set_ylim(50, 100)
            ax.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig)
            
        else:
            # Specific meeting metrics (from new code)
            meeting = filtered_meetings[0]
            
            with col1:
                st.metric("Meeting Score", f"{meeting['final_score']}%")
            with col2:
                st.metric("Duration", f"{meeting['duration']} mins")
            with col3:
                engagement = "High" if meeting['final_score'] >= 80 else "Medium" if meeting['final_score'] >= 65 else "Low"
                st.metric("Engagement", engagement)
            
            # Time-series attention graph for specific meeting (from new code)
            st.subheader("Attention During Meeting")
            
            # Prepare time series data
            time_series = meeting["time_series"]
            time_labels = [f"{(meeting['date'].hour + (meeting['date'].minute + x*10)//60):02d}:{((meeting['date'].minute + x*10)%60):02d}"
                          for x in range(len(time_series))]
            
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(time_labels, time_series, marker='o', color='#1f77b4')
            ax.axhline(y=meeting['final_score'], color='r', linestyle='--', label='Average')
            ax.set_xlabel("Time (24-hour)")
            ax.set_ylabel("Attention Score (%)")
            ax.set_ylim(40, 100)
            ax.set_title(f"Attention Fluctuation - {meeting['title']}")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        
        # Detailed meeting table (from new code)
        st.subheader("Meeting Details" if selected_meeting == "all" else "Meeting Summary")
        
        # Prepare table data
        table_data = []
        for meeting in filtered_meetings:
            table_data.append({
                "Title": meeting["title"],
                "Date": meeting["date"].strftime('%Y-%m-%d %H:%M'),
                "Duration (min)": meeting["duration"],
                "Score": meeting["final_score"],
                "Status": "Completed"
            })
        
        # Display as interactive dataframe with score visualization
        df = pd.DataFrame(table_data)
        st.dataframe(
            df,
            column_config={
                "Score": st.column_config.ProgressColumn(
                    "Score",
                    help="User's attentiveness score",
                    format="%f%%",
                    min_value=0,
                    max_value=100
                )
            },
            hide_index=True,
            use_container_width=True
        )

if __name__ == "__main__":
    main()