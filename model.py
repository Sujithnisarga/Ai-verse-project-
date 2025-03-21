from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification
import librosa
import torch

# Use the correct model for emotion recognition
model_name = "r-f/wav2vec-english-speech-emotion-recognition"
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)

def predict_emotion(audio_path):
    # Fix file path issue
    audio, rate = librosa.load(audio_path, sr=16000)
    inputs = feature_extractor(audio, sampling_rate=rate, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        outputs = model(inputs.input_values)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)  # Apply softmax
        predicted_label = torch.argmax(predictions, dim=-1).item()
        emotion = model.config.id2label[predicted_label]

    return emotion

# Fix the file path using a raw string (r"...") or double backslashes
audio_path = "03-01-06-01-02-02-01.wav"

emotion = predict_emotion(audio_path)
print(f"Predicted emotion: {emotion}")






