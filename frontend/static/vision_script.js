// Get references to all the HTML elements we need
const imageInput = document.getElementById("imageInput");
const processButton = document.getElementById("processButton");
const statusElement = document.getElementById("status");
const resultBox = document.getElementById("resultBox");
const descriptionResult = document.getElementById("descriptionResult");
const audioPlayback = document.getElementById("audioPlayback");
const replayButton = document.getElementById("replayButton"); // New replay button

// The URL of your FastAPI backend
const API_ENDPOINT = "http://127.0.0.1:8000/describe-and-speak";

// Listen for clicks on the main process button
processButton.addEventListener("click", async () => {
    const file = imageInput.files[0];
    if (!file) {
        alert("Please select an image file first.");
        return;
    }

    // --- Better Loading State ---
    statusElement.textContent = "Uploading and analyzing image...";
    resultBox.classList.add("hidden"); 
    replayButton.classList.add("hidden"); // Hide replay button during new request
    processButton.disabled = true;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(API_ENDPOINT, {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "An unknown error occurred on the server.");
        }
        
        // --- Success! Update the UI ---
        descriptionResult.textContent = data.description;
        audioPlayback.src = data.audioUrl;
        audioPlayback.play();
        
        statusElement.textContent = "Done!";
        resultBox.classList.remove("hidden");
        replayButton.classList.remove("hidden"); // Show the replay button

    } catch (error) {
        console.error("Error during API call:", error);
        statusElement.textContent = `Error: ${error.message}`;
    } finally {
        processButton.disabled = false;
    }
});

// --- Add event listener for the new Replay Button ---
replayButton.addEventListener('click', () => {
    if (audioPlayback.src) {
        audioPlayback.currentTime = 0; // Rewind to the start
        audioPlayback.play();
    }
});