import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key_123'

    # MySQL database configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://yash:Yash%402005@localhost:3306/clinicdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin contact info
    ADMIN_EMAIL = 'admin@example.com'
    ADMIN_CONTACT = '+91-XXXXXXXXXX'

    # Email configuration for notifications
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your_email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your_app_password'
