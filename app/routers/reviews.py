from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user, get_optional_user

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

@router.post("/books/{book_id}", response_model=schemas.ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    book_id: int,
    review_data: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Create a new review for a book (requires authentication)"""
    # Check if book exists
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    # Check if user already reviewed this book
    existing_review = db.query(models.Review).filter(
        models.Review.book_id == book_id,
        models.Review.user_id == current_user.id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this book"
        )
    
    # Create new review (pending by default)
    new_review = models.Review(
        rating=review_data.rating,
        comment=review_data.comment,
        user_id=current_user.id,
        book_id=book_id,
        status=models.ReviewStatus.PENDING
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    # Add username to response
    response = schemas.ReviewResponse.model_validate(new_review)
    response.username = current_user.username
    
    return response

@router.get("/books/{book_id}", response_model=List[schemas.ReviewResponse])
def get_book_reviews(
    book_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_user)
):
    """
    Get reviews for a specific book
    - Public users see only approved reviews
    - Authenticated users see their own pending reviews plus approved reviews
    - Admin users see all reviews
    """
    # Check if book exists
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    query = db.query(models.Review).filter(models.Review.book_id == book_id)
    
    # Filter based on user role
    if current_user and current_user.role == models.UserRole.ADMIN:
        # Admin sees all reviews
        pass
    elif current_user:
        # Regular user sees approved reviews + their own pending reviews
        query = query.filter(
            (models.Review.status == models.ReviewStatus.APPROVED) |
            (models.Review.user_id == current_user.id)
        )
    else:
        # Public user sees only approved reviews
        query = query.filter(models.Review.status == models.ReviewStatus.APPROVED)
    
    reviews = query.offset(skip).limit(limit).all()
    
    # Add username to each review
    result = []
    for review in reviews:
        response = schemas.ReviewResponse.model_validate(review)
        response.username = review.user.username
        result.append(response)
    
    return result

@router.get("/my-reviews", response_model=List[schemas.ReviewResponse])
def get_my_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get all reviews written by the current user"""
    reviews = db.query(models.Review).filter(
        models.Review.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    result = []
    for review in reviews:
        response = schemas.ReviewResponse.model_validate(review)
        response.username = current_user.username
        result.append(response)
    
    return result

@router.put("/{review_id}", response_model=schemas.ReviewResponse)
def update_review(
    review_id: int,
    review_data: schemas.ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Update a review
    - Users can only update their own pending reviews
    - Admin can update any review
    """
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    # Check permissions
    if review.user_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own reviews"
        )
    
    # Check if review is not approved yet (or admin can update any)
    if review.status == models.ReviewStatus.APPROVED and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update an approved review"
        )
    
    # Update only provided fields
    update_data = review_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)
    
    db.commit()
    db.refresh(review)
    
    response = schemas.ReviewResponse.model_validate(review)
    response.username = review.user.username
    return response

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Delete a review
    - Users can only delete their own pending reviews
    - Admin can delete any review
    """
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    # Check permissions
    if review.user_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews"
        )
    
    # Check if review is not approved yet (or admin can delete any)
    if review.status == models.ReviewStatus.APPROVED and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete an approved review"
        )
    
    db.delete(review)
    db.commit()
    return None