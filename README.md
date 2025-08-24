# 🚀 AI Vision Companion

## Problem Statement
The AI Vision Companion is a web application designed to assist visually impaired users by providing real-time, audible descriptions of images. This project uses voice as a solution to make the digital world more accessible.

## Live Demo
(If you deploy your app, put the live URL here. Otherwise, you can link to your demo video.)

## Features
* **Image Recognition:** Users can upload any image.
* **AI-Powered Descriptions:** Google's Gemini API analyzes the image and generates a concise description.
* **High-Quality Narration:** The description is converted into natural-sounding speech using the Murf AI TTS API.
* **Polished UI:** A clean, simple, and user-friendly interface with a replay function.

## Tech Stack
* **Backend:** Python, FastAPI
* **Frontend:** HTML, CSS, JavaScript
* **Vision AI:** Google Gemini API
* **Voice AI:** Murf AI Text-to-Speech API

## Setup and Installation
To run this project locally:

1.  Clone the repository.
2.  Navigate to the `backend` folder: `cd backend`
3.  Create a `.env` file and add your `GEMINI_API_KEY` and `MURF_API_KEY`.
4.  Install the required Python packages: `pip install -r requirements.txt`
5.  Run the FastAPI server: `uvicorn app:app --reload`
6.  Open the `frontend/index.html` file in your browser.