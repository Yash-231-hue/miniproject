from app import app
from models import db, User

with app.app_context():
    admin = User.query.filter_by(username='admin123').first()
    if admin:
        print(f"User: {admin.username}")
        print(f"Admin: {admin.is_admin}")
        print(f"Hash: {admin.password_hash}")
    else:
        print("User not found")
