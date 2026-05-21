# 📚 Book Review Hub - Complete REST API 

A production-ready Book Review System built with FastAPI, featuring JWT authentication, role-based access control (User/Admin), review moderation workflow, and a modern Bootstrap frontend.

## 🌟 Features

### Backend Features
- ✅ **User Authentication**: JWT-based authentication with bcrypt password hashing
- ✅ **Role-Based Access**: Separate endpoints for Users and Admins
- ✅ **Review Moderation**: Admin approval workflow for quality control
- ✅ **Book Management**: Complete CRUD operations for books
- ✅ **Rating System**: 1-5 star ratings with average calculations
- ✅ **OpenAPI Documentation**: Auto-generated Swagger UI and ReDoc
- ✅ **SQLAlchemy ORM**: Database abstraction with SQLite (easily switch to PostgreSQL)
- ✅ **Input Validation**: Pydantic models for request/response validation

### Frontend Features
- ✅ **Responsive Design**: Bootstrap 5 with mobile-first approach
- ✅ **User Dashboard**: View books, write reviews, track your reviews
- ✅ **Admin Panel**: Approve/reject reviews, add books, view statistics
- ✅ **Real-time Updates**: Dynamic content loading without page refresh
- ✅ **Star Rating System**: Interactive star selection for reviews
- ✅ **Toast Notifications**: User-friendly feedback messages

## 🏗️ Architecture
┌─────────────────┐ ┌──────────────┐ ┌─────────────┐
│ Frontend │────▶│ FastAPI │────▶│ SQLite │
│ (Bootstrap) │◀────│ Backend │◀────│ Database │
└─────────────────┘ └──────────────┘ └─────────────┘
│ │ │
│ JWT Auth Models
│ Routes │
│ Middleware │
└───────────────────────────────────────────┘


## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge)
- Git (optional)

## 🚀 Quick Start Guide

### 1. Clone/Download the Project

```bash
git clone <your-repo-url>
cd book-review-api

# 2. Create Virtual Environment
Windows:

bash
python -m venv myenv
myenv\Scripts\activate

pip install -r requirements.txt

Create .env file in root directory:

env
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./book_review.db

python init_db.py

Create Admin User
bash
python create_admin.py


uvicorn main:app --reload --port 8000
```

## Project Structure

book-review-api/
│
├── app/                           # Backend application
│   ├── __init__.py
│   ├── main.py                    # FastAPI entry point
│   ├── database.py                # Database configuration
│   ├── models.py                  # SQLAlchemy models
│   ├── schemas.py                 # Pydantic schemas
│   ├── auth.py                    # Authentication logic
│   ├── dependencies.py            # Dependency injections
│   │
│   └── routers/                   # API route handlers
│       ├── auth.py                # Authentication endpoints
│       ├── books.py               # Book management
│       ├── reviews.py             # Review management
│       └── admin.py               # Admin endpoints
│
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables
├── init_db.py                    # Database initializer
├── create_admin.py               # Admin user creator
├── create_sample_books.py        # Sample data loader
├── run_app.bat                   # Windows launcher
└── README.md                     # This file



Authentication Endpoints
Method	Endpoint	Description	Auth
POST	/api/auth/register	Register new user	None
POST	/api/auth/login	Login & get JWT token	None
GET	/api/auth/me	Get current user info	Required
Book Endpoints
Method	Endpoint	Description	Auth
GET	/api/books	List all books with ratings	None
GET	/api/books/{id}	Get specific book details	None
POST	/api/books	Add new book	Admin
PUT	/api/books/{id}	Update book	Admin
DELETE	/api/books/{id}	Delete book	Admin
Review Endpoints
Method	Endpoint	Description	Auth
POST	/api/reviews/books/{id}	Write review (pending)	Required
GET	/api/reviews/books/{id}	Get book reviews	Optional
GET	/api/reviews/my-reviews	Get user's reviews	Required
PUT	/api/reviews/{id}	Update pending review	Required
DELETE	/api/reviews/{id}	Delete pending review	Required
Admin Endpoints
Method	Endpoint	Description	Auth
GET	/api/admin/pending-reviews	List pending reviews	Admin
PUT	/api/admin/reviews/{id}/approve	Approve/reject review	Admin
DELETE	/api/admin/reviews/{id}	Delete any review	Admin
GET	/api/admin/stats	System statistics	Admin
💻 API Usage Examples
Register a User
bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure123"
  }'
Login
bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=secure123"
Response:

json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
Create a Review
bash
curl -X POST "http://localhost:8000/api/reviews/books/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Excellent book! Highly recommended."
  }'
Get Books (Public)
bash
curl -X GET "http://localhost:8000/api/books"
Admin: Approve Review
bash
curl -X PUT "http://localhost:8000/api/admin/reviews/1/approve" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'
🎨 Frontend Features
User Flow
Registration: Create new account

Login: Authenticate to get JWT token

Browse Books: View all books with average ratings

Write Reviews: Rate books (1-5 stars) and write comments

Track Reviews: View all your reviews and their status

Edit/Delete: Modify or remove your pending reviews

