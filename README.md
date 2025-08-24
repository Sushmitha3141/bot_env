# Zappy - Mental Wellness Companion

A compassionate AI chatbot designed to support mental wellness through empathetic conversations, emotion detection, and text-to-speech capabilities.

## 🚀 Features

- **Empathetic Conversations**: Powered by Google's Gemini AI for natural, supportive dialogue
- **Emotion Detection**: Real-time sentiment analysis to personalize responses
- **Text-to-Speech**: Voice output for accessibility and comfort
- **Conversation Memory**: Maintains context across sessions using LangChain
- **Beautiful UI**: Modern, calming interface designed for mental wellness
- **Quick Actions**: Pre-defined mental health prompts for easy access
- **Mood Tracking**: Visual mood selection and tracking
- **Loading States**: Smooth user experience with visual feedback
- **Error Handling**: Graceful error handling and user feedback

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bot_env
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy the `.env.example` file to `.env`
   - Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5000`

## 🔒 Security Improvements

### ✅ Completed
- **Environment Variables**: API keys moved to `.env` file
- **Input Validation**: All user inputs are validated
- **Error Handling**: Comprehensive error handling with user feedback
- **Loading States**: Visual feedback during API calls
- **Input Sanitization**: Prevents XSS and injection attacks

### 🔄 In Progress
- User authentication and session management
- Data encryption for sensitive conversations
- Rate limiting to prevent abuse

## 📁 Project Structure

```
bot_env/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (not in git)
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── user_memory.json     # User conversation memory
├── templates/
│   └── index1.html     # Main chat interface
└── venv/               # Virtual environment
```

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **AI**: Google Gemini API
- **NLP**: Hugging Face Transformers (sentiment analysis)
- **Memory**: LangChain ConversationBufferMemory
- **Frontend**: HTML5, CSS3, JavaScript
- **TTS**: pyttsx3 (text-to-speech)

## 🎯 Usage

1. **Start a conversation**: Type your message and press Enter
2. **Use quick actions**: Click on pre-defined mental health prompts
3. **Select your mood**: Use the mood button to express how you're feeling
4. **Enable speech**: Toggle the auto-speak feature for voice output
5. **Manual speech**: Click the speaker icon on any bot message

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `FLASK_ENV`: Development/production environment
- `FLASK_DEBUG`: Enable/disable debug mode

### Customization
- Modify the bot's personality in `app.py` (system_instruction)
- Adjust TTS settings in the speak() function
- Customize the UI colors in `templates/index1.html`

## 🚨 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your `.env` file contains the correct API key
   - Check that the API key is valid and has proper permissions

2. **Text-to-Speech Not Working**
   - Install system audio drivers
   - On Linux, install `espeak`: `sudo apt-get install espeak`
   - On Windows, ensure Windows Media Foundation is enabled

3. **Model Loading Issues**
   - Ensure you have sufficient RAM (at least 4GB recommended)
   - Check internet connection for model downloads
   - Clear browser cache if UI issues persist

4. **Port Already in Use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is designed for general mental wellness support and is not a substitute for professional mental health care. If you're experiencing a mental health crisis, please contact a mental health professional or emergency services immediately.

## 🔮 Future Enhancements

- [ ] User authentication and profiles
- [ ] Crisis detection and emergency resources
- [ ] Mood tracking with visual charts
- [ ] Breathing exercises and meditation guides
- [ ] Sleep hygiene recommendations
- [ ] Gratitude journaling feature
- [ ] Voice input capabilities
- [ ] Dark mode support
- [ ] Mobile app version
- [ ] Multi-language support 