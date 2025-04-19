from fastapi import FastAPI, UploadFile, File, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
import os

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Azure config (replace with your keys and endpoints)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "<your-openai-endpoint>")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "<your-openai-key>")
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "<your-speech-key>")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "<your-speech-region>")

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Call Azure OpenAI API
    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "user", "content": request.message}],
        "max_tokens": 100
    }
    response = requests.post(
        f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-03-15-preview",
        headers=headers,
        json=data
    )
    result = response.json()
    answer = result["choices"][0]["message"]["content"] if "choices" in result else "Error: No response"
    return ChatResponse(response=answer)

@app.post("/speech-to-text")
def speech_to_text(audio: UploadFile = File(...)):
    # Call Azure Speech-to-Text
    speech_url = f"https://{AZURE_SPEECH_REGION}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
        "Content-Type": "audio/wav"
    }
    audio_bytes = audio.file.read()
    response = requests.post(speech_url, headers=headers, data=audio_bytes)
    result = response.json()
    text = result.get("DisplayText", "")
    return {"text": text}

@app.post("/text-to-speech")
def text_to_speech(text: str = Form(...)):
    # Call Azure Text-to-Speech
    tts_url = f"https://{AZURE_SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-32kbitrate-mono-mp3"
    }
    ssml = f"""
    <speak version='1.0' xml:lang='en-US'>
        <voice xml:lang='en-US' xml:gender='Female' name='en-US-JennyNeural'>
            {text}
        </voice>
    </speak>
    """
    response = requests.post(tts_url, headers=headers, data=ssml.encode('utf-8'))
    return Response(content=response.content, media_type="audio/mpeg")