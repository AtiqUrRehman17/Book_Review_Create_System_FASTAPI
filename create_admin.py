# create_admin.py - Run this SECOND
from app.database import SessionLocal
from app.models import User, UserRole
from app.auth import get_password_hash

def create_admin():
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin user already exists!")
            print(f"Username: admin")
            return
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        
        db.add(admin_user)
        db.commit()
        print("=" * 50)
        print("✓ Admin user created successfully!")
        print("=" * 50)
        print("Username: admin")
        print("Password: admin123")
        print("=" * 50)
        print("\n⚠️  IMPORTANT: Change this password in production!")
        
    except Exception as e:
        print(f"Error creating admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()