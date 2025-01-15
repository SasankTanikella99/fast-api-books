"""
FastAPI Main Application Module

This module initializes and configures the FastAPI application with middleware, 
routes, and database connections. It serves as the entry point for the API service.

Author: Sasank Tanikella
Created: 01-14-2025
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import models
from .database_config import engine
from app.routes import bookRoutes, sseRoutes, userRoutes

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Book Management API",
    description="API for managing books with real-time updates using SSE",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
ALLOWED_ORIGINS = [
    "https://fast-api-books-vama.onrender.com",
    "http://localhost:8000",
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if os.getenv("ENV") == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(bookRoutes.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(userRoutes.router, prefix="/api/v1/user", tags=["User"])
app.include_router(sseRoutes.router, prefix="/api/v1/sse", tags=["SSE"])

# Serve static files if directory exists
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    """Serve the SSE test HTML page."""
    static_file = os.path.join(static_dir, 'sse_test.html')
    if os.path.exists(static_file):
        return FileResponse(static_file)
    return {"message": "Welcome to Book Management API"}

@app.get("/health", include_in_schema=False)
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}

# Add this if you want to run the app directly
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENV") != "production"
    )
