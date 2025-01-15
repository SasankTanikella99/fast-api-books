"""
Server-Sent Events Routes Module

This module handles real-time event streaming endpoints with authentication.
It provides SSE (Server-Sent Events) functionality for book-related updates.


Key Features:
- Secure token verification to authenticate users for accessing real-time streams.
- Integration with Server-Sent Events (SSE) for pushing live updates to connected clients.
- Leverages JWT (JSON Web Token) for authentication and authorization mechanisms.

Dependencies:
- `fastapi` for defining API routes and handling HTTP requests and responses.
- `jose` for decoding and verifying JWT tokens.
- `dotenv` for loading environment variables for sensitive configurations.
- `app.controllers.sseController` for managing event-driven streaming logic.

Constants:
- `SECRET_KEY`: The secret key for decoding JWT tokens, loaded from environment variables.
- `ALGORITHM`: The hashing algorithm used for verifying JWT tokens (default: HS256).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Duration for which the access token remains valid.


Author: Sasank Tanikella
Created: 01-14-2025
"""

from fastapi import APIRouter, HTTPException, Request
from app.controllers import sseController
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants and configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


## verifying the token again 
@router.get("/updates/stream")
async def stream_book_updates(request: Request):
    """
    **`GET /updates/stream`**

    - Validates the presence of a `token` in the query parameters.
   - Decodes the token to extract the user's email (`sub` claim) using the provided secret key and algorithm.
   - Verifies the validity of the token. If invalid or the email is missing, raises an HTTP 401 Unauthorized error.
   - If the token is valid, calls the `stream_updates` method from the `sseController` to stream live updates.
   """
    token = request.query_params.get("token")
    if not token:
        raise HTTPException(
            status_code=401,
            detail="No token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await sseController.stream_updates()
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )