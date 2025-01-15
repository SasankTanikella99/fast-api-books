"""
Database Models Module

This module defines SQLAlchemy ORM models for the application.
It provides the database structure for books and users.

Author: Sasank Tanikella
Created: 01-14-2025
"""

from sqlalchemy import Column, Integer, String, Date
from .database_config import Base

class Book(Base):
    """
    SQLAlchemy model for books table.
    
    Attributes:
        id (int): Primary key for the book
        title (str): Book title, indexed for faster searches
        author (str): Name of the book's author
        published_date (Date): Publication date of the book
        summary (str): Book summary or description
        genre (str): Book's genre or category
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    published_date = Column(Date)
    summary = Column(String)
    genre = Column(String)

class User(Base):
    """
    SQLAlchemy model for users table.
    
    Attributes:
        id (int): Primary key for the user
        email (str): User's email address, unique and indexed
        password_hash (str): Hashed version of user's password
    
    Notes:
        - Email must be unique across all users
        - Password is stored as a hash for security
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