Admin Flow
Admin Login: Special admin credentials

Dashboard: View system statistics

Review Moderation: Approve or reject pending reviews

Book Management: Add, update, or delete books

Content Control: Remove inappropriate reviews

Public Access
Browse all books

Read approved reviews

View book details and average ratings

No login required for reading

🔒 Security Features
Password Hashing: bcrypt with 12 rounds

JWT Tokens: Stateless authentication with 30-minute expiry

Role-Based Access: Admin vs User permissions

Input Validation: All user input sanitized with Pydantic

SQL Injection Protection: SQLAlchemy parameterized queries

CORS Protection: Configured for security

No Plain Text Passwords: Only hashed passwords stored

🧪 Testing
Manual Testing with Swagger UI
Start backend: uvicorn main:app --reload

Visit: http://localhost:8000/docs

Test endpoints interactively

Using curl Commands
bash
# Test health endpoint
curl http://localhost:8000/health

# Complete user flow
# 1. Register
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'

# 2. Login and save token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test&password=test123" | jq -r '.access_token')

# 3. Create review
curl -X POST "http://localhost:8000/api/reviews/books/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rating":5,"comment":"Great book!"}'
🐛 Troubleshooting
Common Issues and Solutions
Issue: "Module not found" errors
bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
Issue: Database locked
bash
# Solution: Delete and recreate database
del book_review.db  # Windows
rm book_review.db   # Mac/Linux
python init_db.py
Issue: CORS errors in browser
Solution: Update CORS settings in app/main.py:

python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Issue: Port already in use
bash
# Use different ports
uvicorn main:app --reload --port 8001
cd frontend && python -m http.server 8081
Issue: Can't login as admin
bash
# Recreate admin user
python recreate_admin.py
🚢 Deployment
Docker Deployment
Create Dockerfile:

dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
Build and run:

bash
docker build -t book-review-api .
docker run -p 8000:8000 book-review-api
Production Considerations
Database: Switch from SQLite to PostgreSQL

python
DATABASE_URL=postgresql://user:pass@localhost/dbname
Secret Key: Use strong, randomly generated key

bash
openssl rand -hex 32
HTTPS: Use reverse proxy (Nginx) with SSL

Environment Variables: Use proper secrets management

Logging: Implement proper logging for production

Rate Limiting: Add rate limiting for public endpoints

📊 Database Schema
Users Table
sql
- id (INTEGER, PK)
- username (TEXT, UNIQUE)
- email (TEXT, UNIQUE)
- hashed_password (TEXT)
- role (TEXT: 'user'/'admin')
- created_at (TIMESTAMP)
Books Table
sql
- id (INTEGER, PK)
- title (TEXT)
- author (TEXT)
- description (TEXT)
- isbn (TEXT, UNIQUE)
- published_year (INTEGER)
- created_at (TIMESTAMP)
Reviews Table
sql
- id (INTEGER, PK)
- rating (INTEGER, 1-5)
- comment (TEXT)
- status (TEXT: 'pending'/'approved'/'rejected')
- user_id (INTEGER, FK)
- book_id (INTEGER, FK)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
🛠️ Development Tools
Recommended VS Code Extensions
Python

Pylance

SQLite Viewer

Prettier

Live Server

Useful Commands
bash
# Database inspection
sqlite3 book_review.db
.tables
SELECT * FROM users;

# Check API endpoints
curl http://localhost:8000/openapi.json | jq

# Format Python code
black app/

# Check for security issues
bandit -r app/
📈 Performance Optimization Tips
Database Indexing: Add indexes on frequently queried fields

python
# In models.py
__table_args__ = (Index('idx_user_username', 'username'),)
Query Optimization: Use selectinload for relationships

python
from sqlalchemy.orm import selectinload
query = db.query(Book).options(selectinload(Book.reviews))
Caching: Implement Redis for frequently accessed data

Pagination: Use skip/limit for large datasets

Async Endpoints: Convert to async for I/O operations

🤝 Contributing
Fork the repository

Create feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👥 Authors
Your Name - Initial work

🙏 Acknowledgments
FastAPI documentation and community

Bootstrap team for the frontend framework

All open-source contributors

📞 Support
For support:

Check troubleshooting section

Open an issue on GitHub

Contact: your-email@example.com

🎯 Roadmap
Version 2.0 Planned Features
Email verification on registration

Password reset functionality

User profiles with avatars

Book search and filtering

Social sharing of reviews

API rate limiting

WebSocket for real-time notifications

Mobile app with React Native

Export reviews as PDF

Weekly digest emails

🏁 Quick Reference Card
Starting the Application
bash
# Terminal 1 - Backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend && python -m http.server 8080
Default Ports
Backend API: 8000

Frontend: 8080

API Docs: 8000/docs

Default Admin Credentials
Username: admin

Password: admin123

Key URLs
Frontend: http://localhost:8080

API Docs: http://localhost:8000/docs

Health Check: http://localhost:8000/health

🎉 Congratulations!
You've successfully set up the Book Review Hub application. Start exploring books, writing reviews, and building your reading community!

Happy Reading and Reviewing! 📚⭐

text
