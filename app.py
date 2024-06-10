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
from routes.auth_routes import router_auth
from middleware import AuthMiddleware
from utils import ensure_admin_user
from configurations.config import engine, Base, SessionLocal
from starlette.requests import Request

import uvicorn

app = FastAPI(
        title = "My FastAPI for AI Chat with PDF, AUDIO and VIDEO",
        description = "A REST API built with FastAPI for AI Chat with PDF, AUDIO and VIDEO.",
        version = "1.0.1",
    )


# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = None
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Add authentication middleware
app.add_middleware(AuthMiddleware)


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

# Include authentication routes
app.include_router(router_auth, prefix="/auth", tags=["auth"])

# Create database tables (optional, use migrations in production)
Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    ensure_admin_user(db)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)