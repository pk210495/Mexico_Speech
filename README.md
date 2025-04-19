# Mexico Speech - AI Conversational Chatbot

This repository contains a full-stack AI conversational chatbot application with speech capabilities.

## Project Structure

```
├── frontend/           # React frontend application
└── backend/            # FastAPI backend application
```

## Setup & Installation

### Backend
1. Navigate to the backend directory
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up your environment variables in a `.env` file

### Frontend
1. Navigate to the frontend directory
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
AZURE_OPENAI_ENDPOINT=your_openai_endpoint
AZURE_OPENAI_KEY=your_openai_key
AZURE_SPEECH_KEY=your_speech_key
AZURE_SPEECH_REGION=your_speech_region
```

## Running the Application

### Backend
1. Navigate to the backend directory
2. Run: `uvicorn main:app --reload`

### Frontend
1. Navigate to the frontend directory
2. Run: `npm start`

The application will be available at `http://localhost:3000`