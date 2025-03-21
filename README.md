# Emotion Detector - EmotionAI

Emotion Detector is a web application that analyzes audio files or recordings to detect emotions like happiness, sadness, anger, and more. It uses machine learning to provide real-time emotion detection and redirects users to relevant support websites based on the detected emotion.

---

## Features

- **Real-Time Emotion Detection**: Analyze emotions from audio files or live recordings.
- **User-Friendly Interface**: Simple and intuitive design.
- **Emotion-Based Redirection**: Redirects users to relevant websites (e.g., mental health resources for "sad" emotions).
- **Responsive Design**: Works on both desktop and mobile devices.

---

## Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Hugging Face's Wav2Vec2 model
- **Libraries**: Librosa, Torch, Transformers

---

## How to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/emotion-detector.git
   cd emotion-detector
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Start the Server:

bash
Copy
uvicorn app:app --reload
Access the Application:

Open your browser and go to http://127.0.0.1:8000.

How to Use
Home Page: Learn about the application and start detecting emotions.

Detect Emotion: Upload a .wav file or record your voice.

View Results: The detected emotion will be displayed, and you’ll be redirected to a relevant website.

Project Structure
Copy
emotion-detector/
├── app.py                  # FastAPI backend
├── model.py                # Emotion detection model
├── index.html              # Home page
├── detect_emotion.html     # Emotion detection page
├── style.css               # CSS for styling
├── script.js               # Frontend interactivity
├── recorder.js             # Audio recording
└── uploads/                # Stores uploaded audio files
