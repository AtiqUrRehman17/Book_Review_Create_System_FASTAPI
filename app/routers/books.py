from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/api/books", tags=["Books"])

@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book_data: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)  # Only admin can add books
):
    """Create a new book (Admin only)"""
    # Check if book with same ISBN already exists
    if book_data.isbn:
        existing_book = db.query(models.Book).filter(models.Book.isbn == book_data.isbn).first()
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ISBN already exists"
            )
    
    new_book = models.Book(**book_data.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/", response_model=List[schemas.BookResponse])
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    title: Optional[str] = None,
    author: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all books with optional filters
    - Filter by title (partial match)
    - Filter by author (partial match)
    """
    query = db.query(models.Book)
    
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    
    books = query.offset(skip).limit(limit).all()
    
    # Calculate average rating and review count for each book
    result = []
    for book in books:
        approved_reviews = db.query(models.Review).filter(
            models.Review.book_id == book.id,
            models.Review.status == models.ReviewStatus.APPROVED
        ).all()
        
        avg_rating = sum(r.rating for r in approved_reviews) / len(approved_reviews) if approved_reviews else None
        review_count = len(approved_reviews)
        
        book_response = schemas.BookResponse.model_validate(book)
        book_response.average_rating = round(avg_rating, 2) if avg_rating else None
        book_response.review_count = review_count
        result.append(book_response)
    
    return result

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    # Calculate average rating and review count
    approved_reviews = db.query(models.Review).filter(
        models.Review.book_id == book_id,
        models.Review.status == models.ReviewStatus.APPROVED
    ).all()
    
    avg_rating = sum(r.rating for r in approved_reviews) / len(approved_reviews) if approved_reviews else None
    review_count = len(approved_reviews)
    
    book_response = schemas.BookResponse.model_validate(book)
    book_response.average_rating = round(avg_rating, 2) if avg_rating else None
    book_response.review_count = review_count
    
    return book_response

@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    book_data: schemas.BookUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)  # Only admin can update books
):
    """Update a book (Admin only)"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    # Update only provided fields
    update_data = book_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)
    
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)  # Only admin can delete books
):
    """Delete a book (Admin only)"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return None