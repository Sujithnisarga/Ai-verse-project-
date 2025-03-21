document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.getElementById('fileInput');
    const statusIcon = document.getElementById('statusIcon');
    const progressBar = document.getElementById('progress-bar');
    const resultText = document.getElementById('resultText');

    // Trigger file input on button click
    uploadBtn.addEventListener('click', () => fileInput.click());

    // Handle file upload
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (!file || !file.name.endsWith('.wav')) {
            alert('Please upload a .wav file.');
            return;
        }

        // Reset UI
        statusIcon.textContent = '?';
        statusIcon.classList.remove('success');
        resultText.classList.remove('show');
        progressBar.style.width = '0%';

        // Simulate progress bar for 2-3 minutes
        simulateProgressBar(150);  // 150 seconds = 2.5 minutes

        // Prepare form data
        const formData = new FormData();
        formData.append('file', file);

        // Send to server
        fetch('/upload', {
            method: 'POST',
            body: formData,
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                progressBar.style.width = '100%';
                statusIcon.textContent = '✔';
                statusIcon.classList.add('success');
                resultText.textContent = `Detected Emotion: ${data.emotion}`;
                resultText.classList.add('show');
            })
            .catch((error) => {
                console.error('Error uploading file:', error);
                alert('Failed to upload file. Please try again.');
            });
    });

    // Simulate Progress Bar for a given duration (in seconds)
    function simulateProgressBar(duration) {
        let width = 0;
        const interval = setInterval(() => {
            if (width >= 95) clearInterval(interval);
            else {
                width += 5;
                progressBar.style.width = width + '%';
            }
        }, (duration * 1000) / 20);  // Adjust interval for smooth progress
    }
});