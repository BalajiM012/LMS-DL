import csv
import sys
import os
from datetime import datetime, timedelta
import sys
import os

# Adjust sys.path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app_factory import create_app, db
from src.models import Book, User, BorrowRecord
from datetime import datetime, timedelta
import csv

app = create_app()

def import_books(csv_path):
    with app.app_context():
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                isbn = row.get('isbn') or row.get('ISBN') or ''
                # Skip books with empty ISBN to avoid UNIQUE constraint errors
                if not isbn.strip():
                    continue
                # Check if book with this ISBN already exists to avoid duplicates
                existing_book = Book.query.filter_by(isbn=isbn).first()
                if existing_book:
                    continue
                book = Book(
                    title=row.get('title') or row.get('Title') or 'Unknown Title',
                    author=row.get('author') or row.get('Author') or 'Unknown Author',
                    isbn=isbn,
                    copies=int(row.get('copies') or 1)
                )
                db.session.add(book)
            db.session.commit()
        print(f"Imported books from {csv_path}")

def import_users_and_borrows(csv_path):
    with app.app_context():
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Import user if not exists
                email = row.get('email') or ''
                username = row.get('username') or ''
                if not email.strip() and not username.strip():
                    # Skip users with no email and no username to avoid UNIQUE constraint errors
                    continue
                user = User.query.filter((User.email == email) | (User.username == username)).first()
                if not user:
                    user = User(
                        fullname=row.get('fullname') or row.get('FullName') or 'Unknown User',
                        email=email,
                        username=username,
                        password='hashed_password_placeholder',  # You may want to handle password properly
                        role='student'
                    )
                    db.session.add(user)
                    db.session.flush()  # To get user.id

                # Import borrow record if book exists
                book = Book.query.filter_by(isbn=row.get('isbn')).first()
                if book:
                    borrow_date_str = row.get('borrow_date') or row.get('BorrowDate')
                    due_date_str = row.get('due_date') or row.get('DueDate')
                    return_date_str = row.get('return_date') or row.get('ReturnDate')

                    borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d') if borrow_date_str else datetime.now()
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else borrow_date + timedelta(days=14)
                    return_date = datetime.strptime(return_date_str, '%Y-%m-%d') if return_date_str else None

                    borrow_record = BorrowRecord(
                        user_id=user.id,
                        book_id=book.id,
                        borrow_date=borrow_date,
                        due_date=due_date,
                        return_date=return_date,
                        fine=0.0
                    )
                    db.session.add(borrow_record)
            db.session.commit()
        print(f"Imported users and borrow records from {csv_path}")

if __name__ == '__main__':
    import_books(r"C:\Users\admin\Documents\Summer Project\Datasets\book1-100k.csv")
    import_users_and_borrows(r"C:\Users\admin\Documents\Summer Project\Datasets\Library_Usage.csv")
