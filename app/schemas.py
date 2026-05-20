from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

# Enums for response models
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class ReviewStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# User schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)
    
class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Book schemas
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    isbn: Optional[str] = Field(None, pattern=r'^[0-9]{10,13}$')
    published_year: Optional[int] = Field(None, ge=1000, le=2025)

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    isbn: Optional[str] = Field(None, pattern=r'^[0-9]{10,13}$')
    published_year: Optional[int] = Field(None, ge=1000, le=2025)

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str]
    isbn: Optional[str]
    published_year: Optional[int]
    created_at: datetime
    average_rating: Optional[float] = None
    review_count: Optional[int] = None
    
    class Config:
        from_attributes = True

# Review schemas
class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=1, max_length=1000)
    
    @field_validator('comment')
    def comment_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Comment cannot be empty')
        return v

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, min_length=1, max_length=1000)

class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str
    status: ReviewStatus
    user_id: int
    book_id: int
    created_at: datetime
    updated_at: datetime
    username: Optional[str] = None  # Added for convenience
    
    class Config:
        from_attributes = True

class ReviewApprove(BaseModel):
    status: ReviewStatus  # APPROVED or REJECTED

# Admin schemas
class AdminUserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.ADMIN