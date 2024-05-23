from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.transcription_routes import router_transcription
from routes.chat_routes import router_chat
from routes.pdf_routes import router_pdf
from routes.user_routes import router as router_user
from routes.source_routes import router as router_source
from routes.content_routes import router as router_content
from routes.access_routes import router as router_access
from routes.user_access_routes import router as router_user_access

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


# Routes media and files
app.include_router(router_transcription, prefix="/ai/transcriptions", tags=["transcriptions"])
app.include_router(router_pdf, prefix="/pdf", tags=["pdf"])
app.include_router(router_chat, prefix="/chat", tags=["chat"])

# Include CRUD routes
app.include_router(router_user, prefix="/users", tags=["users"])
app.include_router(router_source, prefix="/sources", tags=["sources"])
app.include_router(router_content, prefix="/contents", tags=["contents"])
app.include_router(router_access, prefix="/accesses", tags=["accesses"])
app.include_router(router_user_access, prefix="/user_accesses", tags=["user_accesses"])

# Create database tables (optional, use migrations in production)
#Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)