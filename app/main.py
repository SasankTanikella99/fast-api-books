"""
FastAPI Main Application Module

This module initializes and configures the FastAPI application with middleware, 
routes, and database connections. It serves as the entry point for the API service.

Author: Sasank Tanikella
Created: 01-14-2025
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database_config import engine
from app.routes import bookRoutes, sseRoutes, userRoutes
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bookRoutes.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(userRoutes.router, prefix="/api/v1/user", tags=["User"])
app.include_router(sseRoutes.router, prefix="/api/v1/sse", tags=["SSE"])

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/sse_test.html')


