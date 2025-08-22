// Get references to all the HTML elements we need
const imageInput = document.getElementById("imageInput");
const processButton = document.getElementById("processButton");
const statusElement = document.getElementById("status");
const resultBox = document.getElementById("resultBox");
const descriptionResult = document.getElementById("descriptionResult");
const audioPlayback = document.getElementById("audioPlayback");

// The URL of your FastAPI backend
const API_ENDPOINT = "http://127.0.0.1:8000/describe-and-speak";

// Listen for clicks on the button
processButton.addEventListener("click", async () => {
    // 1. Get the file from the input
    const file = imageInput.files[0];
    if (!file) {
        alert("Please select an image file first.");
        return;
    }

    // 2. Update UI to show "processing" state
    statusElement.textContent = "Processing... This may take a moment.";
    resultBox.classList.add("hidden"); // Hide previous results
    processButton.disabled = true;

    // 3. Create FormData and add the file to it
    const formData = new FormData();
    formData.append("file", file);

    // 4. Call the backend API
    try {
        const response = await fetch(API_ENDPOINT, {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            // If the server returns an error, display it
            throw new Error(data.detail || "An unknown error occurred on the server.");
        }
        
        // 5. Success! Update the UI with the results
        descriptionResult.textContent = data.description;
        audioPlayback.src = data.audioUrl;
        audioPlayback.play();
        
        statusElement.textContent = "Done!";
        resultBox.classList.remove("hidden"); // Show the result box

    } catch (error) {
        // 6. Handle any errors during the fetch
        console.error("Error during API call:", error);
        statusElement.textContent = `Error: ${error.message}`;
    } finally {
        // 7. Re-enable the button after the process is finished
        processButton.disabled = false;
    }
});