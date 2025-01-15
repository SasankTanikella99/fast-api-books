"""
Custom Exception Classes Module

This module defines custom HTTP exceptions for the application.
It provides structured error handling for book operations, authentication,
and database operations.

Author: Sasank Tanikella
Created: 01-14-2025
"""

from fastapi import HTTPException, status

class BookException:
    """
    Book-related HTTP exceptions.
    
    Provides standardized exceptions for book operations including
    CRUD operations and validation errors.
    """
    NotFound = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
    
    InvalidInput = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Invalid book data"
    )

    DuplicateTitle = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Book with this title already exists"
    )
    
    UpdateFailed = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to update book"
    )
    
    DeleteFailed = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to delete book"
    )
    
    InvalidISBN = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid ISBN format"
    )

class AuthException:
    """
    Authentication-related HTTP exceptions.
    
    Handles authentication and authorization errors including
    token validation and permission checks.
    """
    InvalidCredentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    ExpiredToken = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    InsufficientPermissions = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions to perform this action"
    )
    
    TokenMissing = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication token is missing",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    InvalidToken = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication token",
        headers={"WWW-Authenticate": "Bearer"}
    )

class DatabaseException:
    """
    Database-related HTTP exceptions.
    
    Handles database operation errors including connection issues
    and transaction failures.
    """
    ConnectionError = HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Database connection error"
    )
    
    QueryError = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database query execution failed"
    )
    
    TransactionError = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database transaction failed"
    )
    
    IntegrityError = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Database integrity constraint violation"
    )
