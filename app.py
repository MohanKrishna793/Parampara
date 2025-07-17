import streamlit as st
import pandas as pd
from utils.translation import translate_text, get_lang_display
from utils.audio import audio_to_text
from utils.db import save_submission, export_data
from utils.nlp import preprocess_text  # optional
import json

# Load regions and languages
with open('assets/regions.json', 'r', encoding='utf-8') as f:
    regions = json.load(f)

LANGUAGES = {
    'hi': 'Hindi', 'bn': 'Bengali', 'ta': 'Tamil', 'te': 'Telugu', 'mr': 'Marathi',
    'gu': 'Gujarati', 'kn': 'Kannada', 'ml': 'Malayalam', 'or': 'Odia',
    'pa': 'Punjabi', 'en': 'English'
}

st.set_page_config(page_title="Parampara", layout="centered")
st.title("🪔 Parampara: Indian Food & Culture Corpus Collection Engine")

with st.form("submission_form"):
    region = st.selectbox("Select Region/State", regions)
    language = st.selectbox("Select Language", list(LANGUAGES.values()))
    recipe_name = st.text_input("Recipe/Tradition Name")
    description = st.text_area("Description (Story, Ritual, Ingredients)")
    image_file = st.file_uploader("Upload Image (Food or Tradition)", type=['jpg', 'jpeg', 'png'])
    audio_file = st.file_uploader("Upload Audio (or record voice)", type=['wav', 'mp3', 'm4a'])
    submit_btn = st.form_submit_button("Submit")

if submit_btn:
    lang_code = [k for k, v in LANGUAGES.items() if v == language][0]
    # Process audio (if uploaded)
    audio_text = ""
    if audio_file:
        audio_text = audio_to_text(audio_file)
        description = f"{description}\nAudio Transcript: {audio_text}"
    # NLP Preprocessing (optional)
    # description = preprocess_text(description)
    # Translate to English
    translated_desc = translate_text(description, lang_code, 'en')
    # Save to DB
    data = {
        "region": region,
        "language": language,
        "recipe_name": recipe_name,
        "description_native": description,
        "description_en": translated_desc,
        "image": image_file.getvalue() if image_file else None,
        "audio_text": audio_text,
        "geo": st.session_state.get("geo", "")  # If geo-tagging
    }
    save_submission(data)
    st.success("Thank you for your contribution! 🙏")

# Admin/Data Export
st.sidebar.header("Admin Tools")
if st.sidebar.button("Export Data"):
    export = export_data()
    st.sidebar.download_button("Download CSV", export, "parampara_data.csv", "text/csv")

# Gamification (Badges)
# Example: Show badge if >10 submissions (implement with user tracking)
if st.session_state.get('submissions', 0) > 10:
    st.sidebar.markdown("🏅 Frequent Contributor Badge!")

# Multilingual UI Demo
st.sidebar.selectbox("Interface Language", list(LANGUAGES.values()))
