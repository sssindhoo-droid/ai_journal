import streamlit as st
import pandas as pd
from datetime import datetime
import openai
import os

# =======================
# OpenAI API Setup
# =======================
# Make sure to set your API key in Streamlit Secrets:
# OPENAI_API_KEY = "your_api_key_here"
openai.api_key = st.secrets["OPENAI_API_KEY"]

# =======================
# Journal Data File
# =======================
DATA_FILE = "journal_entries.csv"

# Load existing entries or create a new dataframe
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["timestamp", "mood", "entry", "ai_reflection"])

# =======================
# Streamlit UI
# =======================
st.set_page_config(page_title="AI Journaling", layout="centered")
st.title("📝 AI Personal Journaling")

# --- New Entry ---
st.header("Add New Entry")
mood = st.selectbox("How are you feeling?", ["😊 Happy", "😔 Sad", "😡 Angry", "😰 Anxious", "😌 Calm", "😴 Tired"])
entry = st.text_area("Write your reflection here:")

if st.button("Save & Reflect"):
    if entry.strip() == "":
        st.warning("Please write something before saving.")
    else:
        # --- AI Reflection ---
        prompt = f"""
        Summarize this journal entry, highlight main emotions and themes, and provide a gentle reflection:
        {entry}
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            ai_reflection = response['choices'][0]['message']['content']
        except Exception as e:
            ai_reflection = "AI reflection not available."
            st.error(f"Error calling OpenAI: {e}")

        # --- Save Entry ---
        new_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood": mood,
            "entry": entry,
            "ai_reflection": ai_reflection
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Entry saved!")
        st.text_area("AI Reflection", value=ai_reflection, height=150)

# --- Timeline / Look-back ---
st.header("Your Past Entries")
if len(df) == 0:
    st.info("No entries yet. Add your first journal entry above!")
else:
    selected_mood = st.selectbox("Filter by mood (optional)", ["All"] + df["mood"].unique().tolist())
    filtered_df = df if selected_mood == "All" else df[df["mood"] == selected_mood]

    for _, row in filtered_df[::-1].iterrows():
        st.subheader(f"{row['timestamp']} | {row['mood']}")
        st.write(row["entry"])
        with st.expander("AI Reflection"):
            st.write(row["ai_reflection"])

# --- Export as RTF ---
st.header("Export Your Journal")
if st.button("Download as RTF"):
    rtf_content = "{\\rtf1\\ansi\\deff0\n"
    for _, row in df.iterrows():
        rtf_content += f"\\b Date: \\b0 {row['timestamp']}\\line\n"
        rtf_content += f"\\b Mood: \\b0 {row['mood']}\\line\n"
        rtf_content += f"{row['entry']}\\line\n"
        rtf_content += f"AI Reflection: {row['ai_reflection']}\\line\\line\n"
    rtf_content += "}"

    st.download_button(
        label="Download Journal",
        data=rtf_content,
        file_name="my_journal.rtf",
        mime="application/rtf"
    )
