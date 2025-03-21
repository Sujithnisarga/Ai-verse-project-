from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from model import predict_emotion
import logging
import os
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files (CSS, JS) from the root directory
app.mount("/static", StaticFiles(directory="."), name="static")

# app.py
emotion_urls = {
    "sad": "https://www.mentalhealth.gov/",
    "happy": "https://www.happiness.com/",
    "angry": "https://www.anger-management.org/",
    "neutral": "https://www.calm.com/",
    "fear": "https://www.anxietycanada.com/",
    "disgust": "https://www.psychologytoday.com/",
    "surprise": "https://www.ted.com/topics/surprise",
}

# Serve HTML files directly
@app.get("/")
async def index():
    return FileResponse("index.html")

@app.get("/detect_emotion")
async def detect_emotion():
    return FileResponse("detect_emotion.html")

@app.get("/about")
async def about():
    return FileResponse("about.html")

# Redirect /detect_emotion to /detect_emotion.html
@app.get("/detect_emotion/")
async def redirect_detect_emotion():
    return RedirectResponse(url="/detect_emotion.html")

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
        redirect_url = emotion_urls.get(emotion, "https://www.google.com")  # Default URL if emotion not found
        return JSONResponse(content={"emotion": emotion, "redirect_url": redirect_url})
    except Exception as e:
        logger.error(f"Error predicting emotion: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
