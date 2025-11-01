from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, TimeField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange
# --- Register Form ---
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=15)])
    role = SelectField('Role', choices=[('patient', 'Patient'), ('doctor', 'Doctor')], default='patient')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# --- Doctor Register Form ---
class DoctorRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=15)])
    name = StringField('Full Name', validators=[DataRequired()])
    degree = StringField('Degree', validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired(), Length(max=500)])
    fees = FloatField('Consultation Fees', validators=[Optional(), NumberRange(min=0)])
    location = StringField('City', validators=[Optional()])
    contact_info = TextAreaField('Additional Contact Info', validators=[Optional()])
    visit_types = SelectField('Visit Types', choices=[('clinic', 'Clinic'), ('online', 'Online'), ('both', 'Both')], default='clinic')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register as Doctor')

# --- Login Form ---
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# --- Profile Form ---
class ProfileForm(FlaskForm):
    address = StringField('Address', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    dob = DateField('Date of Birth', validators=[Optional()])
    submit = SubmitField('Update Profile')

# --- Doctor Form (admin only) ---
class DoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    degree = StringField('Degree', validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired(), Length(max=500)])
    fees = FloatField('Fees', validators=[Optional(), NumberRange(min=0)])
    location = StringField('City', validators=[Optional()])
    contact_info = TextAreaField('Contact Info', validators=[Optional()])
    visit_types = SelectField('Visit Types', choices=[('clinic', 'Clinic'), ('online', 'Online'), ('both', 'Both')], default='clinic')
    submit = SubmitField('Add Doctor')

# --- Search Form ---
class SearchForm(FlaskForm):
    specialization = StringField('Specialization', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    min_fees = FloatField('Max Fees', validators=[Optional(), NumberRange(min=0)])
    min_rating = FloatField('Min Rating', validators=[Optional(), NumberRange(min=0, max=5)])
    submit = SubmitField('Search')

# --- Appointment Form (for users) ---
class AppointmentForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    visit_type = SelectField('Visit Type', choices=[('clinic', 'Clinic Visit'), ('online', 'Online Consultation')], default='clinic')
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Book Appointment')

# --- Reschedule Form ---
class RescheduleForm(FlaskForm):
    date = DateField('New Date', validators=[DataRequired()])
    time = TimeField('New Time', validators=[DataRequired()])
    notes = TextAreaField('Reason for Reschedule', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Reschedule')

# --- Inquiry Form ---
class InquiryForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Send Inquiry')
