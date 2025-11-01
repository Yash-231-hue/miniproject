# Clinic Appointment System

A web-based appointment booking system built with Flask, allowing patients to book appointments with doctors and administrators to manage doctors and view schedules.

## Features

### For Patients
- User registration and authentication
- Browse available doctors
- Book appointments with doctors
- View and cancel personal appointments
- Appointment status tracking (pending, approved, cancelled)
- **AI-Powered Chat Assistant**: Get instant answers about clinic services, appointment booking, working hours, insurance, and general health information

### For Administrators
- Secure admin login
- Add new doctors to the system
- Delete doctors (with associated appointments)
- View doctor schedules and appointments
- Manage doctor information

### AI Chat Assistant
- **24/7 Support**: Available anytime for instant responses
- **Smart Responses**: Handles queries about:
  - Clinic services and specializations
  - Appointment booking process
  - Working hours and location
  - Insurance and payment information
  - Emergency services
  - Doctor information
  - Contact details
- **User-Friendly Interface**: Modern chat interface with quick action buttons
- **Contextual Help**: Provides step-by-step guidance for common tasks

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS (Bootstrap), Jinja2 templates
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Migrations**: Flask-Migrate

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd clinic-appointment-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirement.txt
```

4. Set up the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Default Admin Account
- Username: admin123
- Password: admin@123

### User Registration
1. Visit the homepage
2. Click "Register" to create a new account
3. Fill in the registration form with username, email, password, and contact information

### Booking Appointments
1. Log in as a regular user
2. Browse doctors on the homepage
3. Click on a doctor's profile
4. Click "Book Appointment" and fill in the appointment form
5. Appointments are initially set to "pending" status

### Using the Chat Assistant
1. Click on "Chat Assistant" in the navigation bar or homepage
2. Ask questions about clinic services, appointment booking, or general information
3. Use quick action buttons for common queries
4. Get instant responses and guidance

### Admin Functions
1. Log in with admin credentials
2. Access the Admin Panel
3. Add new doctors using the "Add Doctor" button
4. View doctor schedules by clicking "Schedule" next to each doctor
5. Delete doctors if needed (this will also remove associated appointments)

## Project Structure

```
clinic-appointment-system/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── forms.py              # WTForms definitions
├── requirement.txt       # Python dependencies
├── migrations/           # Database migrations
├── templates/            # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin_panel.html
│   ├── add_doctor.html
│   ├── doctor_profile.html
│   ├── book_appoinment.html
│   ├── my_appointments.html
│   ├── chatbot.html       # AI-powered chat assistant interface
│   └── 404.html
└── README.md
```

## Security Features

- Password hashing using Werkzeug
- Role-based access control (admin vs regular users)
- CSRF protection on forms
- Session management with Flask-Login
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
