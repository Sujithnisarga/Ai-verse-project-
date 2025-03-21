let mediaRecorder;
let recordedChunks = [];
const recordBtn = document.getElementById('recordBtn');
const recordedAudio = document.getElementById('recorded-audio');
const recordedAudioContainer = document.getElementById('recorded-audio-container');
const deleteBtn = document.getElementById('delete-recording');
const submitRecordingBtn = document.getElementById('submit-recording');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const progressContainer = document.getElementById('progress-container');
const progressBar = document.getElementById('progress-bar');
const emotionResult = document.getElementById('emotion-result');
const resultContainer = document.getElementById('result-container');

// Start / stop recording
recordBtn.addEventListener('click', async () => {
    if (!mediaRecorder || mediaRecorder.state === 'inactive') {
        recordedChunks = [];
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) recordedChunks.push(e.data);
        };
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(recordedChunks, { type: 'audio/wav' });
            const audioURL = URL.createObjectURL(audioBlob);
            recordedAudio.src = audioURL;
            recordedAudioContainer.style.display = 'block';
            submitRecordingBtn.audioBlob = audioBlob;
        };
        mediaRecorder.start();
        recordBtn.textContent = '⏹ Stop Recording';
    } else {
        mediaRecorder.stop();
        recordBtn.textContent = '🎤 Use Microphone';
    }
});

// Delete recorded audio
deleteBtn.addEventListener('click', () => {
    recordedChunks = [];
    recordedAudio.src = '';
    recordedAudioContainer.style.display = 'none';
});

// Submit recorded audio
submitRecordingBtn.addEventListener('click', () => {
    if (submitRecordingBtn.audioBlob) {
        sendAudio(submitRecordingBtn.audioBlob);
    }
});

// Upload file & detect
uploadBtn.addEventListener('click', () => {
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a WAV file.');
        return;
    }
    sendAudio(file);
});

// Function to send audio blob or file to backend
function sendAudio(audioBlob) {
    resultContainer.style.display = 'none';
    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';

    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.wav');

    // Animate progress bar simulation
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 10;
        progressBar.style.width = `${progress}%`;
        if (progress >= 100) {
            clearInterval(progressInterval);
        }
    }, 200);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            progressBar.style.width = '100%';
            resultContainer.style.display = 'block';
            emotionResult.textContent = data.emotion;
        })
        .catch(error => {
            console.error(error);
            alert('Error detecting emotion.');
        });
}
