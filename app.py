from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from config import Config
from models import db, User, Doctor, Appointment, Feedback, UserRole
from forms import RegisterForm, LoginForm, DoctorForm, AppointmentForm, DoctorRegisterForm, ProfileForm, SearchForm, RescheduleForm, InquiryForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate
from logger import setup_logger
import json

#admin details
# VALUES ('admin123', 'admin@example.com', 'pbkdf2:sha256:260000$TBTR0D4A0gvuaXHG$4fec38cacae6d2ceba7b49216c85af43c5670c8a0f2798b108b704c83c5c6d7a', '1234567890', 1)
#admin123:admin@123
#user1:user123
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Set up logger
logger = setup_logger()

# Set up mail (commented out as email system removed)
# mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Public pages ---
@app.route('/')
def index():
    docs = Doctor.query.order_by(Doctor.created_at.desc()).all()
    return render_template('index.html', doctors=docs)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/welcome')
def welcome():
    logger.info(f"Request received: {request.method} {request.path}")
    return jsonify({'message': 'Welcome to the Clinic Management System!'})

# --- User registration & login ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken', 'danger')
        elif User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'danger')
        else:
            hashed = generate_password_hash(form.password.data)
            role = UserRole.ADMIN if form.username.data == 'admin123' else UserRole(form.role.data)
            user = User(username=form.username.data, email=form.email.data,
                        password_hash=hashed, contact=form.contact.data, role=role)
            db.session.add(user)
            db.session.commit()
            flash('Registered successfully. Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/doctor_register', methods=['GET', 'POST'])
def doctor_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = DoctorRegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken', 'danger')
        elif User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'danger')
        else:
            hashed = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data,
                        password_hash=hashed, contact=form.contact.data, role=UserRole.DOCTOR)
            db.session.add(user)
            db.session.commit()
            # Create doctor profile
            visit_types = json.dumps([form.visit_types.data]) if form.visit_types.data != 'both' else json.dumps(['clinic', 'online'])
            doc = Doctor(
                user_id=user.id,
                name=form.name.data,
                degree=form.degree.data,
                specialization=form.specialization.data,
                bio=form.bio.data,
                fees=form.fees.data or 0.0,
                location=form.location.data,
                contact_info=form.contact_info.data,
                visit_types=visit_types,
                verified=False
            )
            db.session.add(doc)
            db.session.commit()
            flash('Doctor registration submitted. Awaiting admin approval.', 'success')
            return redirect(url_for('login'))
    return render_template('doctor_register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Logged in successfully', 'success')
            next_page = request.args.get('next') or url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('index'))

# --- Admin panel (doctor management) ---
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return decorated

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    doctors = Doctor.query.order_by(Doctor.created_at.desc()).all()
    users = User.query.order_by(User.id).all()
    return render_template('admin_panel.html', doctors=doctors, users=users,
                           admin_email=app.config['ADMIN_EMAIL'],
                           admin_contact=app.config['ADMIN_CONTACT'])

@app.route('/admin/add_doctor', methods=['GET','POST'])
@login_required
@admin_required
def add_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        visit_types = json.dumps([form.visit_types.data]) if form.visit_types.data != 'both' else json.dumps(['clinic', 'online'])
        doc = Doctor(
            name=form.name.data,
            degree=form.degree.data,
            specialization=form.specialization.data,
            bio=form.bio.data,
            fees=form.fees.data or 0.0,
            location=form.location.data,
            contact_info=form.contact_info.data,
            visit_types=visit_types,
            verified=True
        )
        db.session.add(doc)
        db.session.commit()
        flash('Doctor added', 'success')
        return redirect(url_for('admin_panel'))
    return render_template('add_doctor.html', form=form)

