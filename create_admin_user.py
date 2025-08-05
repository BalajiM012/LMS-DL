from src.app_factory_minimal import db, create_app
from src.models import User
from werkzeug.security import generate_password_hash

def create_users():
    app = create_app()
    
    with app.app_context():
        # Check if admin user already exists
        existing_admin = User.query.filter_by(username="newadmin").first()
        if not existing_admin:
            # Create admin user
            admin = User(
                fullname="New Admin User",
                username="newadmin",
                email="newadmin@example.com",
                password=generate_password_hash("newadminpassword", method='pbkdf2:sha256'),
                role="admin"
            )
            db.session.add(admin)
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")
        
        # Delete existing student user if it exists
        existing_student = User.query.filter_by(username="newstudent").first()
        if existing_student:
            db.session.delete(existing_student)
            db.session.commit()
            print("Existing student user deleted.")
        
        # Create student user with correct password hash
        student = User(
            fullname="New Student User",
            username="newstudent",
            email="newstudent@example.com",
            password=generate_password_hash("newstudentpassword", method='pbkdf2:sha256'),
            role="student"
        )
        db.session.add(student)
        db.session.commit()
        print("Student user created successfully.")
        
        print("User creation process completed.")

if __name__ == "__main__":
    create_users()
