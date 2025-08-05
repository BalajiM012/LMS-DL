import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app_factory import create_app
from src.models import BorrowRecord

app = create_app()

with app.app_context():
    records = BorrowRecord.query.filter_by(return_date=None).all()
    for r in records:
        print(f"user_id: {r.user_id}, book_id: {r.book_id}")
