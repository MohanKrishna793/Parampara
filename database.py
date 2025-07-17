import mysql.connector
from mysql.connector import Error
import bcrypt
import streamlit as st
from datetime import datetime
import os
from config import DB_CONFIG, UPLOAD_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except Error as e:
            st.error(f"Database connection error: {e}")
            return False
            
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            
    def create_tables(self):
        """Create all required tables"""
        try:
            # Users table
            users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # User locations table
            locations_table = """
            CREATE TABLE IF NOT EXISTS user_locations (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                latitude FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                address TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            
            # Submissions table
            submissions_table = """
            CREATE TABLE IF NOT EXISTS submissions (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                category ENUM('Food', 'Culture') NOT NULL,
                content_type ENUM('Text', 'Audio', 'Image', 'Video') NOT NULL,
                file_path TEXT,
                file_size BIGINT,
                transcript TEXT,
                language VARCHAR(50),
                region VARCHAR(50),
                location_lat FLOAT,
                location_lng FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            
            self.cursor.execute(users_table)
            self.cursor.execute(locations_table)
            self.cursor.execute(submissions_table)
            self.connection.commit()
            return True
            
        except Error as e:
            st.error(f"Error creating tables: {e}")
            return False
            
    def hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
    def verify_password(self, password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        
    def register_user(self, username, email, password):
        """Register a new user"""
        try:
            # Check if user already exists
            self.cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            if self.cursor.fetchone():
                return False, "Username or email already exists"
                
            # Hash password and insert user
            password_hash = self.hash_password(password)
            query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (username, email, password_hash))
            self.connection.commit()
            
            return True, "User registered successfully"
            
        except Error as e:
            return False, f"Registration error: {e}"
            
    def login_user(self, username, password):
        """Authenticate user login"""
        try:
            query = "SELECT id, username, email, password_hash FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            user = self.cursor.fetchone()
            
            if user and self.verify_password(password, user['password_hash']):
                return True, user
            else:
                return False, "Invalid username or password"
                
        except Error as e:
            return False, f"Login error: {e}"
            
    def save_location(self, user_id, latitude, longitude, address=None):
        """Save user location"""
        try:
            query = """
            INSERT INTO user_locations (user_id, latitude, longitude, address) 
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (user_id, latitude, longitude, address))
            self.connection.commit()
            return True
            
        except Error as e:
            st.error(f"Error saving location: {e}")
            return False
            
    def get_user_location(self, user_id):
        """Get user's latest location"""
        try:
            query = """
            SELECT latitude, longitude, address, recorded_at 
            FROM user_locations 
            WHERE user_id = %s 
            ORDER BY recorded_at DESC 
            LIMIT 1
            """
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()
            
        except Error as e:
            st.error(f"Error getting location: {e}")
            return None
            
    def save_submission(self, user_id, title, description, category, content_type, 
                       file_path=None, file_size=None, transcript=None, language=None, 
                       region=None, location_lat=None, location_lng=None):
        """Save user submission"""
        try:
            query = """
            INSERT INTO submissions (user_id, title, description, category, content_type, 
                                   file_path, file_size, transcript, language, region, 
                                   location_lat, location_lng) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (user_id, title, description, category, content_type, 
                     file_path, file_size, transcript, language, region, 
                     location_lat, location_lng)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            return True, self.cursor.lastrowid
            
        except Error as e:
            st.error(f"Error saving submission: {e}")
            return False, None
            
    def get_user_submissions(self, user_id):
        """Get all submissions by a user"""
        try:
            query = """
            SELECT * FROM submissions 
            WHERE user_id = %s 
            ORDER BY created_at DESC
            """
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchall()
            
        except Error as e:
            st.error(f"Error getting submissions: {e}")
            return []
            
    def get_submission_stats(self):
        """Get submission statistics"""
        try:
            stats = {}
            
            # Total submissions
            self.cursor.execute("SELECT COUNT(*) as total FROM submissions")
            stats['total_submissions'] = self.cursor.fetchone()['total']
            
            # Submissions by category
            self.cursor.execute("""
                SELECT category, COUNT(*) as count 
                FROM submissions 
                GROUP BY category
            """)
            stats['by_category'] = {row['category']: row['count'] for row in self.cursor.fetchall()}
            
            # Submissions by content type
            self.cursor.execute("""
                SELECT content_type, COUNT(*) as count 
                FROM submissions 
                GROUP BY content_type
            """)
            stats['by_content_type'] = {row['content_type']: row['count'] for row in self.cursor.fetchall()}
            
            # Submissions by region
            self.cursor.execute("""
                SELECT region, COUNT(*) as count 
                FROM submissions 
                WHERE region IS NOT NULL
                GROUP BY region 
                ORDER BY count DESC 
                LIMIT 10
            """)
            stats['by_region'] = {row['region']: row['count'] for row in self.cursor.fetchall()}
            
            return stats
            
        except Error as e:
            st.error(f"Error getting stats: {e}")
            return {}

# Database instance
@st.cache_resource
def get_database():
    """Get database instance with connection pooling"""
    db = Database()
    if db.connect():
        db.create_tables()
        return db
    return None

def ensure_upload_directory():
    """Ensure upload directory exists"""
    upload_dir = UPLOAD_CONFIG['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    # Create subdirectories for different media types
    for media_type in ['images', 'audio', 'videos', 'documents']:
        subdir = os.path.join(upload_dir, media_type)
        if not os.path.exists(subdir):
            os.makedirs(subdir)

def save_uploaded_file(uploaded_file, media_type, user_id):
    """Save uploaded file to disk"""
    ensure_upload_directory()
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{user_id}_{timestamp}_{uploaded_file.name}"
    
    # Determine subdirectory based on media type
    subdir_map = {
        'Image': 'images',
        'Audio': 'audio', 
        'Video': 'videos',
        'Text': 'documents'
    }
    
    subdir = subdir_map.get(media_type, 'documents')
    file_path = os.path.join(UPLOAD_CONFIG['UPLOAD_FOLDER'], subdir, filename)
    
    try:
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return file_path, uploaded_file.size
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None, 0