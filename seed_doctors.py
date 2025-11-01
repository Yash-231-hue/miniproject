from app import app, db
from models import Doctor, User, UserRole
import json

def seed_doctors():
    with app.app_context():
        # Check if doctors already exist
        if Doctor.query.count() > 0:
            print("Doctors already seeded!")
            return

        # Sample doctor data
        doctors_data = [
            {
                'username': 'dr_smith',
                'email': 'smith@clinic.com',
                'password_hash': 'pbkdf2:sha256:260000$ugBfY05GEHFttxFl$b18af3f230dbeaeb84b2f1a5915beb85f80a4e1b762f9413c7bcda9aefce64a6',  # password: doctor123
                'contact': '+91-9876543210',
                'role': UserRole.DOCTOR,
                'name': 'Dr. John Smith',
                'degree': 'MD, MBBS',
                'specialization': 'Cardiology',
                'bio': 'Experienced cardiologist with 15 years of practice. Specializes in heart diseases and preventive cardiology.',
                'fees': 1500.0,
                'location': 'Mumbai',
                'contact_info': 'smith@clinic.com, +91-9876543210',
                'visit_types': json.dumps(['clinic', 'online']),
                'verified': True
            },
            {
                'username': 'dr_jones',
                'email': 'jones@clinic.com',
                'password_hash': 'pbkdf2:sha256:260000$TBTR0D4A0gvuaXHG$4fec38cacae6d2ceba7b49216c85af43c5670c8a0f2798b108b704c83c5c6d7a',  # password: doctor123
                'contact': '+91-9876543211',
                'role': UserRole.DOCTOR,
                'name': 'Dr. Emily Jones',
                'degree': 'MD, Pediatrics',
                'specialization': 'Pediatrics',
                'bio': 'Dedicated pediatrician focused on child health and development. 10 years experience in pediatric care.',
                'fees': 1200.0,
                'location': 'Delhi',
                'contact_info': 'jones@clinic.com, +91-9876543211',
                'visit_types': json.dumps(['clinic', 'online']),
                'verified': True
            },
            {
                'username': 'dr_brown',
                'email': 'brown@clinic.com',
                'password_hash': 'pbkdf2:sha256:260000$TBTR0D4A0gvuaXHG$4fec38cacae6d2ceba7b49216c85af43c5670c8a0f2798b108b704c83c5c6d7a',  # password: doctor123
                'contact': '+91-9876543212',
                'role': UserRole.DOCTOR,
                'name': 'Dr. Michael Brown',
                'degree': 'MS, Orthopedics',
                'specialization': 'Orthopedics',
                'bio': 'Orthopedic surgeon specializing in joint replacements and sports injuries. 12 years of surgical experience.',
                'fees': 2000.0,
                'location': 'Bangalore',
                'contact_info': 'brown@clinic.com, +91-9876543212',
                'visit_types': json.dumps(['clinic']),
                'verified': True
            },
            {
                'username': 'dr_davis',
                'email': 'davis@clinic.com',
                'password_hash': 'pbkdf2:sha256:260000$TBTR0D4A0gvuaXHG$4fec38cacae6d2ceba7b49216c85af43c5670c8a0f2798b108b704c83c5c6d7a',  # password: doctor123
                'contact': '+91-9876543213',
                'role': UserRole.DOCTOR,
                'name': 'Dr. Sarah Davis',
                'degree': 'MD, Dermatology',
                'specialization': 'Dermatology',
                'bio': 'Dermatologist with expertise in skin disorders, cosmetic procedures, and laser treatments.',
                'fees': 1800.0,
                'location': 'Chennai',
                'contact_info': 'davis@clinic.com, +91-9876543213',
                'visit_types': json.dumps(['clinic', 'online']),
                'verified': True
            },
            {
                'username': 'dr_wilson',
                'email': 'wilson@clinic.com',
                'password_hash': 'pbkdf2:sha256:260000$TBTR0D4A0gvuaXHG$4fec38cacae6d2ceba7b49216c85af43c5670c8a0f2798b108b704c83c5c6d7a',  # password: doctor123
                'contact': '+91-9876543214',
                'role': UserRole.DOCTOR,
                'name': 'Dr. Robert Wilson',
                'degree': 'MD, Psychiatry',
                'specialization': 'Psychiatry',
                'bio': 'Psychiatrist specializing in mental health disorders, therapy, and medication management.',
                'fees': 1600.0,
                'location': 'Pune',
                'contact_info': 'wilson@clinic.com, +91-9876543214',
                'visit_types': json.dumps(['online']),
                'verified': True
            }
        ]

        for doc_data in doctors_data:
            # Create user first
            user = User(
                username=doc_data['username'],
                email=doc_data['email'],
                password_hash=doc_data['password_hash'],
                contact=doc_data['contact'],
                role=doc_data['role']
            )
            db.session.add(user)
            db.session.commit()

            # Create doctor profile
            doctor = Doctor(
                user_id=user.id,
                name=doc_data['name'],
                degree=doc_data['degree'],
                specialization=doc_data['specialization'],
                bio=doc_data['bio'],
                fees=doc_data['fees'],
                location=doc_data['location'],
                contact_info=doc_data['contact_info'],
                visit_types=doc_data['visit_types'],
                verified=doc_data['verified']
            )
            db.session.add(doctor)
            db.session.commit()

        print("Doctors seeded successfully!")

if __name__ == '__main__':
    seed_doctors()
