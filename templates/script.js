<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zappy - Mental Wellness Companion</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body>
    <div class="chat-container">
        <!-- Bubble background animations -->
        <div class="bubble" style="width: 80px; height: 80px; left: 10%;"></div>
        <div class="bubble" style="width: 40px; height: 40px; left: 25%; animation-delay: 2s;"></div>
        <div class="bubble" style="width: 60px; height: 60px; left: 60%; animation-delay: 4s;"></div>
        <div class="bubble" style="width: 50px; height: 50px; left: 80%; animation-delay: 1s;"></div>
        <div class="bubble" style="width: 70px; height: 70px; left: 40%; animation-delay: 3s;"></div>
        
        <div class="chat-header">
            <div class="logo">
                <i class="fas fa-bolt logo-icon"></i>
                <span>Zappy</span>
            </div>
            <div class="settings">
                <div class="toggle-container">
                    <label for="speechToggle">Auto-speak</label>
                    <label class="toggle">
                        <input type="checkbox" id="speechToggle">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="quick-actions">
                <div class="action-btn" data-message="How to manage anxiety">How to manage anxiety</div>
                <div class="action-btn" data-message="Help me sleep better">Help me sleep better</div>
                <div class="action-btn" data-message="Quick stress relief">Quick stress relief</div>
                <div class="action-btn" data-message="Positive affirmations">Positive affirmations</div>
                <div class="action-btn" data-message="Mindfulness exercises">Mindfulness exercises</div>
            </div>
            
            <div class="message bot-message">
                <span class="message-text">Hi, I'm Zappy! I'm here to support your mental wellness journey. How are you feeling today?</span>
                <i class="fas fa-volume-up speak-btn" onclick="speakMessage(this.parentElement)"></i>
            </div>
        </div>
        
        <button class="mood-button" id="moodButton">
            <i class="fas fa-smile-beam"></i>
        </button>
        
        <div class="mood-selector" id="moodSelector">
            <h3>How are you feeling?</h3>
            <div class="moods">
                <div class="mood" data-mood="Happy">
                    <span>😊</span>
                    <p>Happy</p>
                </div>
                <div class="mood" data-mood="Anxious">
                    <span>😰</span>
                    <p>Anxious</p>
                </div>
                <div class="mood" data-mood="Sad">
                    <span>😢</span>
                    <p>Sad</p>
                </div>
                <div class="mood" data-mood="Stressed">
                    <span>😫</span>
                    <p>Stressed</p>
                </div>
                <div class="mood" data-mood="Calm">
                    <span>😌</span>
                    <p>Calm</p>
                </div>
                <div class="mood" data-mood="Tired">
                    <span>😴</span>
                    <p>Tired</p>
                </div>
                <div class="mood" data-mood="Confused">
                    <span>🤔</span>
                    <p>Confused</p>
                </div>
                <div class="mood" data-mood="Excited">
                    <span>🤩</span>
                    <p>Excited</p>
                </div>
            </div>
        </div>
        
        <div class="breathing-guide" id="breathingGuide">
            <div class="breathing-circle">
                <div class="breathing-inner">
                    <i class="fas fa-lungs"></i>
                </div>
            </div>
            <div class="breathing-text">
                <p>Breathe in... hold... breathe out...</p>
                <p>Focus on your breathing</p>
            </div>
            <button class="close-breathing" id="closeBreathing">
                I feel better now
            </button>
        </div>
        
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="Share what's on your mind..." autocomplete="off">
            <button id="sendButton">
                <i class="fas fa-paper-plane"></i>
                <span>Send</span>
            </button>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>