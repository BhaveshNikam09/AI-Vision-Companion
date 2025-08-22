import os
import httpx
import logging
from dotenv import load_dotenv

# --- Step 1: Setup basic logging ---
# This will print INFO level messages and above to your console.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("🚀 Script starting...")

# --- Load Environment Variables ---
load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
# NEW URL for testing
# Workaround URL
API_URL = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"

# --- Step 2: Log the variables to verify them ---
logging.info(f"Using API URL: {API_URL}")

if HF_API_TOKEN:
    # IMPORTANT: Never log the actual token value for security reasons!
    logging.info("✅ Hugging Face API token loaded successfully.")
else:
    logging.warning("⚠️ Hugging Face API token not found. Check your .env file.")


def get_image_description(image_bytes: bytes) -> str:
    """
    Sends image data to Hugging Face API and gets a description.
    """
    if not HF_API_TOKEN:
        return "Error: Hugging Face API token is not set."

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    try:
        logging.info(f"Sending {len(image_bytes)} bytes to the API...")
        response = httpx.post(API_URL, headers=headers, content=image_bytes, timeout=30.0)
        
        logging.info(f"Received response with status code: {response.status_code}")
        response.raise_for_status() # Raise an exception for bad responses (4xx or 5xx)
        
        result = response.json()
        
        if result and isinstance(result, list) and 'generated_text' in result[0]:
            description = result[0]['generated_text']
            logging.info(f"✅ Success! Description: {description}")
            return description
        else:
            logging.error(f"Unexpected API response format: {result}")
            return "Error: Could not parse the image description."

    except httpx.HTTPStatusError as e:
        # --- Step 3: Log detailed error information ---
        logging.error("--- HTTP Error Details ---")
        logging.error(f"Status Code: {e.response.status_code}")
        logging.error(f"Reason: {e.response.reason_phrase}")
        logging.error(f"Response Body: {e.response.text}")
        logging.error("--------------------------")
        return "Error: The image analysis service failed."
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        return "Error: Could not get image description."


if __name__ == '__main__':
    image_path = "images/abc.jpg"
    logging.info(f"Attempting to open image at: {image_path}")
    
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
        logging.info("✅ Image file opened and read successfully.")
        
        description = get_image_description(image_data)
        print(f"\nFinal Description: {description}")

    except FileNotFoundError:
        logging.error(f"❌ Critical Error: The image file was not found at '{image_path}'.")
        logging.error("Please make sure you have a folder named 'images' and a file named 'abc.jpg' inside it.")
        print(f"\nFinal Description: Error: Image file not found.")