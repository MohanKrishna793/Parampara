#!/usr/bin/env python3
"""
Test script to verify Parampara installation and dependencies.
Run this script to check if all required packages are installed correctly.
"""

import sys
import importlib
import os
from pathlib import Path

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Please use Python 3.10 or higher.")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    print("\n📦 Testing package imports...")
    
    required_packages = [
        ('streamlit', 'Streamlit web framework'),
        ('mysql.connector', 'MySQL database connector'),
        ('bcrypt', 'Password hashing'),
        ('whisper', 'OpenAI Whisper for audio transcription'),
        ('speech_recognition', 'Speech recognition library'),
        ('pydub', 'Audio processing'),
        ('PIL', 'Pillow image processing'),
        ('pandas', 'Data manipulation'),
        ('dotenv', 'Environment variable management'),
        ('deep_translator', 'Translation services'),
        ('indic_transliteration', 'Indic language support')
    ]
    
    failed_imports = []
    
    for package, description in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} - {description}")
        except ImportError as e:
            print(f"❌ {package} - {description} (Error: {e})")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import {len(failed_imports)} packages: {', '.join(failed_imports)}")
        print("Please install missing packages using: pip install -r requirements.txt")
        return False
    else:
        print(f"\n✅ All {len(required_packages)} packages imported successfully!")
        return True

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'app.py',
        'config.py',
        'database.py',
        'media_processing.py',
        'requirements.txt',
        'setup_database.py',
        'regions.json',
        '.env.example'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (missing)")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} files: {', '.join(missing_files)}")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files found!")
        return True

def test_configuration():
    """Test configuration setup"""
    print("\n⚙️ Testing configuration...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Load and check environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
        missing_vars = []
        
        for var in required_vars:
            if os.getenv(var):
                print(f"✅ {var} is set")
            else:
                print(f"❌ {var} is not set")
                missing_vars.append(var)
        
        if missing_vars:
            print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
            return False
        else:
            print("\n✅ All required environment variables are set!")
            return True
    else:
        print("❌ .env file not found")
        print("Please copy .env.example to .env and configure your settings")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from database import get_database
        db = get_database()
        
        if db:
            print("✅ Database connection successful")
            
            # Test if tables exist
            try:
                stats = db.get_submission_stats()
                print("✅ Database tables are accessible")
                return True
            except Exception as e:
                print(f"❌ Database tables not found: {e}")
                print("Please run: python setup_database.py")
                return False
        else:
            print("❌ Database connection failed")
            print("Please check your database settings in .env file")
            return False
            
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_media_processing():
    """Test media processing capabilities"""
    print("\n🎵 Testing media processing...")
    
    try:
        from media_processing import get_media_processor
        processor = get_media_processor()
        
        if processor:
            print("✅ Media processor initialized")
            
            # Test Whisper model loading (this might take a while on first run)
            try:
                model = processor.load_whisper_model("base")
                if model:
                    print("✅ Whisper model loaded successfully")
                else:
                    print("❌ Failed to load Whisper model")
                    return False
            except Exception as e:
                print(f"⚠️ Whisper model loading failed: {e}")
                print("This is normal on first run - model will be downloaded when needed")
            
            return True
        else:
            print("❌ Media processor initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Media processing error: {e}")
        return False

def test_upload_directories():
    """Test upload directory structure"""
    print("\n📂 Testing upload directories...")
    
    base_dir = 'uploads'
    subdirs = ['images', 'audio', 'videos', 'documents']
    
    if not os.path.exists(base_dir):
        print(f"❌ Upload directory '{base_dir}' does not exist")
        print("Please run: python setup_database.py")
        return False
    
    print(f"✅ Upload directory '{base_dir}' exists")
    
    for subdir in subdirs:
        path = os.path.join(base_dir, subdir)
        if os.path.exists(path):
            print(f"✅ Subdirectory '{subdir}' exists")
        else:
            print(f"❌ Subdirectory '{subdir}' missing")
            return False
    
    return True

def main():
    """Main test function"""
    print("🪔 Parampara Installation Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_imports),
        ("File Structure", test_file_structure),
        ("Configuration", test_configuration),
        ("Upload Directories", test_upload_directories),
        ("Database Connection", test_database_connection),
        ("Media Processing", test_media_processing)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 All tests passed! Your Parampara installation is ready.")
        print("\nNext steps:")
        print("1. Run the application: streamlit run app.py")
        print("2. Open your browser and go to: http://localhost:8501")
        print("3. Register a new account and start contributing!")
    else:
        print(f"\n❌ {failed} tests failed. Please fix the issues above before running the application.")
        print("\nFor help, check the README.md file or visit the project repository.")
        sys.exit(1)

if __name__ == "__main__":
    main()