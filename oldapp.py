import os
import google.generativeai as genai
import pyttsx3
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env


# Initialize Flask app
app = Flask(__name__)

# Initialize text-to-speech engine
try:
    engine = pyttsx3.init()
    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
    
    # Get available voices and set a voice
    voices = engine.getProperty('voices')
    # Use the first voice (index 0 for male voice, typically index 1 for female voice)
    if voices:
        engine.setProperty('voice', voices[0].id)
    
    tts_enabled = True
except Exception as e:
    print(f"Text-to-speech initialization failed: {e}")
    tts_enabled = False
    engine = None

# Configure Gemini API
# Replace with your actual API key
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

def speak(text):
    """Speak the provided text using the text-to-speech engine"""
    if tts_enabled and engine:
        try:
            print(f"Speaking: {text}")
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            return False
    return False

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "I'm sorry, I couldn't process your request at the moment. Try again later."



# Flask routes
@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    speak_response = request.json.get('speak', False)
    
    response = get_gemini_response(user_message)
    
    # If speech is requested and available, speak the response
    if speak_response and tts_enabled:
        speak(response)
    
    return jsonify({'response': response, 'speech_successful': speak_response and tts_enabled})

@app.route('/speak_text', methods=['POST'])
def speak_text():
    """Endpoint to speak a given text"""
    text = request.json.get('text', '')
    success = speak(text)
    return jsonify({'success': success})

if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Start the Flask app
    app.run(debug=True)