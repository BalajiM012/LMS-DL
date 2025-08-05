# Dataset Integration Guide

This document explains how the library management system integrates with various book datasets.

## Supported Datasets

### 1. Book Recommendation Dataset (Currently Implemented)

- **Source**: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset
- **Features**: Book metadata, ratings, recommendations
- **Status**: ✅ Implemented with sample data

### 2. Goodreads Book Datasets 10M

- **Source**: https://www.kaggle.com/datasets/bahramjannesarr/goodreads-book-datasets-10m
- **Features**: 10 million book records with ratings, reviews, and metadata
- **Status**: 🔄 Ready for implementation

### 3. Library Books Dataset

- **Source**: https://www.kaggle.com/datasets/bimalgajera/library-books
- **Features**: Library-specific book collections
- **Status**: 🔄 Ready for implementation

### 4. SF Library Usage Data

- **Source**: https://www.kaggle.com/datasets/datasf/sf-library-usage-data
- **Features**: Library usage statistics and patterns
- **Status**: 🔄 Ready for implementation

## Current Implementation

### Database Schema

The system now includes the following models:

1. **Book**: Enhanced with dataset fields

   - ISBN, title, author, publisher, year
   - Genre, pages, language, cover image
   - Description, average rating, ratings count
   - Stock management

2. **BookRating**: User ratings and reviews
3. **BookRecommendation**: AI-powered book recommendations
4. **User**: User management
5. **BorrowRecord**: Book borrowing history
6. **Fees**: Fine management

### API Endpoints

#### Books

- `GET /api/books` - Get all books with filtering and pagination
- `GET /api/books/<id>` - Get specific book details
- `GET /api/books/genres` - Get all unique genres
- `GET /api/books/top-rated` - Get top-rated books
- `GET /api/books/<id>/recommendations` - Get book recommendations
- `POST /api/books/<id>/ratings` - Add book rating
- `POST /api/books/import-dataset` - Import dataset

#### Users

- `GET /api/users` - Get all users
- `POST /api/users` - Create new user

#### Borrowing

- `GET /api/borrowing` - Get all borrow records
- `POST /api/borrowing` - Create new borrow record
- `PUT /api/borrowing/<id>/return` - Return a book

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_new_db.py
```

This will:

- Drop existing tables
- Create new schema
- Import sample book recommendation dataset
- Create admin user (username: admin, password: admin123)

### 3. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Dataset Import Process

### Manual Import

You can manually trigger dataset import via API:

```bash
curl -X POST http://localhost:5000/api/books/import-dataset
```

### Custom Dataset Import

To import your own dataset:

1. Place your CSV file in the `data/` directory
2. Update the import function in `src/utils/dataset_importer.py`
3. Run the import script

## Sample Data Structure

The current implementation includes 10 sample books from popular fantasy series:

- Harry Potter series (7 books)
- The Hobbit
- The Lord of the Rings
- The Chronicles of Narnia

Each book includes:

- Complete metadata
- Sample ratings
- Recommendation relationships
- Stock information

## Future Enhancements

### Planned Features

1. **Real-time Dataset Import**: Direct Kaggle API integration
2. **Advanced Search**: Full-text search with Elasticsearch
3. **Recommendation Engine**: ML-based book recommendations
4. **User Preferences**: Personalized book suggestions
5. **Reading Lists**: User-curated book collections
6. **Social Features**: Book reviews and ratings

### Dataset Expansion

1. **Goodreads Integration**: Import 10M+ book records
2. **Library Systems**: Integration with actual library catalogs
3. **Publisher APIs**: Real-time book availability
4. **Academic Datasets**: Research paper and textbook integration

## API Usage Examples

### Get All Books

```bash
curl http://localhost:5000/api/books
```

### Search Books

```bash
curl "http://localhost:5000/api/books?search=harry&genre=Fantasy"
```

### Get Book Recommendations

```bash
curl http://localhost:5000/api/books/1/recommendations
```

### Add Book Rating

```bash
curl -X POST http://localhost:5000/api/books/1/ratings \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "review": "Excellent book!"}'
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**

   - Ensure SQLite database file exists
   - Check file permissions

2. **Import Errors**

   - Verify dataset file format
   - Check for duplicate ISBNs

3. **API Errors**
   - Ensure all dependencies are installed
   - Check Flask app configuration

### Debug Mode

Run the application in debug mode:

```bash
python app.py
```

The server will automatically reload on code changes.

## Contributing

To add new datasets:

1. Create import function in `src/utils/dataset_importer.py`
2. Add API endpoint in `src/routes/books.py`
3. Update database schema if needed
4. Add tests for new functionality
5. Update this documentation
