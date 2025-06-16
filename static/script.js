function startWebcam() {
    fetch('/webcam/start')
        .then(res => res.json())
        .then(data => alert(data.message));
}

function stopWebcam() {
    fetch('/webcam/stop')
        .then(res => res.json())
        .then(data => alert(data.message));
}

// Update count every 2 seconds
setInterval(() => {
    fetch('/status')
        .then(res => res.json())
        .then(data => {
            document.getElementById('count').innerText = "EVs Detected: " + data.ev_count;
        });
}, 2000);
