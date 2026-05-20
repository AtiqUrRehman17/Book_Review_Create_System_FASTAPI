# init_db.py - Run this FIRST
from app.database import engine, Base
from app import models

def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Show created tables
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if tables:
        print("\nTables created:")
        for table in tables:
            print(f"  ✓ {table}")
    else:
        print("No tables were created. Check your models.")

if __name__ == "__main__":
    init_database()