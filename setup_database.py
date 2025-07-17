#!/usr/bin/env python3
"""
Database setup script for Parampara application.
This script creates the necessary database tables and initial configuration.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'parampara'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

def create_database():
    """Create the database if it doesn't exist"""
    config = get_db_config()
    db_name = config.pop('database')
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Database '{db_name}' created successfully")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    return True

def create_tables():
    """Create all required tables"""
    config = get_db_config()
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Users table
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_username (username),
            INDEX idx_email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
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
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user_id (user_id),
            INDEX idx_location (latitude, longitude)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
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
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user_id (user_id),
            INDEX idx_category (category),
            INDEX idx_content_type (content_type),
            INDEX idx_language (language),
            INDEX idx_region (region),
            INDEX idx_created_at (created_at),
            FULLTEXT idx_title_description (title, description)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        # Create tables
        cursor.execute(users_table)
        print("✅ Users table created successfully")
        
        cursor.execute(locations_table)
        print("✅ User locations table created successfully")
        
        cursor.execute(submissions_table)
        print("✅ Submissions table created successfully")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        return False

def create_upload_directories():
    """Create upload directories"""
    base_dir = 'uploads'
    subdirs = ['images', 'audio', 'videos', 'documents']
    
    try:
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            print(f"✅ Created upload directory: {base_dir}")
        
        for subdir in subdirs:
            path = os.path.join(base_dir, subdir)
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"✅ Created subdirectory: {path}")
                
        return True
        
    except Exception as e:
        print(f"❌ Error creating upload directories: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    config = get_db_config()
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Test basic query
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ Database connection successful. MySQL version: {version[0]}")
        
        # Test tables exist
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        expected_tables = ['users', 'user_locations', 'submissions']
        
        existing_tables = [table[0] for table in tables]
        for table in expected_tables:
            if table in existing_tables:
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' missing")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🪔 Parampara Database Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found. Please copy .env.example to .env and configure your database settings.")
        sys.exit(1)
    
    # Create database
    print("\n1. Creating database...")
    if not create_database():
        print("❌ Failed to create database. Please check your database settings.")
        sys.exit(1)
    
    # Create tables
    print("\n2. Creating tables...")
    if not create_tables():
        print("❌ Failed to create tables. Please check your database permissions.")
        sys.exit(1)
    
    # Create upload directories
    print("\n3. Creating upload directories...")
    if not create_upload_directories():
        print("❌ Failed to create upload directories. Please check file permissions.")
        sys.exit(1)
    
    # Test connection
    print("\n4. Testing database connection...")
    if not test_database_connection():
        print("❌ Database connection test failed.")
        sys.exit(1)
    
    print("\n🎉 Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the application: streamlit run app.py")
    print("2. Open your browser and go to: http://localhost:8501")
    print("3. Register a new account and start contributing!")

if __name__ == "__main__":
    main()