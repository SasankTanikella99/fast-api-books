"""
Database Configuration Module

This module handles SQLAlchemy database configuration and session management.
It provides database connection settings, session handling, and dependency injection
for database operations.

Author: Sasank Tanikella
Created: 01-14-2025
"""

import os
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

# Database URL configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Handle Heroku PostgreSQL URL format
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    # Fallback for local development
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_PATH = os.path.join(BASE_DIR, "books (2).db")
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Database engine configuration
engine_args = {
    "poolclass": QueuePool,
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 1800,
    "echo": False
}

# Add SQLite-specific arguments only for SQLite
if DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

# Database engine configuration
engine = create_engine(DATABASE_URL, **engine_args)

# Session configuration
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Base class for SQLAlchemy models
Base = declarative_base()

def get_db_connection() -> Generator[Session, None, None]:
    """
    Dependency injection function for database sessions.
    
    Creates a new database session for each request and ensures
    proper cleanup after the request is completed.

    Yields:
        Session: SQLAlchemy database session

    Notes:
        - Sessions are automatically closed after use
        - Implements proper error handling
        - Ensures connection cleanup
    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    
    Provides a context-managed database session for use in
    non-FastAPI contexts (background tasks, scripts, etc.).

    Yields:
        Session: SQLAlchemy database session

    Example:
        with get_db_context() as db:
            result = db.query(Model).all()
    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

def init_db() -> None:
    """
    Initialize database tables and initial data.
    
    Creates all defined tables in the database and can be used
    to populate initial data if needed.

    Raises:
        SQLAlchemyError: If database initialization fails
    """
    Base.metadata.create_all(bind=engine)

def check_database_connection() -> bool:
    """
    Check if database connection is working.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        # Log the error in production
        return False
