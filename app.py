from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.transcription_routes import router_transcription
from routes.chat_routes import router_chat
from routes.pdf_routes import router_pdf
import uvicorn

app = FastAPI(
        title = "My FastAPI for AI Chat with audio and video",
        description = "A REST API built with FastAPI for AI Chat with audio and video.",
        version = "1.0.0",
    )


# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Set up routes
app.include_router(router_transcription, prefix="/ai/transcriptions", tags=["transcriptions"])
app.include_router(router_pdf, prefix="/pdf", tags=["pdf"])
app.include_router(router_chat, prefix="/chat", tags=["chat"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)