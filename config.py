import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'parampara'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# File Upload Configuration
UPLOAD_CONFIG = {
    'MAX_FILE_SIZE': 5 * 1024 * 1024 * 1024,  # 5GB
    'UPLOAD_FOLDER': 'uploads',
    'ALLOWED_EXTENSIONS': {
        'image': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
        'audio': ['mp3', 'wav', 'm4a', 'flac', 'ogg'],
        'video': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm']
    }
}

# Application Configuration
APP_CONFIG = {
    'TITLE': 'Parampara - Preserving Indian Culture',
    'DESCRIPTION': 'Crowdsourcing platform for Indian regional culture preservation',
    'VERSION': '1.0.0',
    'SECRET_KEY': os.getenv('SECRET_KEY', 'parampara-secret-key-2024'),
    'SESSION_TIMEOUT': 3600  # 1 hour
}

# Supported Languages
LANGUAGES = {
    'hi': 'हिंदी (Hindi)',
    'bn': 'বাংলা (Bengali)', 
    'ta': 'தமிழ் (Tamil)',
    'te': 'తెలుగు (Telugu)',
    'mr': 'मराठी (Marathi)',
    'gu': 'ગુજરાતી (Gujarati)',
    'kn': 'ಕನ್ನಡ (Kannada)',
    'ml': 'മലയാളം (Malayalam)',
    'or': 'ଓଡ଼ିଆ (Odia)',
    'pa': 'ਪੰਜਾਬੀ (Punjabi)',
    'as': 'অসমীয়া (Assamese)',
    'ur': 'اردو (Urdu)',
    'en': 'English'
}

# Indian States and Regions
REGIONS = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

# Content Categories
CATEGORIES = {
    'Food': {
        'icon': '🍲',
        'description': 'Traditional recipes, cooking methods, and food culture',
        'examples': ['Regional recipes', 'Cooking techniques', 'Festival foods', 'Street food']
    },
    'Culture': {
        'icon': '🪔',
        'description': 'Festivals, rituals, traditions, and cultural practices',
        'examples': ['Festivals', 'Rituals', 'Folk songs', 'Traditional arts', 'Oral histories']
    }
}

# Media Types
MEDIA_TYPES = {
    'Text': {
        'icon': '📝',
        'description': 'Written stories, recipes, and descriptions'
    },
    'Audio': {
        'icon': '🎤',
        'description': 'Voice recordings, songs, and oral histories'
    },
    'Image': {
        'icon': '📷',
        'description': 'Photos of food, festivals, and cultural practices'
    },
    'Video': {
        'icon': '📹',
        'description': 'Video recordings of traditions and practices'
    }
}