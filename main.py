from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, books, reviews, admin

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Book Review API",
    description="""
    ## Book Review REST API Service
    
    This API allows users to:
    - Register and login to their accounts
    - Post book reviews with ratings (1-5 stars)
    - View approved reviews for books
    
    ### Admin Features
    - Approve or reject pending reviews
    - Add, update, and delete books
    - Manage all reviews and users
    
    ### Authentication
    - Use `/api/auth/login` to get a JWT token
    - Include token in Authorization header: `Bearer <token>`
    
    ### Review Status Flow
    1. User posts review → Status: `pending`
    2. Admin approves → Status: `approved` (visible to all)
    3. Admin rejects → Status: `rejected` (deleted)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    }
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(admin.router)

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Book Review API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "auth": "/api/auth",
            "books": "/api/books",
            "reviews": "/api/reviews",
            "admin": "/api/admin"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Optional: Create a default admin user on startup
@app.on_event("startup")
def startup_event():
    from sqlalchemy.orm import Session
    from app.database import SessionLocal
    from app.auth import get_password_hash
    
    db = SessionLocal()
    
    # Check if admin user exists
    admin_user = db.query(admin.models.User).filter(
        admin.models.User.username == "admin"
    ).first