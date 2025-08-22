import os
import io
import base64
import httpx
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# --- 1. CONFIGURE API KEYS ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
if not MURF_API_KEY:
    raise ValueError("MURF_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)


# --- 2. INITIALIZE THE FASTAPI APP ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 3. HELPER FUNCTIONS for AI Services ---

def get_image_description_gemini(image_bytes: bytes) -> str | None:
    try:
        img = Image.open(io.BytesIO(image_bytes))
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = "Describe this image for a visually impaired person in one, clear sentence."
        print("Sending image to Gemini API...")
        response = model.generate_content([prompt, img])
        print("✅ Description received from Gemini.")
        return response.text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return None

def get_murf_audio_url(text: str) -> str | None:
    """
    Calls Murf API and returns the direct audio URL.
    """
    # Added a check for empty text from Gemini
    if not text or not text.strip():
        print("Error: Input text for Murf is empty. Skipping API call.")
        return None

    generate_url = "https://api.murf.ai/v1/speech/generate"
    headers = {'Content-Type': 'application/json', 'api-key': MURF_API_KEY}
    
    # Using the voiceId from your previous successful project
    payload = {
        "text": text,
        "voiceId": "en-US-charles",
        "format": "MP3",
        "quality": "high",
        "style": "conversational"
    }

    try:
        print(f"Sending text to Murf API: '{text}'")
        with httpx.Client() as client:
            response = client.post(generate_url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            response_data = response.json()
            audio_url = response_data.get("audioFile")

            if not audio_url:
                print(f"Error: Murf did not return an audioUrl. Full response: {response_data}")
                return None

            print(f"✅ Received audio URL: {audio_url}")
            return audio_url
    except Exception as e:
        print(f"An error occurred with the Murf API: {e}")
        return None


# --- 4. THE API ENDPOINT ---
@app.post("/describe-and-speak")
async def describe_and_speak(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    image_bytes = await file.read()
    
    description = get_image_description_gemini(image_bytes)
    if not description:
        raise HTTPException(status_code=500, detail="Failed to get image description from Gemini.")
        
    audio_url = get_murf_audio_url(description)
    
    if not audio_url:
        # This will be triggered if you are out of characters or another Murf error occurs
        print("Murf API failed. Sending fallback audio URL to frontend.")
        return {
            "description": description,
            "audioUrl": "/static/fallback.mp3" 
        }
        
    return {
        "description": description,
        "audioUrl": audio_url
    }

# --- 5. Root endpoint ---
@app.get("/")
def read_root():
    return {"message": "AI Vision Companion Backend is running!"}