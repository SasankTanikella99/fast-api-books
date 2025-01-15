"""
Authentication Middleware Module

This module provides authentication and token management functionality.
It handles JWT token generation, validation, and password hashing operations.

Author: Sasank Tanikella
Created: 01-14-2025
"""


from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants and configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Custom HTTP Bearer dependency
http_bearer = HTTPBearer()

# Test user
# Hardcoding user credentials, as there is no user table, (instead of creating a user table and creating new users, I hard coded a test user)
TEST_USER = {
    "email": "testuser@test.com",
    "hashed_password": pwd_context.hash("testpassword")
}

# Functions for password hashing and verification
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Authenticate a user
def authenticate_user(email: str, password: str):
    if email != TEST_USER["email"]:
        return False
    if not verify_password(password, TEST_USER["hashed_password"]):
        return False
    return TEST_USER

# Create a JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify the provided JWT token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = credentials.credentials 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception

