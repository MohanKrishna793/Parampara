#!/usr/bin/env python3
"""
Quick start script for Parampara application.
This script helps users get started quickly with minimal setup.
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """Check if basic requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        return False
    
    # Check if MySQL is available
    if not shutil.which('mysql'):
        print("⚠️ MySQL client not found. Please install MySQL")
        print("On Ubuntu/Debian: sudo apt-get install mysql-client")
        print("On macOS: brew install mysql")
        
    print("✅ Basic requirements check passed")
    return True

def setup_environment():
    """Set up the development environment"""
    print("\n🛠️ Setting up environment...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
            print("⚠️ Please edit .env file with your database credentials")
        else:
            print("❌ .env.example file not found")
            return False
    
    # Install dependencies
    if not run_command('pip install -r requirements.txt', 'Installing dependencies'):
        return False
    
    return True

def setup_database():
    """Set up the database"""
    print("\n🗄️ Setting up database...")
    
    if not run_command('python setup_database.py', 'Setting up database'):
        print("❌ Database setup failed. Please check your database configuration in .env")
        return False
    
    return True

def run_tests():
    """Run installation tests"""
    print("\n🧪 Running tests...")
    
    if not run_command('python test_installation.py', 'Running installation tests'):
        print("❌ Some tests failed. Please check the output above")
        return False
    
    return True

def start_application():
    """Start the Streamlit application"""
    print("\n🚀 Starting Parampara application...")
    print("The application will open in your browser at: http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    
    try:
        subprocess.run(['streamlit', 'run', 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")

def main():
    """Main quick start function"""
    print("🪔 Parampara Quick Start")
    print("=" * 50)
    
    if not check_requirements():
        sys.exit(1)
    
    if not setup_environment():
        sys.exit(1)
    
    # Ask user if they want to set up database
    response = input("\n❓ Do you want to set up the database now? (y/n): ").lower()
    if response in ['y', 'yes']:
        if not setup_database():
            print("❌ Database setup failed. You can run 'python setup_database.py' later")
    
    # Ask user if they want to run tests
    response = input("\n❓ Do you want to run installation tests? (y/n): ").lower()
    if response in ['y', 'yes']:
        if not run_tests():
            print("❌ Some tests failed, but you can still try running the application")
    
    # Ask user if they want to start the application
    response = input("\n❓ Do you want to start the application now? (y/n): ").lower()
    if response in ['y', 'yes']:
        start_application()
    else:
        print("\n🎉 Setup completed!")
        print("To start the application later, run: streamlit run app.py")

if __name__ == "__main__":
    main()