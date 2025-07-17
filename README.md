# 🪔 Parampara - Preserving Indian Culture

**Parampara** is an open-source, AI-powered, multilingual web application built with Streamlit that aims to crowdsource and preserve Indian regional culture—including food, festivals, rituals, and oral histories—especially from rural and semi-connected areas.

## 🌟 Features

### ✅ Core Features
- **🔐 User Authentication**: Secure MySQL-based user registration and login
- **📍 Location Capture**: Browser geolocation or manual location input
- **🧭 Category Selection**: Choose between Food and Culture categories
- **🎙️ Media Type Selection**: Support for Text, Audio, Image, and Video contributions
- **📤 File Upload**: Support for files up to 5GB with validation
- **🤖 AI Processing**: Automatic audio transcription using Whisper
- **🌍 Multilingual Support**: 13+ Indian languages supported
- **📊 Analytics**: Real-time statistics and contribution tracking

### 🎯 Purpose
To empower citizens from every Indian state and region to digitally preserve their native culture and languages, one contribution at a time—whether it's a grandmother's recipe, a forgotten festival, or a traditional ritual.

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, MySQL
- **Frontend**: Streamlit
- **AI/ML**: OpenAI Whisper (audio transcription), Google Translate
- **Media Processing**: Pillow (images), pydub (audio)
- **Authentication**: bcrypt for password hashing
- **Database**: MySQL with proper schema design

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- MySQL 8.0 or higher
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/parampara.git
cd parampara
```

### Step 2: Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up MySQL Database
1. Create a MySQL database named `parampara`
2. Create a MySQL user with appropriate permissions

```sql
CREATE DATABASE parampara CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'parampara_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON parampara.* TO 'parampara_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 5: Configure Environment Variables
1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your database credentials:
```env
DB_HOST=localhost
DB_USER=parampara_user
DB_PASSWORD=your_password
DB_NAME=parampara
DB_PORT=3306
SECRET_KEY=your-secret-key-here
```

### Step 6: Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🗄️ Database Schema

The application uses three main tables:

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### User Locations Table
```sql
CREATE TABLE user_locations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    address TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Submissions Table
```sql
CREATE TABLE submissions (
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
);
```

## 🚀 Usage

### Step-by-Step User Journey

1. **🔐 Authentication**
   - Register a new account or login with existing credentials
   - Secure password hashing with bcrypt

2. **📍 Location Capture**
   - Allow browser geolocation or enter location manually
   - Location data helps map cultural practices to regions

3. **🧭 Category Selection**
   - Choose between Food (🍲) and Culture (🪔) categories
   - Can select one or both categories

4. **🎙️ Media Type Selection**
   - Text: Written stories, recipes, descriptions
   - Audio: Voice recordings, songs, oral histories
   - Image: Photos of food, festivals, cultural practices
   - Video: Video recordings of traditions and practices

5. **📤 Upload & Submit**
   - Add title, description, and media files
   - Automatic audio transcription for audio files
   - File validation and size checking (up to 5GB)
   - Multilingual support for content

## 🌍 Supported Languages

- हिंदी (Hindi)
- বাংলা (Bengali)
- தமிழ் (Tamil)
- తెలుగు (Telugu)
- మరాఠీ (Marathi)
- ગુજરાતી (Gujarati)
- ಕನ್ನಡ (Kannada)
- മലയാളം (Malayalam)
- ଓଡ଼ିଆ (Odia)
- ਪੰਜਾਬੀ (Punjabi)
- অসমীয়া (Assamese)
- اردو (Urdu)
- English

## 📁 Project Structure

```
parampara/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── database.py           # Database operations
├── media_processing.py   # Media processing utilities
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables example
├── README.md            # This file
├── uploads/             # File upload directory
│   ├── images/
│   ├── audio/
│   ├── videos/
│   └── documents/
└── regions.json         # Indian states/regions data
```

## 🔧 Configuration

### File Upload Limits
- Maximum file size: 5GB
- Supported image formats: JPG, PNG, GIF, BMP
- Supported audio formats: MP3, WAV, M4A, FLAC, OGG
- Supported video formats: MP4, AVI, MOV, WMV, FLV, WEBM

### AI Features
- **Audio Transcription**: Uses OpenAI Whisper for multilingual transcription
- **Translation**: Google Translate API for language translation
- **Text Processing**: Support for Indic languages

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

#### Option 1: Streamlit Cloud
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Configure environment variables
4. Deploy

#### Option 2: Docker (Future Enhancement)
```bash
docker build -t parampara .
docker run -p 8501:8501 parampara
```

#### Option 3: Self-Hosted
1. Set up a Linux server
2. Install Python, MySQL, and dependencies
3. Configure reverse proxy (nginx)
4. Set up SSL certificates
5. Run with process manager (PM2, systemd)

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Areas for Contribution
- 🌐 Additional language support
- 🎨 UI/UX improvements
- 🔊 Enhanced audio processing
- 📱 Mobile responsiveness
- 🔍 Search and discovery features
- 📊 Advanced analytics
- 🌏 Geographic visualization

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI Whisper** for audio transcription
- **Streamlit** for the web framework
- **Google Translate** for multilingual support
- **Indian cultural communities** for inspiration
- **Contributors** who help preserve our heritage

## 📞 Support

For support, questions, or suggestions:
- 📧 Email: support@parampara.org
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/parampara/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/parampara/discussions)

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Basic authentication and user management
- ✅ File upload and media processing
- ✅ Audio transcription
- ✅ Multilingual support

### Phase 2 (Planned)
- 🔄 Advanced search and filtering
- 📱 Mobile app development
- 🌍 Geographic visualization
- 🤖 AI-powered content categorization

### Phase 3 (Future)
- 🎥 Live streaming support
- 🏆 Gamification and rewards
- 🔗 API for third-party integrations
- 📊 Advanced analytics dashboard

---

**Made with ❤️ for preserving Indian culture and heritage**