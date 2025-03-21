from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification
import librosa
import torch
from collections import Counter

# Load model and feature extractor
model_name = "r-f/wav2vec-english-speech-emotion-recognition"
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)

def predict_emotion(audio_path, runs=10):
    try:
        # Load and normalize the audio file
        audio, rate = librosa.load(audio_path, sr=16000)
        audio = librosa.util.normalize(audio)

        # Extract features
        inputs = feature_extractor(audio, sampling_rate=rate, return_tensors="pt", padding=True)

        emotion_votes = []

        # Run emotion detection multiple times for accuracy
        for _ in range(runs):
            with torch.no_grad():
                outputs = model(inputs.input_values)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1).squeeze().tolist()
                emotion_scores = {model.config.id2label[i]: predictions[i] for i in range(len(predictions))}
                top_emotion = max(emotion_scores, key=emotion_scores.get)
                emotion_votes.append(top_emotion)

        # Get the most voted emotion
        most_voted = Counter(emotion_votes).most_common(1)[0][0]
        return most_voted

    except Exception as e:
        print(f"Error in predict_emotion: {e}")
        raise