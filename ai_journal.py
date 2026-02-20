import streamlit as st
from openai import OpenAI
import pandas as pd
from datetime import datetime

# ----------------------
# Streamlit App Setup
# ----------------------
st.set_page_config(page_title="AI Journal 💛", page_icon="📝")
st.title("AI Journaling App 💛")
st.write("Write down your thoughts, select your mood, and get AI reflections.")

# ----------------------
# OpenAI Client
# ----------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ----------------------
# Initialize session state for entries
# ----------------------
if "entries" not in st.session_state:
    st.session_state.entries = []

# ----------------------
# User input
# ----------------------
user_input = st.text_area("Write your thoughts here:")

mood = st.selectbox(
    "Select your mood",
    ["🙂 Happy", "😐 Neutral", "😔 Sad", "😡 Angry", "😰 Anxious"]
)

# ----------------------
# Save & Reflect button
# ----------------------
if st.button("Save & Reflect") and user_input.strip() != "":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Call OpenAI for reflection
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a kind, emotionally intelligent journaling companion."},
                {"role": "user", "content": f"My mood is {mood}. Here's my journal entry: {user_input}"}
            ]
        )
        ai_reply = response.choices[0].message.content
    except Exception as e:
        ai_reply = f"AI reflection failed: {e}"

    # Save entry in session
    st.session_state.entries.append({
        "timestamp": timestamp,
        "mood": mood,
        "entry": user_input,
        "reflection": ai_reply
    })

# ----------------------
# Display past entries
# ----------------------
if st.session_state.entries:
    st.write("## Your Past Entries")

    df = pd.DataFrame(st.session_state.entries)
    df = df[::-1]  # Show newest first
    for idx, row in df.iterrows():
        st.write(f"**{row['timestamp']}** | Mood: {row['mood']}")
        st.write(row["entry"])
        st.write(f"💡 AI Reflection: {row['reflection']}")
        st.markdown("---")
