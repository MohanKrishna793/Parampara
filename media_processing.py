import whisper
import streamlit as st
import tempfile
import os
from PIL import Image
import io
from deep_translator import GoogleTranslator
from config import LANGUAGES, UPLOAD_CONFIG
import speech_recognition as sr
from pydub import AudioSegment
import hashlib

class MediaProcessor:
    def __init__(self):
        self.whisper_model = None
        self.recognizer = sr.Recognizer()
        
    @st.cache_resource
    def load_whisper_model(_self, model_size="base"):
        """Load Whisper model for audio transcription"""
        try:
            if _self.whisper_model is None:
                _self.whisper_model = whisper.load_model(model_size)
            return _self.whisper_model
        except Exception as e:
            st.error(f"Error loading Whisper model: {e}")
            return None
            
    def transcribe_audio_whisper(self, audio_file, language=None):
        """Transcribe audio using Whisper"""
        try:
            model = self.load_whisper_model()
            if model is None:
                return None, "Failed to load Whisper model"
                
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_file.write(audio_file.getbuffer())
                temp_path = temp_file.name
                
            # Transcribe audio
            result = model.transcribe(temp_path, language=language)
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return result['text'], None
            
        except Exception as e:
            return None, f"Error transcribing audio: {e}"
            
    def transcribe_audio_sr(self, audio_file, language='hi-IN'):
        """Transcribe audio using SpeechRecognition (Google API)"""
        try:
            # Convert to wav if needed
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_file.write(audio_file.getbuffer())
                temp_path = temp_file.name
                
            # Load audio file
            audio = AudioSegment.from_file(temp_path)
            
            # Convert to wav format for speech recognition
            wav_path = temp_path.replace('.wav', '_converted.wav')
            audio.export(wav_path, format='wav')
            
            # Transcribe using speech recognition
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language=language)
                
            # Clean up temporary files
            os.unlink(temp_path)
            os.unlink(wav_path)
            
            return text, None
            
        except sr.UnknownValueError:
            return None, "Could not understand audio"
        except sr.RequestError as e:
            return None, f"Error with speech recognition service: {e}"
        except Exception as e:
            return None, f"Error transcribing audio: {e}"
            
    def process_image(self, image_file, max_size=(1920, 1080)):
        """Process and optimize image"""
        try:
            # Open image
            image = Image.open(image_file)
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
                
            # Resize if too large
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
            # Save optimized image
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            return output, None
            
        except Exception as e:
            return None, f"Error processing image: {e}"
            
    def extract_text_from_image(self, image_file):
        """Extract text from image using OCR (placeholder for future implementation)"""
        # This would use libraries like pytesseract or cloud OCR services
        # For now, returning placeholder
        return "OCR not implemented yet", None
        
    def translate_text(self, text, source_lang='auto', target_lang='en'):
        """Translate text using Google Translate"""
        try:
            if not text.strip():
                return text, None
                
            # Convert language codes if needed
            lang_map = {
                'hi': 'hi', 'bn': 'bn', 'ta': 'ta', 'te': 'te', 'mr': 'mr',
                'gu': 'gu', 'kn': 'kn', 'ml': 'ml', 'or': 'or', 'pa': 'pa',
                'as': 'as', 'ur': 'ur', 'en': 'en'
            }
            
            source_lang = lang_map.get(source_lang, source_lang)
            target_lang = lang_map.get(target_lang, target_lang)
            
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated = translator.translate(text)
            
            return translated, None
            
        except Exception as e:
            return text, f"Translation error: {e}"
            
    def detect_language(self, text):
        """Detect language of text"""
        try:
            from deep_translator import GoogleTranslator
            detected = GoogleTranslator(source='auto', target='en').translate(text)
            # This is a simplified approach - in practice, you'd use a proper language detection library
            return 'auto', None
        except Exception as e:
            return 'en', f"Language detection error: {e}"
            
    def validate_file_type(self, file, allowed_types):
        """Validate uploaded file type"""
        if file is None:
            return False, "No file uploaded"
            
        file_extension = file.name.split('.')[-1].lower()
        if file_extension not in allowed_types:
            return False, f"File type .{file_extension} not allowed. Allowed types: {', '.join(allowed_types)}"
            
        return True, "File type valid"
        
    def validate_file_size(self, file, max_size=None):
        """Validate file size"""
        if file is None:
            return False, "No file uploaded"
            
        if max_size is None:
            max_size = UPLOAD_CONFIG['MAX_FILE_SIZE']
            
        file_size = len(file.getbuffer())
        if file_size > max_size:
            max_size_mb = max_size / (1024 * 1024)
            current_size_mb = file_size / (1024 * 1024)
            return False, f"File size ({current_size_mb:.1f}MB) exceeds maximum allowed size ({max_size_mb:.1f}MB)"
            
        return True, f"File size valid ({file_size / (1024 * 1024):.1f}MB)"
        
    def get_file_hash(self, file):
        """Generate hash for file deduplication"""
        try:
            file_content = file.getbuffer()
            return hashlib.md5(file_content).hexdigest()
        except Exception as e:
            return None
            
    def process_video_thumbnail(self, video_file):
        """Extract thumbnail from video (placeholder)"""
        # This would use libraries like opencv-python or ffmpeg
        # For now, returning placeholder
        return None, "Video thumbnail extraction not implemented yet"
        
    def compress_audio(self, audio_file, target_bitrate='64k'):
        """Compress audio file"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file.write(audio_file.getbuffer())
                temp_path = temp_file.name
                
            # Load and compress audio
            audio = AudioSegment.from_file(temp_path)
            
            # Export with compression
            compressed_path = temp_path.replace('.mp3', '_compressed.mp3')
            audio.export(compressed_path, format='mp3', bitrate=target_bitrate)
            
            # Read compressed file
            with open(compressed_path, 'rb') as f:
                compressed_data = f.read()
                
            # Clean up
            os.unlink(temp_path)
            os.unlink(compressed_path)
            
            return io.BytesIO(compressed_data), None
            
        except Exception as e:
            return None, f"Error compressing audio: {e}"

# Global media processor instance
@st.cache_resource
def get_media_processor():
    """Get media processor instance"""
    return MediaProcessor()

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def get_language_code(language_name):
    """Get language code from language name"""
    for code, name in LANGUAGES.items():
        if name == language_name:
            return code
    return 'en'  # Default to English

def get_supported_languages_for_transcription():
    """Get list of languages supported for audio transcription"""
    return {
        'hi': 'Hindi',
        'bn': 'Bengali',
        'ta': 'Tamil',
        'te': 'Telugu',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'pa': 'Punjabi',
        'en': 'English'
    }