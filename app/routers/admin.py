from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/pending-reviews", response_model=List[schemas.ReviewResponse])
def get_pending_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Get all reviews pending approval (Admin only)"""
    pending_reviews = db.query(models.Review).filter(
        models.Review.status == models.ReviewStatus.PENDING
    ).offset(skip).limit(limit).all()
    
    result = []
    for review in pending_reviews:
        response = schemas.ReviewResponse.model_validate(review)
        response.username = review.user.username
        result.append(response)
    
    return result

@router.put("/reviews/{review_id}/approve", response_model=schemas.ReviewResponse)
def approve_review(
    review_id: int,
    approve_data: schemas.ReviewApprove,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Approve or reject a review (Admin only)"""
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    if review.status != models.ReviewStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Review is already {review.status.value}"
        )
    
    review.status = approve_data.status
    db.commit()
    db.refresh(review)
    
    response = schemas.ReviewResponse.model_validate(review)
    response.username = review.user.username
    return response

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Delete any review (Admin only)"""
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    db.delete(review)
    db.commit()
    return None

@router.get("/stats", response_model=dict)
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Get system statistics (Admin only)"""
    total_users = db.query(models.User).count()
    total_books = db.query(models.Book).count()
    total_reviews = db.query(models.Review).count()
    pending_reviews = db.query(models.Review).filter(
        models.Review.status == models.ReviewStatus.PENDING
    ).count()
    approved_reviews = db.query(models.Review).filter(
        models.Review.status == models.ReviewStatus.APPROVED
    ).count()
    rejected_reviews = db.query(models.Review).filter(
        models.Review.status == models.ReviewStatus.REJECTED
    ).count()
    
    return {
        "total_users": total_users,
        "total_books": total_books,
        "total_reviews": total_reviews,
        "pending_reviews": pending_reviews,
        "approved_reviews": approved_reviews,
        "rejected_reviews": rejected_reviews
    }