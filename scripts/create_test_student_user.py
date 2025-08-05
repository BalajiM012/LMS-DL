from src.app_factory import db
from src.models import User
from werkzeug.security import generate_password_hash

def create_test_student():
    user = User.query.filter_by(username='teststudent').first()
    if user:
        print("Test student user already exists.")
        return
    password_hash = generate_password_hash('testpassword', method='pbkdf2:sha256')
    test_user = User(
        fullname='Test Student',
        email='teststudent@example.com',
        username='teststudent',
        password=password_hash,
        role='student'
    )
    db.session.add(test_user)
    db.session.commit()
    print("Test student user created successfully.")

if __name__ == '__main__':
    from src.app_factory import create_app
    app = create_app()
    with app.app_context():
        create_test_student()
