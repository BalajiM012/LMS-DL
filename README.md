# Library Management System

A modern library management system built with Next.js, PostgreSQL, and TypeScript, enhanced with TensorFlow-powered machine learning features.

## Features

- User authentication with role-based access (Admin/Student)
- Book inventory management
- Loan tracking with due dates and fines
- Admin dashboard with statistics
- Student portal with borrowed books and recommendations

### 🤖 Machine Learning Features (TensorFlow Powered)

- **AI Book Recommendations**: Personalized book suggestions using neural networks
- **Demand Forecasting**: Predicts future book demand for inventory optimization
- **Automated Fine Calculation**: Estimates potential fines with risk assessment
- **Due Date Tracking**: Predicts user compliance with due dates
- **Book Demand Forecasting**: Individual book popularity predictions

## Prerequisites

- Node.js (v18 or later)
- Docker and Docker Compose
- npm or yarn
- Python 3.10+ and pip (for backend Flask API)

### Machine Learning Prerequisites (Optional)

- TensorFlow-compatible system (Windows, macOS, or Linux)
- Python 3.8-3.11 (for TensorFlow compatibility)

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd library-management-system
```

2. Install frontend dependencies:

```bash
npm install
```

3. Set up environment variables:
   Create a `.env.local` file with the following content:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=library_db
JWT_SECRET=your-super-secret-key-change-this-in-production
JWT_EXPIRY=24h
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

4. Start the PostgreSQL database:

```bash
docker-compose up -d
```

5. Initialize the database with sample data:

```bash
npm run init-db
```

6. Set up Python virtual environment and install backend dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Machine Learning Installation (Optional)

```bash
pip install -r requirements-ml.txt
```

Note: The system includes mock TensorFlow implementations that work without installing actual TensorFlow.

7. Initialize backend database tables:

```bash
python create_tables.py
```

8. Start the Flask backend API server:

```bash
flask run
```

9. Start the Next.js frontend development server:

```bash
npm run dev
```

The application will be available at http://localhost:8000

## Default Users

After initialization, the following users are available:

### Admin

- Username: admin
- Password: admin123

### Students

- Username: student1
- Password: student123
- Username: student2
- Password: student123

## API Routes

### Authentication

- POST `/api/auth/login` - User login

### Admin Routes

- GET `/api/admin/books` - List all books
- POST `/api/admin/books` - Add a new book
- DELETE `/api/admin/books/{id}` - Delete a book
- GET `/api/admin/stats` - Get library statistics

### Student Routes

- GET `/api/student/books/borrowed` - Get user's borrowed books
- POST `/api/student/books/borrow` - Borrow a book
- GET `/api/student/books/recommended` - Get book recommendations
- GET `/api/student/get_books` - Get all books (new)
- POST `/api/student/submit_book` - Submit/return a book (new)
- GET `/api/student/borrowed_books_history` - Borrowed books history (new)
- GET `/api/student/fine_calculator` - Fine calculation (new)
- GET `/api/student/profile` - Student profile (new)

### Machine Learning API Routes

- GET `/api/tensorflow/status` - Check TensorFlow status
- GET `/api/tensorflow/recommendations` - Get book recommendations
- GET `/api/tensorflow/demand_forecast` - Get demand forecast
- POST `/api/tensorflow/fine_prediction` - Predict fines
- GET `/api/tensorflow/due_date_tracking` - Track due dates
- GET `/api/tensorflow/book_demand/{book_id}` - Forecast individual book demand

## Technology Stack

- **Frontend**: Next.js, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: Flask API, Next.js API Routes
- **Database**: PostgreSQL, SQLite (for testing)
- **Authentication**: JWT
- **Container**: Docker
- **ORM**: SQLAlchemy (Flask), node-postgres (pg)

## Development

### Database Schema

The system uses the following main tables:

- `users` - Store user information and roles
- `books` - Manage book inventory
- `borrow_records` - Track book loans and returns
- `categories` - Book categorization
- `fees` - Fine tracking

### File Structure

```
├── src/
│   ├── app/              # Next.js app directory
│   │   ├── api/          # API routes
│   │   ├── admin/        # Admin pages
│   │   └── student/      # Student pages
│   ├── components/       # React components
│   ├── features/        # Flask API features
│   │   ├── tensorflow_integration.py  # TensorFlow models and logic
│   │   ├── tensorflow_api.py          # TensorFlow API endpoints
│   │   └── ...                        # Other feature modules
│   ├── lib/              # Utilities and database
│   └── middleware.ts     # Authentication middleware
├── public/               # Static files
│   ├── tensorflow-dashboard.html      # AI dashboard frontend
│   ├── tensorflow-recommendations.html # Book recommendations frontend
│   └── ...                            # Other HTML files
├── scripts/              # Database initialization scripts
├── tests/                # Test cases
├── docker-compose.yml    # Docker configuration
└── requirements.txt      # Python dependencies
```

## License

MIT
└── requirements.txt      # Python dependencies

## Documentation

Additional documentation for machine learning features:
- `ML_FEATURES.md` - Detailed documentation of machine learning features
- `requirements-ml.txt` - Machine learning requirements

## License

MIT
