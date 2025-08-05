from src.app_factory import db
from src.models import User
from werkzeug.security import generate_password_hash

def create_admin():
    # Create app context
    from src.app_factory import create_app
    app = create_app()
    
    with app.app_context():
        admin = User(
            username="newadmin",
            email="newadmin@example.com",
            password_hash=generate_password_hash("newadminpassword"),
            role="admin"
        )
        # Remove existing admin with same username or email if any
        existing_admin = User.query.filter((User.username == admin.username) | (User.email == admin.email)).first()
        if existing_admin:
            db.session.delete(existing_admin)
            db.session.commit()
        db.session.add(admin)
        db.session.commit()
        print("New admin user created successfully.")

