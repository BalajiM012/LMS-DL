from flask import Blueprint, request, jsonify
from src.app_factory import db
from src.models import Book, BookRating, BookRecommendation
from sqlalchemy import or_, desc

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    """Get all books with optional filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    genre = request.args.get('genre', '')
    author = request.args.get('author', '')
    
    query = Book.query
    
    if search:
        query = query.filter(
            or_(
                Book.title.contains(search),
                Book.author.contains(search),
                Book.isbn.contains(search)
            )
        )
    
    if genre:
        query = query.filter(Book.genre == genre)
    
    if author:
        query = query.filter(Book.author.contains(author))
    
    books = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'books': [{
            'id': book.id,
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'year': book.year,
            'genre': book.genre,
            'pages': book.pages,
            'language': book.language,
            'cover_image': book.cover_image,
            'description': book.description,
            'average_rating': book.average_rating,
            'ratings_count': book.ratings_count,
            'stock': book.stock,
            'created_at': book.created_at.isoformat()
        } for book in books.items],
        'total': books.total,
        'pages': books.pages,
        'current_page': page
    })

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID"""
    book = Book.query.get_or_404(book_id)
    
    return jsonify({
        'id': book.id,
        'isbn': book.isbn,
        'title': book.title,
        'author': book.author,
        'publisher': book.publisher,
        'year': book.year,
        'genre': book.book_genre,
        'pages': book.pages,
        'language': book.language,
        'cover_image': book.cover_image,
        'description': book.description,
        'average_rating': book.average_rating,
        'ratings_count': book.ratings_count,
        'stock': book.stock,
        'created_at': book.created_at.isoformat()
    })

@books_bp.route('/genres', methods=['GET'])
def get_genres():
    """Get all unique genres"""
    genres = db.session.query(Book.genre).distinct().filter(Book.genre != None).all()
    return jsonify([genre[0] for genre in genres if genre[0]])

@books_bp.route('/top-rated', methods=['GET'])
def get_top_rated_books():
    """Get top rated books"""
    limit = request.args.get('limit', 10, type=int)
    books = Book.query.filter(
        Book.average_rating.isnot(None),
        Book.ratings_count > 0
    ).order_by(desc(Book.average_rating)).limit(limit).all()
    
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'average_rating': book.average_rating,
        'ratings_count': book.ratings_count,
        'cover_image': book.cover_image
    } for book in books])

@books_bp.route('/<int:book_id>/recommendations', methods=['GET'])
def get_book_recommendations(book_id):
    """Get book recommendations based on a specific book"""
    recommendations = BookRecommendation.query.filter_by(book_id=book_id)\
        .join(Book, BookRecommendation.recommended_book_id == Book.id)\
        .order_by(desc(BookRecommendation.score)).limit(10).all()
    
    return jsonify([{
        'book': {
            'id': rec.recommended_book.id,
            'title': rec.recommended_book.title,
            'author': rec.recommended_book.author,
            'average_rating': rec.recommended_book.average_rating,
            'cover_image': rec.recommended_book.cover_image
        },
        'score': rec.score
    } for rec in recommendations])

@books_bp.route('/<int:book_id>/ratings', methods=['POST'])
def add_book_rating(book_id):
    """Add a rating for a book"""
    data = request.get_json()
    
    if not data or 'rating' not in data:
        return jsonify({'error': 'Rating is required'}), 400
    
    rating = data.get('rating')
    review = data.get('review', '')
    
    if not 1 <= rating <= 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    # Check if user already rated this book
    existing_rating = BookRating.query.filter_by(
        user_id=1,  # For demo purposes, using user_id=1
        book_id=book_id
    ).first()
    
    if existing_rating:
        existing_rating.rating = rating
        existing_rating.review = review
    else:
        new_rating = BookRating(
            user_id=1,  # For demo purposes
            book_id=book_id,
            rating=rating,
            review=review
        )
        db.session.add(new_rating)
    
    db.session.commit()
    
    # Update book average rating
    book = Book.query.get(book_id)
    ratings = BookRating.query.filter_by(book_id=book_id).all()
    if ratings:
        book.average_rating = sum(r.rating for r in ratings) / len(ratings)
        book.ratings_count = len(ratings)
        db.session.commit()
    
    return jsonify({'message': 'Rating added successfully'})

@books_bp.route('/import-dataset', methods=['POST'])
def import_book_dataset():
    """Import books from the book recommendation dataset"""
    from src.utils.dataset_importer import import_book_recommendation_dataset
    
    try:
        count = import_book_recommendation_dataset()
        return jsonify({'message': f'Successfully imported {count} books'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
