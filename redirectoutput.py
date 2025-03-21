from flask import Flask, redirect, url_for, flash, render_template_string
from flask import session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Define URLs for each emotion
emotion_urls = {
    "happy": "https://www.goodnewsnetwork.org/",
    "sad": "https://www.talkspace.com/",
    "angry": "https://www.headspace.com/meditation",
    "neutral": "https://www.wikipedia.org/",
    "fearful": "https://www.calm.com/",
    "surprised": "https://www.nationalgeographic.com/",
    "disgusted": "https://www.helpguide.org/"
}

# HTML template to display flash message and redirect
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Emotion Response</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 50px;
            text-align: center;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: inline-block;
        }
        h2 {
            color: #333;
        }
        a {
            text-decoration: none;
            color: #007BFF;
            font-size: 18px;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <h2>{{ messages[0] }}</h2>
                <p>Redirecting you now...</p>
            {% endif %}
        {% endwith %}
    </div>
    <script>
        setTimeout(function() {
            window.location.href = "{{ url }}";
        }, 5000);  // Redirect after 5 seconds
    </script>
</body>
</html>
"""

@app.route('/emotion/<emotion>')
def redirect_emotion(emotion):
    emotion_lower = emotion.lower()
    url = emotion_urls.get(emotion_lower)
    
    if url:
        # Flash the message before redirection
        flash(f"I understand you feel {emotion_lower.capitalize()}. This might help you: {url}")
        return render_template_string(html_template, url=url)
    else:
        flash("Emotion not recognized. Please try again.")
        return redirect(url_for('index'))

@app.route('/')
def index():
    return "Welcome! Use /emotion/<emotion> to test emotion-based redirection."

if __name__ == '__main__':
    app.run(debug=True)
