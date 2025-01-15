"""
Login Controller Module

This module handles user authentication and token generation.
It provides the core login functionality for the application.

Author: Sasank Tanikella
Created: 01-14-2025
"""

from typing import Dict
from fastapi import HTTPException, status
from app.authentication_middleware import (
    authenticate_user,
    create_access_token,
)

def login_user(email: str, password: str) -> Dict[str, str]:
    """
    Authenticates a user and generates an access token.

    This function verifies user credentials and creates a JWT token
    for successful authentications. It implements a stateless
    authentication mechanism using JWT tokens.

    Args:
        email (str): User's email address
        password (str): User's password in plain text

    Returns:
        Dict[str, str]: Dictionary containing access token and token type
            {
                "access_token": "jwt-token-string",
                "token_type": "bearer"
            }

    Notes:
        - Passwords are verified against hashed versions stored in the database
        - Tokens are JWT format with configured expiration time
        - Uses Bearer authentication scheme
    """
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user["email"]})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
