from app import app
from models import db, User, UserRole
from werkzeug.security import generate_password_hash

with app.app_context():
    # Check if yash exists
    existing = User.query.filter_by(username='yash').first()
    if existing:
        print("User yash already exists")
        print(f"Role: {existing.role}")
        print(f"Hash: {existing.password_hash}")
        # Update to admin if not already
        if existing.role != UserRole.ADMIN:
            existing.role = UserRole.ADMIN
            db.session.commit()
            print("Updated to admin")
    else:
        # Create new admin user
        hashed = generate_password_hash('yash')
        admin = User(
            username='yash',
            email='yash@gmail.com',
            password_hash=hashed,
            contact='+91-XXXXXXXXXX',
            role=UserRole.ADMIN
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully")
        print(f"Username: yash")
        print(f"Password: yash")
        print(f"Email: yash@gmail.com")
        print(f"Hash: {hashed}")
