import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------------
# Streamlit App Setup
# ----------------------
st.set_page_config(page_title="Mood & Journal Tracker 💛", page_icon="📝")
st.title("🌈 Mood & Journal Tracker")
st.write("Track your moods, write reflections, and see your history.")

# ----------------------
# Initialize session state
# ----------------------
if "entries" not in st.session_state:
    st.session_state.entries = []

# ----------------------
# Mood options with color codes
# ----------------------
mood_options = {
    "🙂 Happy": "#FFD700",
    "😐 Neutral": "#87CEEB",
    "😔 Sad": "#6495ED",
    "😡 Angry": "#FF6347",
    "😰 Anxious": "#FF4500",
    "😶 Feeling nothing": "#C0C0C0"
}

# ----------------------
# User input
# ----------------------
st.subheader("Write your reflection")
user_input = st.text_area("Your thoughts here:")

mood = st.selectbox(
    "Select your mood:",
    list(mood_options.keys())
)

# ----------------------
# Save button
# ----------------------
if st.button("Save Reflection") and user_input.strip() != "":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.session_state.entries.append({
        "timestamp": timestamp,
        "mood": mood,
        "entry": user_input
    })
    
    st.success("Reflection saved!")

# ----------------------
# Display past entries by date
# ----------------------
if st.session_state.entries:
    st.subheader("📅 Past Reflections")
    
    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.entries)
    
    # Group by date
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    dates = df['date'].unique()[::-1]  # newest first
    
    for date in dates:
        st.markdown(f"### {date}")
        daily_entries = df[df['date'] == date]
        for idx, row in daily_entries.iterrows():
            color = mood_options.get(row["mood"], "#FFFFFF")
            st.markdown(
                f"<div style='background-color:{color}; padding:10px; border-radius:10px; margin-bottom:5px'>"
                f"<strong>{row['timestamp']} | {row['mood']}</strong><br>{row['entry']}</div>",
                unsafe_allow_html=True
            )
