"""
Book Controller Module

This module handles all business logic related to book operations including CRUD operations
and event broadcasting. It implements proper error handling and database transaction management.

Author: Sasank Tanikella
Created: 01-14-2025
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import models, schemas, exceptions
import logging
from app.events.manager import event_manager

# Logging setup
logging.basicConfig(level=logging.INFO)

async def create_book(book: schemas.BookCreate, db: Session):
    """Create a new book entry in the database.

    Args:
        book (schemas.BookCreate): Book data to be created.
        db (Session): SQLAlchemy database session.

    Returns:
        models.Book: The newly created book.

    Raises:
        exceptions.BookException.DuplicateTitle: If a book with the same title exists.
        exceptions.DatabaseException.ConnectionError: If a database error occurs.
    """
    try:
        existing_book = db.query(models.Book).filter(models.Book.title == book.title).first()
        if existing_book:
            raise exceptions.BookException.DuplicateTitle

        db_book = models.Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)

        # Convert to Pydantic model first
        book_data = schemas.Book.from_orm(db_book).dict()
        
        await event_manager.broadcast(
            "bookCreated", 
            "Book created successfully", 
            book_id=db_book.id,
            book_data=book_data
        )
        return db_book
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.DatabaseException.ConnectionError
    
async def get_books(skip: int, limit: int, db: Session):
    """Retrieve a list of books with pagination.

    Args:
        skip (int): Number of books to skip.
        limit (int): Maximum number of books to retrieve.
        db (Session): SQLAlchemy database session.

    Returns:
        List[models.Book]: List of books.

    Raises:
        exceptions.DatabaseException.ConnectionError: If a database error occurs.
    """
    try:
        books = db.query(models.Book).offset(skip).limit(limit).all()
        await event_manager.broadcast(
            "booksRetrieved", 
            "Books retrieved successfully"
        )
        return books
    except SQLAlchemyError:
        raise exceptions.DatabaseException.ConnectionError

async def get_book(book_id: int, db: Session):
    """Retrieve a single book by its ID.

    Args:
        book_id (int): The ID of the book to retrieve.
        db (Session): SQLAlchemy database session.

    Returns:
        models.Book: The book with the specified ID.

    Raises:
        exceptions.BookException.NotFound: If the book does not exist.
        exceptions.DatabaseException.ConnectionError: If a database error occurs.
    """
    try:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if book is None:
            raise exceptions.BookException.NotFound

        # Convert the SQLAlchemy model to a Pydantic model first
        book_data = schemas.Book.from_orm(book).dict()
        
        await event_manager.broadcast(
            "bookRetrieved", 
            "Book retrieved successfully", 
            book_id=book_id,
            book_data=book_data
        )
        return book
    except SQLAlchemyError:
        raise exceptions.DatabaseException.ConnectionError
    
async def update_book(book_id: int, book: schemas.BookCreate, db: Session):
    """Update the details of an existing book.

    Args:
        book_id (int): The ID of the book to update.
        book (schemas.BookCreate): The updated book data.
        db (Session): SQLAlchemy database session.

    Returns:
        models.Book: The updated book.

    Raises:
        exceptions.BookException.NotFound: If the book does not exist.
        exceptions.DatabaseException.ConnectionError: If a database error occurs.
    """
    try:
        db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not db_book:
            raise exceptions.BookException.NotFound

        for key, value in book.dict().items():
            setattr(db_book, key, value)

        db.commit()
        db.refresh(db_book)

        # Convert to Pydantic model first
        book_data = schemas.Book.from_orm(db_book).dict()
        
        await event_manager.broadcast(
            "bookUpdated", 
            "Book updated successfully", 
            book_id=book_id,
            book_data=book_data
        )
        return db_book
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.DatabaseException.ConnectionError
    
async def delete_book(book_id: int, db: Session):
    """Delete a book from the database.

    Args:
        book_id (int): The ID of the book to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A message confirming the deletion.

    Raises:
        exceptions.BookException.NotFound: If the book does not exist.
        exceptions.DatabaseException.ConnectionError: If a database error occurs.
    """
    try:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not book:
            raise exceptions.BookException.NotFound

        db.delete(book)
        db.commit()

        await event_manager.broadcast(
            "bookDeleted", 
            "Book deleted successfully", 
            book_id=book_id
        )
        return {"message": "Book deleted successfully"}
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.DatabaseException.ConnectionError
