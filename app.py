import streamlit as st
import time
from datetime import datetime
import os
import json

# Import custom modules
from config import *
from database import get_database, save_uploaded_file
from media_processing import get_media_processor, format_file_size, get_language_code

# Page configuration
st.set_page_config(
    page_title=APP_CONFIG['TITLE'],
    page_icon="🪔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'auth'
    if 'location_captured' not in st.session_state:
        st.session_state.location_captured = False
    if 'selected_categories' not in st.session_state:
        st.session_state.selected_categories = []
    if 'selected_media_type' not in st.session_state:
        st.session_state.selected_media_type = None
    if 'user_location' not in st.session_state:
        st.session_state.user_location = None

def show_header():
    """Display application header"""
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1>🪔 Parampara</h1>
            <p style="font-size: 1.2em; color: #666; margin-bottom: 2rem;">
                Preserving Indian Culture, One Story at a Time
            </p>
        </div>
    """, unsafe_allow_html=True)

def show_progress_bar(current_step):
    """Show progress bar for the multi-step process"""
    steps = ['🔐 Authentication', '📍 Location', '🧭 Category', '🎙️ Media Type', '📤 Upload']
    step_map = {
        'auth': 0,
        'location': 1,
        'category': 2,
        'media_type': 3,
        'upload': 4
    }
    
    current_index = step_map.get(current_step, 0)
    progress = (current_index + 1) / len(steps)
    
    st.progress(progress)
    
    # Show current step
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"**Step {current_index + 1} of {len(steps)}: {steps[current_index]}**")

def authentication_page():
    """Handle user authentication (login/register)"""
    st.subheader("🔐 Welcome to Parampara")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_btn = st.form_submit_button("Login", use_container_width=True)
            
            if login_btn:
                if username and password:
                    db = get_database()
                    if db:
                        success, result = db.login_user(username, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.user = result
                            st.session_state.current_step = 'location'
                            st.success("Login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(result)
                    else:
                        st.error("Database connection failed")
                else:
                    st.error("Please enter both username and password")
    
    with tab2:
        st.markdown("### Create New Account")
        with st.form("register_form"):
            new_username = st.text_input("Username", placeholder="Choose a username")
            new_email = st.text_input("Email", placeholder="Enter your email address")
            new_password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            register_btn = st.form_submit_button("Register", use_container_width=True)
            
            if register_btn:
                if new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        db = get_database()
                        if db:
                            success, result = db.register_user(new_username, new_email, new_password)
                            if success:
                                st.success("Registration successful! Please login.")
                            else:
                                st.error(result)
                        else:
                            st.error("Database connection failed")
                else:
                    st.error("Please fill in all fields")

def location_capture_page():
    """Handle location capture after login"""
    st.subheader("📍 Location Capture")
    
    st.markdown("""
        <div style="background-color: #f0f8ff; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <h4>🙏 Welcome to Parampara!</h4>
            <p>You're helping us preserve Indian traditions and culture. Your location helps us understand regional diversity and cultural patterns across India.</p>
            <p><strong>Why we need your location:</strong></p>
            <ul>
                <li>🗺️ Map cultural practices to specific regions</li>
                <li>📊 Understand regional diversity in traditions</li>
                <li>🔍 Help researchers study cultural patterns</li>
                <li>🌍 Create a comprehensive cultural map of India</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("📍 Allow Location Access", use_container_width=True):
            # In a real implementation, this would trigger browser geolocation
            # For now, we'll use a manual input as fallback
            st.session_state.location_captured = True
            st.success("Location access granted!")
            
    with col2:
        if st.button("📝 Enter Location Manually", use_container_width=True):
            st.session_state.show_manual_location = True
    
    # Manual location input
    if st.session_state.get('show_manual_location', False):
        st.markdown("### Enter Your Location Manually")
        with st.form("manual_location_form"):
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Latitude", value=28.6139, format="%.6f")
            with col2:
                longitude = st.number_input("Longitude", value=77.2090, format="%.6f")
            
            region = st.selectbox("Select Your State/Region", REGIONS)
            city = st.text_input("City/District", placeholder="Enter your city or district")
            
            if st.form_submit_button("Save Location"):
                db = get_database()
                if db:
                    address = f"{city}, {region}" if city else region
                    if db.save_location(st.session_state.user['id'], latitude, longitude, address):
                        st.session_state.user_location = {
                            'latitude': latitude,
                            'longitude': longitude,
                            'address': address
                        }
                        st.session_state.location_captured = True
                        st.success("Location saved successfully!")
                    else:
                        st.error("Failed to save location")
    
    # JavaScript for geolocation (this would work in a real browser environment)
    if st.session_state.get('location_captured', False):
        st.markdown("### ✅ Location Captured Successfully!")
        if st.button("Next: Select Category", use_container_width=True):
            st.session_state.current_step = 'category'
            st.rerun()

def category_selection_page():
    """Handle category selection"""
    st.subheader("🧭 Choose Your Contribution Category")
    
    st.markdown("Select one or both categories you'd like to contribute to:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        food_selected = st.checkbox("Food", value='Food' in st.session_state.selected_categories)
        
        st.markdown(f"""
            <div style="border: 2px solid {'#4CAF50' if food_selected else '#ddd'}; 
                        border-radius: 1rem; padding: 1rem; margin: 1rem 0; 
                        background-color: {'#f8fff8' if food_selected else '#f9f9f9'};">
                <div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">
                    {CATEGORIES['Food']['icon']}
                </div>
                <h3 style="text-align: center; margin-bottom: 1rem;">Food</h3>
                <p>{CATEGORIES['Food']['description']}</p>
                <p><strong>Examples:</strong></p>
                <ul>
                    {"".join(f"<li>{example}</li>" for example in CATEGORIES['Food']['examples'])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        culture_selected = st.checkbox("Culture", value='Culture' in st.session_state.selected_categories)
        
        st.markdown(f"""
            <div style="border: 2px solid {'#4CAF50' if culture_selected else '#ddd'}; 
                        border-radius: 1rem; padding: 1rem; margin: 1rem 0; 
                        background-color: {'#f8fff8' if culture_selected else '#f9f9f9'};">
                <div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">
                    {CATEGORIES['Culture']['icon']}
                </div>
                <h3 style="text-align: center; margin-bottom: 1rem;">Culture</h3>
                <p>{CATEGORIES['Culture']['description']}</p>
                <p><strong>Examples:</strong></p>
                <ul>
                    {"".join(f"<li>{example}</li>" for example in CATEGORIES['Culture']['examples'])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    # Update selected categories
    selected_categories = []
    if food_selected:
        selected_categories.append('Food')
    if culture_selected:
        selected_categories.append('Culture')
    
    st.session_state.selected_categories = selected_categories
    
    if selected_categories:
        st.success(f"Selected: {', '.join(selected_categories)}")
        if st.button("Next: Choose Media Type", use_container_width=True):
            st.session_state.current_step = 'media_type'
            st.rerun()
    else:
        st.warning("Please select at least one category to continue.")

def media_type_selection_page():
    """Handle media type selection"""
    st.subheader("🎙️ Choose Your Media Type")
    
    st.markdown("Select the type of content you want to contribute:")
    
    # Create a 2x2 grid for media types
    col1, col2 = st.columns(2)
    
    media_types = list(MEDIA_TYPES.keys())
    
    for i, media_type in enumerate(media_types):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            if st.button(f"{MEDIA_TYPES[media_type]['icon']} {media_type}", 
                        use_container_width=True,
                        key=f"media_{media_type}"):
                st.session_state.selected_media_type = media_type
                st.session_state.current_step = 'upload'
                st.rerun()
            
            st.markdown(f"""
                <div style="text-align: center; margin-bottom: 1rem; padding: 0.5rem;">
                    <small>{MEDIA_TYPES[media_type]['description']}</small>
                </div>
            """, unsafe_allow_html=True)

def upload_page():
    """Handle file upload and submission"""
    st.subheader("📤 Upload Your Contribution")
    
    # Show selected options
    st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <p><strong>Selected Categories:</strong> {', '.join(st.session_state.selected_categories)}</p>
            <p><strong>Media Type:</strong> {st.session_state.selected_media_type}</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("upload_form"):
        # Basic information
        st.markdown("### 📝 Basic Information")
        title = st.text_input("Title*", placeholder="Enter a descriptive title for your contribution")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category*", st.session_state.selected_categories)
        with col2:
            language = st.selectbox("Language*", list(LANGUAGES.values()))
        
        description = st.text_area(
            "Description*", 
            placeholder="Describe your contribution in detail. Include cultural context, regional significance, or personal stories.",
            height=150
        )
        
        # File upload section
        st.markdown("### 📁 File Upload")
        media_type = st.session_state.selected_media_type
        
        uploaded_file = None
        if media_type == 'Text':
            st.info("For text contributions, please provide detailed description above.")
        elif media_type == 'Image':
            uploaded_file = st.file_uploader(
                "Upload Image", 
                type=UPLOAD_CONFIG['ALLOWED_EXTENSIONS']['image'],
                help="Supported formats: JPG, PNG, GIF, BMP"
            )
        elif media_type == 'Audio':
            uploaded_file = st.file_uploader(
                "Upload Audio", 
                type=UPLOAD_CONFIG['ALLOWED_EXTENSIONS']['audio'],
                help="Supported formats: MP3, WAV, M4A, FLAC, OGG"
            )
        elif media_type == 'Video':
            uploaded_file = st.file_uploader(
                "Upload Video", 
                type=UPLOAD_CONFIG['ALLOWED_EXTENSIONS']['video'],
                help="Supported formats: MP4, AVI, MOV, WMV, FLV, WEBM"
            )
        
        # File validation
        if uploaded_file:
            file_size = len(uploaded_file.getbuffer())
            st.info(f"File size: {format_file_size(file_size)}")
            
            if file_size > UPLOAD_CONFIG['MAX_FILE_SIZE']:
                st.error(f"File size exceeds maximum allowed size of {format_file_size(UPLOAD_CONFIG['MAX_FILE_SIZE'])}")
        
        # Additional options
        st.markdown("### ⚙️ Additional Options")
        
        col1, col2 = st.columns(2)
        with col1:
            region = st.selectbox("Region/State", REGIONS, 
                                help="Select the region this contribution is from")
        with col2:
            auto_transcribe = st.checkbox("Auto-transcribe audio", 
                                        value=True if media_type == 'Audio' else False,
                                        disabled=media_type != 'Audio')
        
        # Submit button
        submit_btn = st.form_submit_button("🚀 Submit Contribution", use_container_width=True)
        
        if submit_btn:
            if not title or not description:
                st.error("Please fill in all required fields (Title and Description)")
            else:
                process_submission(title, description, category, media_type, language, 
                                region, uploaded_file, auto_transcribe)

def process_submission(title, description, category, media_type, language, 
                      region, uploaded_file, auto_transcribe):
    """Process and save the submission"""
    
    with st.spinner("Processing your contribution..."):
        db = get_database()
        if not db:
            st.error("Database connection failed")
            return
        
        # Save uploaded file
        file_path = None
        file_size = 0
        transcript = None
        
        if uploaded_file:
            file_path, file_size = save_uploaded_file(uploaded_file, media_type, st.session_state.user['id'])
            if not file_path:
                st.error("Failed to save uploaded file")
                return
        
        # Process audio transcription
        if media_type == 'Audio' and uploaded_file and auto_transcribe:
            media_processor = get_media_processor()
            lang_code = get_language_code(language)
            
            # Try Whisper first, fallback to SpeechRecognition
            transcript, error = media_processor.transcribe_audio_whisper(uploaded_file, lang_code)
            if not transcript:
                transcript, error = media_processor.transcribe_audio_sr(uploaded_file, f"{lang_code}-IN")
            
            if transcript:
                st.success("Audio transcribed successfully!")
                with st.expander("View Transcript"):
                    st.text(transcript)
            elif error:
                st.warning(f"Transcription failed: {error}")
        
        # Get user location
        user_location = st.session_state.get('user_location')
        location_lat = user_location['latitude'] if user_location else None
        location_lng = user_location['longitude'] if user_location else None
        
        # Save to database
        success, submission_id = db.save_submission(
            user_id=st.session_state.user['id'],
            title=title,
            description=description,
            category=category,
            content_type=media_type,
            file_path=file_path,
            file_size=file_size,
            transcript=transcript,
            language=language,
            region=region,
            location_lat=location_lat,
            location_lng=location_lng
        )
        
        if success:
            st.success("🎉 Contribution submitted successfully!")
            st.balloons()
            
            # Show submission summary
            st.markdown("### 📋 Submission Summary")
            st.markdown(f"""
                - **ID:** {submission_id}
                - **Title:** {title}
                - **Category:** {category}
                - **Media Type:** {media_type}
                - **Language:** {language}
                - **Region:** {region}
                - **File Size:** {format_file_size(file_size) if file_size else 'N/A'}
                - **Submitted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """)
            
            # Reset for new submission
            if st.button("🔄 Submit Another Contribution"):
                st.session_state.current_step = 'category'
                st.session_state.selected_categories = []
                st.session_state.selected_media_type = None
                st.rerun()
                
        else:
            st.error("Failed to save submission to database")

def main():
    """Main application flow"""
    init_session_state()
    show_header()
    
    # Check authentication
    if not st.session_state.authenticated:
        authentication_page()
        return
    
    # Show progress bar
    show_progress_bar(st.session_state.current_step)
    
    # Route to appropriate page based on current step
    if st.session_state.current_step == 'location':
        location_capture_page()
    elif st.session_state.current_step == 'category':
        category_selection_page()
    elif st.session_state.current_step == 'media_type':
        media_type_selection_page()
    elif st.session_state.current_step == 'upload':
        upload_page()
    
    # Sidebar with user info and logout
    with st.sidebar:
        st.markdown("### 👤 User Information")
        st.markdown(f"**Username:** {st.session_state.user['username']}")
        st.markdown(f"**Email:** {st.session_state.user['email']}")
        
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.current_step = 'auth'
            st.rerun()
        
        # Show statistics
        st.markdown("### 📊 Statistics")
        db = get_database()
        if db:
            stats = db.get_submission_stats()
            st.metric("Total Contributions", stats.get('total_submissions', 0))
            
            if stats.get('by_category'):
                st.markdown("**By Category:**")
                for category, count in stats['by_category'].items():
                    st.markdown(f"- {category}: {count}")

if __name__ == "__main__":
    main()
