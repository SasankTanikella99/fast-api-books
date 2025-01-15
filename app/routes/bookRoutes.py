"""
Book Routes Module

This module defines the API endpoints for book operations including CRUD operations.
All endpoints require JWT authentication and handle database operations through the book controller.

Author: Sasank Tanikella
Created: 01-14-2025
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app import schemas, database_config
from app.controllers import bookController
from app.authentication_middleware import verify_token

router = APIRouter()

@router.post("/", 
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    response_description="The created book"
)
async def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(database_config.get_db_connection),
    current_user: str = Depends(verify_token)
) -> schemas.Book:
    """
    Create a new book in the database.

    Args:
        book: Book data for creation
        db: Database session
        current_user: Email of authenticated user

    Returns:
        schemas.Book: Created book object

    Raises:
        HTTPException: 400 if creation fails
    """
    try:
        return await bookController.create_book(book, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", 
    response_model=List[schemas.Book],
    summary="Get all books",
    response_description="List of books"
)
async def read_books(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database_config.get_db_connection),
    current_user: str = Depends(verify_token)
) -> List[schemas.Book]:
    """
    Retrieve a paginated list of books.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Email of authenticated user

    Returns:
        List[schemas.Book]: List of book objects
    """
    try:
        return await bookController.get_books(skip, limit, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{book_id}", 
    response_model=schemas.Book,
    summary="Get a specific book",
    response_description="The requested book"
)
async def read_book(
    book_id: int,
    db: Session = Depends(database_config.get_db_connection),
    current_user: str = Depends(verify_token)
) -> schemas.Book:
    """
    Retrieve a specific book by ID.

    Args:
        book_id: ID of the book to retrieve
        db: Database session
        current_user: Email of authenticated user

    Returns:
        schemas.Book: Requested book object

    Raises:
        HTTPException: 404 if book not found
    """
    try:
        book = await bookController.get_book(book_id, db)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return book
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{book_id}", 
    response_model=schemas.Book,
    summary="Update a book",
    response_description="The updated book"
)
async def update_book(
    book_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(database_config.get_db_connection),
    current_user: str = Depends(verify_token)
) -> schemas.Book:
    """
    Update an existing book.

    Args:
        book_id: ID of the book to update
        book: Updated book data
        db: Database session
        current_user: Email of authenticated user

    Returns:
        schemas.Book: Updated book object

    Raises:
        HTTPException: 404 if book not found
    """
    try:
        updated_book = await bookController.update_book(book_id, book, db)
        if not updated_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return updated_book
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{book_id}",
    response_model=Dict[str, Any],
    summary="Delete a book",
    response_description="Deletion confirmation"
)
async def delete_book(
    book_id: int,
    db: Session = Depends(database_config.get_db_connection),
    current_user: str = Depends(verify_token)
) -> Dict[str, Any]:
    """
    Delete a book from the database.

    Args:
        book_id: ID of the book to delete
        db: Database session
        current_user: Email of authenticated user

    Returns:
        Dict[str, Any]: Deletion confirmation message

    Raises:
        HTTPException: 404 if book not found
    """
    try:
        result = await bookController.delete_book(book_id, db)
        return {
            "message": "Book deleted successfully",
            "book": result
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
