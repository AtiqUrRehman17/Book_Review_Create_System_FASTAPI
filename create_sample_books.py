# create_sample_books.py - Run this THIRD (optional)
from app.database import SessionLocal
from app.models import Book

def create_sample_books():
    db = SessionLocal()
    
    sample_books = [
        Book(
            title="The Great Gatsby", 
            author="F. Scott Fitzgerald", 
            description="A story of decadence and excess in the Jazz Age",
            isbn="9780743273565", 
            published_year=1925
        ),
        Book(
            title="To Kill a Mockingbird", 
            author="Harper Lee", 
            description="A classic of modern American literature about racial injustice",
            isbn="9780061120084", 
            published_year=1960
        ),
        Book(
            title="1984", 
            author="George Orwell", 
            description="Dystopian social science fiction about totalitarianism",
            isbn="9780451524935", 
            published_year=1949
        ),
        Book(
            title="Pride and Prejudice", 
            author="Jane Austen", 
            description="Romantic novel of manners set in Georgian England",
            isbn="9780141439518", 
            published_year=1813
        ),
        Book(
            title="The Hobbit", 
            author="J.R.R. Tolkien", 
            description="Fantasy adventure about Bilbo Baggins",
            isbn="9780547928227", 
            published_year=1937
        ),
    ]
    
    added_count = 0
    for book in sample_books:
        existing = db.query(Book).filter(Book.title == book.title).first()
        if not existing:
            db.add(book)
            added_count += 1
    
    db.commit()
    print(f"✓ Added {added_count} sample books to the database!")
    
    # Show all books
    all_books = db.query(Book).all()
    print(f"\nTotal books in database: {len(all_books)}")
    print("\nBook list:")
    for book in all_books:
        print(f"  {book.id}. {book.title} by {book.author}")
    
    db.close()

if __name__ == "__main__":
    create_sample_books()