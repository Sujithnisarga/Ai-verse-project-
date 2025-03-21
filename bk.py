from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import logging

# Mock function for emotion prediction (replace with your actual model)
def predict_emotion(file_path: str, runs: int = 50) -> str:
    # Replace this with your actual emotion prediction logic
    # For now, it returns a random emotion from the list
    import random
    emotions = ["happy", "sad", "angry", "neutral", "fear", "disgust", "surprise"]
    return random.choice(emotions)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Serve static files (CSS, JS, images) from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Emotion to website mapping
emotion_links = {
    "happy": "https://www.ted.com/talks",  # Inspirational TED Talks
    "sad": "https://www.7cups.com",       # Emotional support
    "angry": "https://www.calm.com",      # Calming exercises
    "neutral": "https://www.wikipedia.org",  # Neutral information
    "fear": "https://www.helpguide.org",  # Overcoming fear
    "disgust": "https://www.mind.org.uk",  # Mental health support
    "surprise": "https://www.boredpanda.com"  # Fun and surprising content
}

# Serve HTML files
@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.get("/detect_emotion")
async def detect_emotion():
    return FileResponse("static/detect_emotion.html")

@app.get("/about")
async def about():
    return FileResponse("static/about.html")

# Redirect /detect_emotion to /detect_emotion.html
@app.get("/detect_emotion/")
async def redirect_detect_emotion():
    return RedirectResponse(url="/detect_emotion")

# Reject GET requests to /upload
@app.get("/upload")
async def upload_get():
    raise HTTPException(status_code=405, detail="Method Not Allowed")

# File upload endpoint
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    logger.info(f"Uploading file: {file.filename}")
    # Validate file type
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are allowed")

    # Save the uploaded file
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save file")

    # Predict emotion
    try:
        emotion = predict_emotion(file_path, runs=50)
        # Get the corresponding link for the predicted emotion
        link = emotion_links.get(emotion, "https://www.google.com")  # Default link
        message = f"I understand that you feel {emotion}. Maybe this might help you: {link}"
        return JSONResponse(content={"emotion": emotion, "message": message, "link": link})
    except Exception as e:
        logger.error(f"Error predicting emotion: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Endpoint to redirect to the actual website
@app.get("/redirect")
async def redirect_to_website(link: str = Query(..., description="The website URL to redirect to")):
    return RedirectResponse(url=link)

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
