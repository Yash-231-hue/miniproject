# Test Documentation for Clinic Management System

This document outlines the test cases for the Clinic Management System Flask application. Tests are categorized by feature and include manual testing steps, expected outcomes, and any automated test suggestions (using pytest or Flask's test client). All tests assume the application is running with a MySQL database (clinicdb) and seeded with sample data (e.g., doctors like Dr. John Smith).

## Prerequisites
- Run `flask run` to start the server (default: http://127.0.0.1:5000).
- Database seeded with sample doctors (via `python seed_doctors.py`).
- Admin user: username `admin123`, password `admin@123`.
- Sample patient user: Register a new patient or use seeded data if available.
- Email testing: Use a test SMTP server (e.g., Mailtrap) or mock emails in code for verification.

## 1. User Registration and Login
### Test Case 1.1: Patient Registration
- **Steps**:
  1. Navigate to `/register`.
  2. Fill form: username (unique, e.g., `testpatient`), email (valid, unique), contact (10-15 digits), role=Patient, password (min 6 chars), confirm password.
  3. Submit.
- **Expected Outcome**:
  - Success flash: "Registered successfully. Please login."
  - Redirect to `/login`.
  - User record in DB with role=Patient.
- **Edge Cases**:
  - Duplicate username/email: Flash "Username already taken" or "Email already registered".
  - Invalid password length: Form validation error.
- **Automated Test Suggestion**: Use Flask test client to POST form data and assert redirect/status.

### Test Case 1.2: Doctor Registration
- **Steps**:
  1. Navigate to `/doctor_register`.
  2. Fill form: username/email/contact (unique), name/degree/specialization/bio (required), fees/location/contact_info (optional), visit_types (clinic/online/both), password.
  3. Submit.
- **Expected Outcome**:
  - Success flash: "Doctor registration submitted. Awaiting admin approval."
  - Redirect to `/login`.
  - User (role=Doctor) and Doctor profile (verified=False) created in DB.
- **Edge Cases**:
  - Duplicate credentials: Flash error.
  - Missing required fields: Form validation.
- **Automated Test Suggestion**: POST to `/doctor_register`, query DB for unverified Doctor.

### Test Case 1.3: Admin Registration
- **Steps**:
  1. Navigate to `/register`.
  2. Use username `admin123`, valid email/contact, role=Patient (auto-upgrades), password.
  3. Submit and login.
- **Expected Outcome**:
  - User created with role=Admin (due to username check in app.py).
  - Access to `/admin` granted.
- **Edge Cases**: Non-admin username defaults to Patient.

### Test Case 1.4: Login
- **Steps**:
  1. Navigate to `/login`.
  2. Enter valid username/password (e.g., admin123/admin@123).
  3. Submit.
- **Expected Outcome**:
  - Success flash: "Logged in successfully".
  - Redirect to `/` or next page.
  - Session active (current_user accessible).
- **Edge Cases**:
  - Invalid credentials: Flash "Invalid credentials".
  - Already logged in: Redirect to `/`.
- **Automated Test Suggestion**: Test client POST, assert session user.

### Test Case 1.5: Logout
- **Steps**:
  1. Login as any user.
  2. Navigate to `/logout`.
- **Expected Outcome**:
  - Flash "Logged out".
  - Redirect to `/`.
  - Session cleared.
- **Automated Test Suggestion**: POST to logout, assert no current_user.

## 2. Doctor Management (Admin Only)
### Test Case 2.1: Admin Panel Access
- **Steps**:
  1. Login as admin123.
  2. Navigate to `/admin`.
- **Expected Outcome**:
  - Displays list of doctors (seeded ones visible).
  - Admin contact info shown.
- **Edge Cases**:
  - Non-admin access: 403 Forbidden.

### Test Case 2.2: Add Doctor (Admin)
- **Steps**:
  1. Login as admin.
  2. Go to `/admin/add_doctor`.
  3. Fill DoctorForm: name/degree/specialization/bio (required), fees/location/etc. (optional), visit_types.
  4. Submit.
- **Expected Outcome**:
  - Flash "Doctor added".
  - Redirect to `/admin`.
  - New Doctor in DB with verified=True (no user account).
- **Edge Cases**: Missing fields: Form validation.

### Test Case 2.3: Approve Doctor
- **Steps**:
  1. Register a doctor (unverified).
  2. Login as admin, go to `/admin`.
  3. Click approve for the doctor (POST to `/admin/approve_doctor/<user_id>`).
- **Expected Outcome**:
  - Doctor.verified = True.
  - Flash "Doctor [name] approved."
  - Redirect to `/admin`.
- **Edge Cases**: Non-doctor or verified already: No change.

### Test Case 2.4: Delete Doctor
- **Steps**:
  1. Login as admin.
  2. In `/admin`, POST to `/admin/delete_doctor/<doc_id>`.
- **Expected Outcome**:
  - Doctor and associated appointments deleted.
  - Flash "Doctor deleted successfully".
- **Edge Cases**: Non-existent ID: 404.

### Test Case 2.5: View Schedule
- **Steps**:
  1. Login as admin.
  2. Go to `/admin/schedule/<doc_id>` (optional ?date=YYYY-MM-DD).
- **Expected Outcome**:
  - Shows appointments for the date/doctor.
- **Edge Cases**: Invalid date: Defaults to today.

## 3. Appointment Booking and Management
### Test Case 3.1: Book Appointment (Patient)
- **Steps**:
  1. Login as patient.
  2. Go to `/doctor/<doc_id>` (verified doctor).
  3. Click book: `/book/<doc_id>`.
  4. Fill AppointmentForm: date/time (future, available slot), visit_type, notes.
  5. Submit.
- **Expected Outcome**:
  - Availability check passes (no duplicate slot).
  - Appointment created (status=pending).
  - Flash "Appointment requested...".
  - Email sent (check logs or test server).
  - Redirect to `/my_appointments`.
- **Edge Cases**:
  - Unverified doctor: Flash warning, redirect to index.
  - Admin booking: Flash warning, redirect to admin.
  - Taken slot: Flash "This slot is already taken".
  - Invalid date/time: Form validation.

### Test Case 3.2: View My Appointments
- **Steps**:
  1. Login as patient.
  2. Go to `/my_appointments`.
- **Expected Outcome**:
  - Lists patient's appointments (sorted by date/time).
- **Edge Cases**: Admin: Flash warning, redirect to admin.

### Test Case 3.3: Cancel Appointment
- **Steps**:
  1. Login as patient with pending/confirmed appt.
  2. In `/my_appointments`, click cancel: GET `/cancel/<appt_id>`.
- **Expected Outcome**:
  - Status = 'cancelled'.
  - Email sent.
  - Flash "Appointment cancelled".
  - Redirect to `/my_appointments`.
- **Edge Cases**:
  - Not owner: 403.
  - Admin: 403.

### Test Case 3.4: Reschedule Appointment
- **Steps**:
  1. Login as patient with pending/confirmed appt.
  2. In `/my_appointments`, click reschedule: `/reschedule/<appt_id>`.
  3. Fill RescheduleForm: new date/time (available), notes.
  4. Submit.
- **Expected Outcome**:
  - Updates date/time/notes, reschedule_count +=1, status=pending.
  - Email sent.
  - Flash "Appointment rescheduled."
- **Edge Cases**:
  - Invalid status (e.g., cancelled): Flash warning.
  - Taken slot: Flash "This slot is already taken".
  - Not owner: 403.

## 4. Doctor Dashboard
### Test Case 4.1: Access Doctor Dashboard
- **Steps**:
  1. Login as verified doctor (e.g., dr_smith/doctor123).
  2. Go to `/doctor_dashboard`.
- **Expected Outcome**:
  - Lists doctor's appointments (sorted).
- **Edge Cases**:
  - Unverified/non-doctor: 403.

### Test Case 4.2: Accept Appointment
- **Steps**:
  1. Login as doctor.
  2. In dashboard, POST to `/accept_appointment/<appt_id>` (pending appt).
- **Expected Outcome**:
  - Status = 'confirmed', doctor_response = 'accept'.
  - Email to patient.
  - Flash "Appointment accepted."
- **Edge Cases**: Not owner's appt: 403.

### Test Case 4.3: Decline Appointment
- **Steps**:
  1. Similar to accept, but POST to `/decline_appointment/<appt_id>`.
- **Expected Outcome**:
  - Status = 'cancelled', doctor_response = 'decline'.
  - Email to patient.
  - Flash "Appointment declined."

## 5. Search and Profile
### Test Case 5.1: Doctor Search
- **Steps**:
  1. Go to `/search`.
  2. Fill SearchForm: specialization (e.g., Cardiology), city (Mumbai), max fees (2000), min rating (4.0).
  3. Submit.
- **Expected Outcome**:
  - Filtered verified doctors displayed in `/search_results.html`.
- **Edge Cases**: No matches: Empty list.

### Test Case 5.2: Update Profile
- **Steps**:
  1. Login as user.
  2. Go to `/profile`.
  3. Fill ProfileForm: address, city, dob.
  4. Submit.
- **Expected Outcome**:
  - User fields updated.
  - Flash "Profile updated."
- **Edge Cases**: Optional fields blank: No error.

### Test Case 5.3: Contact Doctor (Inquiry)
- **Steps**:
  1. Login as patient.
  2. Go to `/doctor/<doc_id>`.
  3. Click contact: `/contact/<doc_id>`.
  4. Fill InquiryForm: message.
  5. Submit.
- **Expected Outcome**:
  - Email sent to doctor's contact_info (or admin).
  - Flash "Inquiry sent."
  - Redirect to doctor profile.
- **Edge Cases**: Invalid email: Log error, flash "Failed to send".

## 6. Feedback and Ratings
### Test Case 6.1: Submit Feedback
- **Steps**:
  1. (Assume post-appointment) Add route/form for feedback (not implemented yet).
  2. Submit rating (1-5), comment.
- **Expected Outcome**:
  - Feedback record created.
  - Doctor rating updated (average).
- **Note**: Implement `/feedback/<appt_id>` route if needed.

## 7. Error Handling and Security
### Test Case 7.1: 403 Forbidden
- **Steps**: Access protected route (e.g., `/admin`) as non-admin.
- **Expected Outcome**: Render 404.html with "Forbidden (403)".

### Test Case 7.2: 404 Not Found
- **Steps**: Navigate to invalid URL (e.g., `/invalid`).
- **Expected Outcome**: Render 404.html with "Not found (404)".

### Test Case 7.3: Email Notifications
- **Steps**: Perform actions triggering emails (book/cancel/reschedule/accept).
- **Expected Outcome**:
  - Emails queued/sent (verify in test SMTP or logs).
  - No crash on failure (logged error).
- **Edge Cases**: Invalid MAIL config: Graceful fallback.

## 8. Integration Tests
- **Database Integrity**: After migrations/seeding, query tables (users, doctors, appointments, feedbacks) in MySQL Workbench. Verify relationships (e.g., Doctor.user_id FK).
- **End-to-End**: Register patient → Book appt → Doctor accepts → Patient views confirmed appt.
- **Performance**: Search with 10+ doctors; ensure <2s response.
- **Security**: Test SQL injection (forms sanitized via WTForms), XSS (escape outputs in templates).

## Automated Testing Setup
- Install pytest: `pip install pytest pytest-flask`.
- Create `test_app.py` with Flask test client.
- Example:
  ```python
  import pytest
  from app import app, db

  @pytest.fixture
  def client():
      app.config['TESTING'] = True
      with app.test_client() as client:
          with app.app_context():
              db.create_all()
              yield client
              db.drop_all()

  def test_register(client):
      rv = client.post('/register', data={
          'username': 'test', 'email': 'test@example.com', 'contact': '1234567890',
          'role': 'patient', 'password': 'testpass', 'confirm_password': 'testpass'
      })
      assert rv.status_code == 302  # Redirect
  ```
- Run: `pytest test_app.py -v`.

## Coverage
- Aim for 80%+ code coverage (use pytest-cov).
- Focus: Routes, forms, DB operations, email sending.

Last Updated: [Current Date]
