import os
import google.generativeai as genai
import pyttsx3
from flask import Flask, render_template, request, jsonify
from transformers import pipeline

# Load sentiment model once
sentiment_pipeline = pipeline("sentiment-analysis")

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
genai.configure(api_key="AIzaSyC9Y22Y0mWaX6QHstBUMqlzDxvY_5Injls")

chat_history = []
MAX_MESSAGES = 15  # store last 15 exchanges (adjust as needed)

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

def detect_emotion(text):
    result = sentiment_pipeline(text)[0]  # Get label and score
    label = result['label'].lower()  # 'POSITIVE' or 'NEGATIVE'

    if 'positive' in label:
        return 'positive'
    elif 'negative' in label:
        return 'negative'
    else:
        return 'neutral'


def get_gemini_response(prompt):
    try:
        # Create context from recent messages
        history_context = ""
        for pair in chat_history[-MAX_MESSAGES:]:
            history_context += f"User: {pair['user']}\nBot: {pair['bot']}\n"

        full_prompt = f"{history_context}User: {prompt}\nBot:"

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "I'm sorry, I couldn't process your request at the moment."


# Flask routes
@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    speak_response = request.json.get('speak', False)
    
    response = get_gemini_response(user_message)
    emotion = detect_emotion(user_message)
    print(f"Detected emotion: {emotion}")

    
    # If speech is requested and available, speak the response
    if speak_response and tts_enabled:
        speak(response)

    chat_history.append({'user': user_message, 'bot': response})
    if len(chat_history) > MAX_MESSAGES:
        chat_history.pop(0)

    
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