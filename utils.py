import json
import pandas as pd
import os

# Translation
from googletrans import Translator
from indic_transliteration.sanscript import transliterate, DEVANAGARI, ITRANS

translator = Translator()
LANGUAGES = {
    'hi': 'Hindi', 'bn': 'Bengali', 'ta': 'Tamil', 'te': 'Telugu', 'mr': 'Marathi',
    'gu': 'Gujarati', 'kn': 'Kannada', 'ml': 'Malayalam', 'or': 'Odia',
    'pa': 'Punjabi', 'en': 'English'
}

def translate_text(text, src, dest):
    try:
        result = translator.translate(text, src=src, dest=dest)
        return result.text
    except Exception:
        return text

def get_lang_display(code):
    return LANGUAGES.get(code, code)

# Audio-to-text (using Whisper)
import whisper
import tempfile

def audio_to_text(audio_file):
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio.flush()
            model = whisper.load_model("base")
            result = model.transcribe(temp_audio.name)
            return result['text']
    except Exception:
        return ""

# Database: Firebase or CSV
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    cred = credentials.Certificate("path-to-your-firebase-key.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception:
    db = None  # For offline mode

DATA_FILE = "parampara_data.csv"

def save_submission(data):
    if db:
        db.collection("submissions").add(data)
    else:
        df = pd.DataFrame([data])
        header = not os.path.exists(DATA_FILE)
        df.to_csv(DATA_FILE, mode='a', header=header, index=False)

def export_data():
    if db:
        docs = db.collection("submissions").stream()
        data = [doc.to_dict() for doc in docs]
        return pd.DataFrame(data).to_csv(index=False).encode()
    else:
        with open(DATA_FILE, "rb") as f:
            return f.read()

# Optional: NLP preprocessing
def preprocess_text(text):
    # Example: transliterate to Devanagari
    return transliterate(text, ITRANS, DEVANAGARI)
