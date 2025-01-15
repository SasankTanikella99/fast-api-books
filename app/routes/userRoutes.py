"""
User Authentication Routes Module

This module handles user authentication endpoints, specifically the login functionality.
It provides the API interface for user authentication and token generation.

Author: Sasank Tanikella
Created: 01-14-2025
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Dict

from app.controllers import userController
from app import schemas

class LoginRequest(BaseModel):
    """
    Schema for login request validation.

    Attributes:
        email (EmailStr): User's email address
        password (str): User's password in plain text

    Example:
        {
            "email": "user@example.com",
            "password": "userpassword123"
        }
    """
    email: EmailStr
    password: str

    class Config:
        """Pydantic model configuration"""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }

router = APIRouter()

@router.post(
    "/login",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and generate token",
    response_description="Access token for authenticated user",
    responses={
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid credentials"}
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid email format"}
                }
            }
        }
    }
)
async def login(login_request: LoginRequest) -> Dict[str, str]:
    """
    Authenticate user and generate access token.

    This endpoint validates user credentials and generates a JWT token
    for successful authentications. The token can be used for subsequent
    authenticated requests.

    Args:
        login_request (LoginRequest): User credentials containing email and password

    Returns:
        Dict[str, str]: Token response containing access token and token type
            {
                "access_token": "jwt-token-string",
                "token_type": "bearer"
            }

    Raises:
        HTTPException:
            - 401: If credentials are invalid
            - 422: If request validation fails

    Examples:
        >>> response = await login({"email": "user@example.com", "password": "pass123"})
        >>> print(response["access_token"])
        eyJ0eXAiOiJKV1QiLCJhbGc...
    """
    try:
        # Authenticate user and generate token
        token = userController.login_user(
            email=login_request.email,
            password=login_request.password
        )
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return token

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
