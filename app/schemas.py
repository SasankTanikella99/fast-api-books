"""
Pydantic Schemas Module

This module defines Pydantic models for request/response validation
and serialization. It provides data validation and serialization
for the API endpoints.

Author: Sasank Tanikella
Created: 01-14-2025
"""

from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class BookBase(BaseModel):
    """
    Base schema for book data.
    
    Attributes:
        title (str): Book title
        author (str): Book author
        published_date (date): Publication date
        summary (str): Book description
        genre (str): Book genre
    """
    title: str
    author: str
    published_date: date
    summary: str
    genre: str

class BookCreate(BookBase):
    """Schema for creating new books. Inherits all fields from BookBase."""
    pass

class Book(BookBase):
    """
    Complete book schema including database ID.
    
    Extends BookBase to include:
        id (int): Unique identifier from database
    """
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    """
    JWT token schema.
    
    Attributes:
        access_token (str): JWT token string
        token_type (str): Type of token (usually 'bearer')
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    JWT token payload schema.
    
    Attributes:
        email (Optional[str]): User's email if present
    """
    email: Optional[str] = None

class UserLogin(BaseModel):
    """
    User login credentials schema.
    
    Attributes:
        email (str): User's email address
        password (str): User's password
    """
    email: EmailStr
    password: str

class UserBase(BaseModel):
    """
    Base user schema.
    
    Attributes:
        email (str): User's email address
    """
    email: EmailStr

class UserCreate(UserBase):
    """
    Schema for creating new users.
    
    Extends UserBase to include:
        password (str): User's password
    """
    password: str

class User(UserBase):
    """
    Complete user schema including database ID.
    
    Extends UserBase to include:
        id (int): Unique identifier from database
    """
    id: int

    class Config:
        from_attributes = True
