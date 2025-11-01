from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class UserRole(Enum):
    PATIENT = 'patient'
    DOCTOR = 'doctor'
    ADMIN = 'admin'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.PATIENT)
    contact = db.Column(db.String(30))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    dob = db.Column(db.Date)

    appointments = db.relationship('Appointment', back_populates='patient')
    feedbacks = db.relationship('Feedback', back_populates='user')

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(120), nullable=False)
    degree = db.Column(db.String(200))
    specialization = db.Column(db.String(200))
    bio = db.Column(db.Text)
    availability = db.Column(db.Text)  # JSON string for slots
    fees = db.Column(db.Float, default=0.0)
    rating = db.Column(db.Float, default=0.0)
    location = db.Column(db.String(100))  # city
    contact_info = db.Column(db.Text)  # email/phone
    verified = db.Column(db.Boolean, default=False)
    visit_types = db.Column(db.Text)  # JSON: ['online', 'clinic']
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', back_populates='doctor')
    feedbacks = db.relationship('Feedback', back_populates='doctor')
    user = db.relationship('User', backref='doctor_profile')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    visit_type = db.Column(db.String(20), default='clinic')  # online/clinic
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending/confirmed/cancelled
    reschedule_count = db.Column(db.Integer, default=0)
    doctor_response = db.Column(db.String(20))  # accept/decline
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship('Doctor', back_populates='appointments')
    patient = db.relationship('User', back_populates='appointments')

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='feedbacks')
    doctor = db.relationship('Doctor', back_populates='feedbacks')
