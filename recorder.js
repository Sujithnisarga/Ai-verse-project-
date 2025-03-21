let mediaRecorder;
let recordedChunks = [];

const recordBtn = document.getElementById('recordBtn');
const audioPlayback = document.getElementById('audioPlayback');
const recordControls = document.querySelector('.record-controls');
const deleteRecording = document.getElementById('deleteRecording');
const submitRecording = document.getElementById('submitRecording');
const statusIcon = document.getElementById('statusIcon');
const progressBar = document.getElementById('progress-bar');
const resultText = document.getElementById('resultText');

// Start/Stop Recording
recordBtn.addEventListener('click', async () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        recordBtn.textContent = '🎤 Start Recording';
        recordBtn.classList.remove('recording');
    } else {
        recordedChunks = [];
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            recordBtn.textContent = '⏹ Stop Recording';
            recordBtn.classList.add('recording');

            mediaRecorder.ondataavailable = (e) => recordedChunks.push(e.data);
            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, { type: 'audio/wav' });
                const audioURL = URL.createObjectURL(blob);
                audioPlayback.src = audioURL;
                audioPlayback.style.display = 'block';
                recordControls.style.display = 'flex';
            };
        } catch (error) {
            alert('Error accessing microphone. Please allow microphone access.');
            console.error('Microphone access error:', error);
        }
    }
});

// Delete Recording
deleteRecording.addEventListener('click', () => {
    audioPlayback.src = '';
    audioPlayback.style.display = 'none';
    recordControls.style.display = 'none';
    recordedChunks = [];
});

// Submit Recording
submitRecording.addEventListener('click', () => {
    if (recordedChunks.length === 0) {
        alert('No recording found. Please record your voice first.');
        return;
    }

    const blob = new Blob(recordedChunks, { type: 'audio/wav' });
    const file = new File([blob], 'recorded_audio.wav');
    const formData = new FormData();
    formData.append('file', file);

    // Reset UI
    statusIcon.textContent = '?';
    statusIcon.classList.remove('success');
    resultText.classList.remove('show');
    progressBar.style.width = '0%';

    // Simulate progress bar
    simulateProgressBar();

    // Send to server
    fetch('/upload', { method: 'POST', body: formData })
        .then((res) => res.json())
        .then((data) => {
            progressBar.style.width = '100%';
            statusIcon.textContent = '✔';
            statusIcon.classList.add('success');
            resultText.textContent = `Detected Emotion: ${data.emotion}`;
            resultText.classList.add('show');
        })
        .catch((error) => {
            console.error('Error uploading file:', error);
            alert('Failed to upload recording. Please try again.');
        });
});

// Simulate Progress Bar
function simulateProgressBar() {
    let width = 0;
    const interval = setInterval(() => {
        if (width >= 95) clearInterval(interval);
        else {
            width += 5;
            progressBar.style.width = width + '%';
        }
    }, 150);
}