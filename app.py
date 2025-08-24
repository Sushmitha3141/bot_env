import os
import google.generativeai as genai
import pyttsx3
from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import nltk
import json
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Only download once if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

from langchain.memory import ConversationBufferMemory


# Load 3-class sentiment model
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Label mapping
labels = ['negative', 'neutral', 'positive']


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
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=api_key)
memory = ConversationBufferMemory(return_messages=True)


# File path
MEMORY_FILE = "user_memory.json"

def load_user_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"name": "User", "last_emotion": "", "last_message": ""}

def save_user_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


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
    # Preprocess
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        scores = outputs.logits[0]
        predicted_class = torch.argmax(scores).item()
    return labels[predicted_class]


def get_gemini_response(prompt):
    try:
        # Get conversation history as a string
        history = ""
        for msg in memory.chat_memory.messages:
            role = "User" if msg.type == "human" else "Bot"
            history += f"{role}: {msg.content}\n"

        system_instruction = (
            "You are Zappy, a kind, calm, and empathetic mental wellness chatbot. "
            "Always respond with warmth, encouragement, and emotional support. "
            "Avoid listing options. Just reply naturally and empathetically, like a caring friend.\n"
        )

        full_prompt = f"{system_instruction}{history}User: {prompt}\nBot:"


        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt)

        # Add messages to memory
        memory.chat_memory.add_user_message(prompt)
        memory.chat_memory.add_ai_message(response.text)

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
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Invalid request format'}), 400
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        speak_response = data.get('speak', False)

        # Load existing memory
        try:
            user_data = load_user_memory()
        except Exception as e:
            logger.error(f"Error loading user memory: {e}")
            user_data = {"name": "User", "last_emotion": "", "last_message": ""}

        # Detect emotion
        try:
            emotion = detect_emotion(user_message)
            logger.info(f"Detected emotion: {emotion}")
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            emotion = "neutral"

        # Gemini response with added personalization
        try:
            prompt = f"{user_data['name']} said: {user_message}\nPrevious message: {user_data['last_message']}\nRespond empathetically."
            response = get_gemini_response(prompt)
        except Exception as e:
            logger.error(f"Error getting Gemini response: {e}")
            response = "I'm sorry, I'm having trouble processing your message right now. Please try again in a moment."

        # Update and save memory
        try:
            user_data['last_message'] = user_message
            user_data['last_emotion'] = emotion
            save_user_memory(user_data)
        except Exception as e:
            logger.error(f"Error saving user memory: {e}")

        # Speak
        speech_successful = False
        if speak_response and tts_enabled:
            try:
                speech_successful = speak(response)
            except Exception as e:
                logger.error(f"Error in text-to-speech: {e}")

        return jsonify({
            'response': response,
            'emotion': emotion,
            'speech_successful': speech_successful,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in send_message: {e}")
        return jsonify({
            'error': 'An unexpected error occurred. Please try again.',
            'status': 'error'
        }), 500

@app.route('/speak_text', methods=['POST'])
def speak_text():
    """Endpoint to speak a given text"""
    try:
        if not request.is_json:
            return jsonify({'error': 'Invalid request format'}), 400
        
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        success = speak(text)
        return jsonify({
            'success': success,
            'status': 'success' if success else 'error'
        })
        
    except Exception as e:
        logger.error(f"Error in speak_text: {e}")
        return jsonify({
            'error': 'Failed to speak text',
            'status': 'error'
        }), 500

if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Start the Flask app
    app.run(debug=True)


@app.route('/nltk_test')
def nltk_test():
    test_text = "Hey Suzzz! You’re building an amazing mental wellness bot. Let's see if nltk is alive."
    from nltk.tokenize import sent_tokenize, word_tokenize
    
    try:
        sentences = sent_tokenize(test_text)
        words = word_tokenize(test_text)
        return jsonify({
            'text': test_text,
            'sentences': sentences,
            'words': words
        })
    except Exception as e:
        return jsonify({'error': str(e)})