@app.route('/admin/approve_doctor/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def approve_doctor(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == UserRole.DOCTOR and hasattr(user, 'doctor_profile') and user.doctor_profile:
        user.doctor_profile.verified = True
        db.session.commit()
        flash(f'Doctor {user.doctor_profile.name} approved.', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/doctor/<int:doc_id>')
def doctor_profile(doc_id):
    doc = Doctor.query.get_or_404(doc_id)
    return render_template('doctor_profile.html', doc=doc)

# --- Appointment booking (only for logged-in users) ---
@app.route('/book/<int:doc_id>', methods=['GET','POST'])
@login_required
def book(doc_id):
    if current_user.is_admin:
        flash('Admins cannot book appointments. Please manage doctors from the admin panel.', 'warning')
        return redirect(url_for('admin_panel'))
    doc = Doctor.query.get_or_404(doc_id)
    if not doc.verified:
        flash('This doctor is not yet verified.', 'warning')
        return redirect(url_for('index'))
    form = AppointmentForm()
    if form.validate_on_submit():
        # Basic availability check (no duplicate for same doctor at same date+time)
        existing = Appointment.query.filter(
    Appointment.doctor_id == doc.id,
    Appointment.date == form.date.data,
    Appointment.time == form.time.data,
    Appointment.status != 'cancelled'
).first()

        if existing:
            flash('This slot is already taken. Choose another time.', 'warning')
        else:
            appt = Appointment(
                doctor_id=doc.id,
                patient_id=current_user.id,
                date=form.date.data,
                time=form.time.data,
                visit_type=form.visit_type.data,
                notes=form.notes.data,
                status='pending'
            )
            db.session.add(appt)
            db.session.commit()
            flash('Appointment requested. You can view in My Appointments.', 'success')
            return redirect(url_for('my_appointments'))
    return render_template('book_appoinment.html', doctor=doc, form=form)

@app.route('/my_appointments')
@login_required
def my_appointments():
    if current_user.is_admin:
        flash('Admins cannot view personal appointments. Please manage doctors from the admin panel.', 'warning')
        return redirect(url_for('admin_panel'))
    appts = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.date, Appointment.time).all()
    return render_template('my_appointments.html', appointments=appts)

@app.route('/cancel/<int:appt_id>')
@login_required
def cancel_appointment(appt_id):
    if current_user.is_admin:
        abort(403)
    appt = Appointment.query.get_or_404(appt_id)
    if appt.patient_id != current_user.id:
        abort(403)
    appt.status = 'cancelled'
    db.session.commit()
    flash('Appointment cancelled', 'info')
    return redirect(url_for('my_appointments'))

@app.route('/reschedule/<int:appt_id>', methods=['GET', 'POST'])
@login_required
def reschedule(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    if appt.patient_id != current_user.id:
        abort(403)
    if appt.status not in ['pending', 'confirmed']:
        flash('Cannot reschedule this appointment.', 'warning')
        return redirect(url_for('my_appointments'))
    form = RescheduleForm()
    if form.validate_on_submit():
        # Check availability
        existing = Appointment.query.filter(
            Appointment.doctor_id == appt.doctor_id,
            Appointment.date == form.date.data,
            Appointment.time == form.time.data,
            Appointment.status != 'cancelled',
            Appointment.id != appt_id
        ).first()
        if existing:
            flash('This slot is already taken. Choose another time.', 'warning')
        else:
            appt.date = form.date.data
            appt.time = form.time.data
            appt.notes = form.notes.data
            appt.reschedule_count += 1
            appt.status = 'pending'  # Reset to pending
            db.session.commit()
            flash('Appointment rescheduled.', 'success')
            return redirect(url_for('my_appointments'))
    return render_template('reschedule.html', form=form, appointment=appt)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.dob = form.dob.data
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('profile'))
    form.address.data = current_user.address
    form.city.data = current_user.city
    form.dob.data = current_user.dob
    return render_template('profile.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    doctors = []
    if form.validate_on_submit():
        query = Doctor.query.filter_by(verified=True)
        if form.specialization.data:
            query = query.filter(Doctor.specialization.ilike(f'%{form.specialization.data}%'))
        if form.city.data:
            query = query.filter(Doctor.location.ilike(f'%{form.city.data}%'))
        if form.min_fees.data:
            query = query.filter(Doctor.fees <= form.min_fees.data)
        if form.min_rating.data:
            query = query.filter(Doctor.rating >= form.min_rating.data)
        doctors = query.all()
    return render_template('search_results.html', form=form, doctors=doctors)

@app.route('/contact/<int:doc_id>', methods=['GET', 'POST'])
@login_required
def contact(doc_id):
    doc = Doctor.query.get_or_404(doc_id)
    form = InquiryForm()
    if form.validate_on_submit():
        flash('Inquiry submitted.', 'success')
        return redirect(url_for('doctor_profile', doc_id=doc_id))
    return render_template('contact_form.html', form=form, doctor=doc)

@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != UserRole.DOCTOR or not hasattr(current_user, 'doctor_profile') or not current_user.doctor_profile.verified:
        abort(403)
    appts = Appointment.query.filter_by(doctor_id=current_user.doctor_profile.id).order_by(Appointment.date, Appointment.time).all()
    return render_template('doctor_dashboard.html', appointments=appts)

@app.route('/accept_appointment/<int:appt_id>', methods=['POST'])
@login_required
def accept_appointment(appt_id):
    if current_user.role != UserRole.DOCTOR:
        abort(403)
    appt = Appointment.query.get_or_404(appt_id)
    if appt.doctor_id != current_user.doctor_profile.id:
        abort(403)
    appt.status = 'confirmed'
    appt.doctor_response = 'accept'
    db.session.commit()
    flash('Appointment accepted.', 'success')
    return redirect(url_for('doctor_dashboard'))

@app.route('/decline_appointment/<int:appt_id>', methods=['POST'])
@login_required
def decline_appointment(appt_id):
    if current_user.role != UserRole.DOCTOR:
        abort(403)
    appt = Appointment.query.get_or_404(appt_id)
    if appt.doctor_id != current_user.doctor_profile.id:
        abort(403)
    appt.status = 'cancelled'
    appt.doctor_response = 'decline'
    db.session.commit()
    flash('Appointment declined.', 'success')
    return redirect(url_for('doctor_dashboard'))

# --- Admin: view doctor's daily schedule ---
@app.route('/admin/schedule/<int:doc_id>')
@login_required
@admin_required
def admin_schedule(doc_id):
    # show today's schedule, or date passed via query
    date_str = request.args.get('date')
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date = datetime.utcnow().date()
    else:
        date = datetime.utcnow().date()
    appts = Appointment.query.filter_by(doctor_id=doc_id, date=date).order_by(Appointment.time).all()
    doc = Doctor.query.get_or_404(doc_id)
    doctors = Doctor.query.order_by(Doctor.created_at.desc()).all()
    users = User.query.order_by(User.id).all()
    return render_template('admin_panel.html', doctors=doctors, users=users, schedule=appts, admin_email=app.config['ADMIN_EMAIL'], admin_contact=app.config['ADMIN_CONTACT'])

@app.route('/admin/delete_doctor/<int:doc_id>', methods=['POST'])
@login_required
@admin_required
def delete_doctor(doc_id):
    doc = Doctor.query.get_or_404(doc_id)
    # Delete associated appointments first to avoid foreign key constraint
    Appointment.query.filter_by(doctor_id=doc_id).delete()
    db.session.delete(doc)
    db.session.commit()
    flash('Doctor deleted successfully', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin_users')
@login_required
@admin_required
def admin_users():
    users = User.query.order_by(User.id).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin_edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = ProfileForm()
    if form.validate_on_submit():
        user.address = form.address.data
        user.city = form.city.data
        user.dob = form.dob.data
        db.session.commit()
        flash('User updated.', 'success')
        return redirect(url_for('admin_users'))
    form.address.data = user.address
    form.city.data = user.city
    form.dob.data = user.dob
    return render_template('admin_edit_user.html', form=form, user=user)

@app.route('/admin_delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # Delete associated doctor profile if exists
    if hasattr(user, 'doctor_profile') and user.doctor_profile:
        Appointment.query.filter_by(doctor_id=user.doctor_profile.id).delete()
        db.session.delete(user.doctor_profile)
    # Delete associated appointments as patient
    Appointment.query.filter_by(patient_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin_users'))



# --- Error handlers ---
@app.errorhandler(403)
def forbidden(e):
    return render_template('404.html', message='Forbidden (403)'), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', message='Not found (404)'), 404

if __name__ == '__main__':
    app.run(debug=True)
