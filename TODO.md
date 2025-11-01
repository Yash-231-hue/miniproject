# TODO: Implement Clinic Management Features

## 1. Update Models (models.py)
- [ ] Add role enum to User model (patient, doctor, admin)
- [ ] Add profile fields to User: address, city, dob
- [ ] Add to Doctor: user_id, availability (JSON), fees, rating, location, contact_info, verified, visit_types
- [ ] Add to Appointment: visit_type, notes, reschedule_count, doctor_response
- [ ] New Feedback model: user_id, doctor_id, rating, comment
- [ ] Add relationships: User.doctor_profile, User.feedbacks, Doctor.feedbacks

## 2. Update Forms (forms.py)
- [ ] New DoctorRegisterForm for doctor signup
- [ ] Update RegisterForm: Add role selection, conditional fields
- [ ] New ProfileForm for profile updates
- [ ] New SearchForm for doctor search
- [ ] New RescheduleForm for rescheduling
- [ ] New InquiryForm for contact
- [ ] Update AppointmentForm: Add visit_type

## 3. Update Config (config.py)
- [ ] Add MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD for Flask-Mail

## 4. Update Requirements (requirement.txt)
- [ ] Add flask-mail

## 5. Update App Logic (app.py)
- [ ] Update register/login for roles
- [ ] New /doctor_register route
- [ ] New /profile route
- [ ] New /search route
- [ ] Update /book route with visit_type and availability
- [ ] New /reschedule/<appt_id> route
- [ ] New /doctor_dashboard route
- [ ] Update admin_panel with user management
- [ ] New /admin/approve_doctor/<user_id> route
- [ ] New /contact/<doc_id> route (inquiry form)
- [ ] Update my_appointments with reschedule
- [ ] Add email notifications (Flask-Mail integration)
- [ ] Update index with search bar

## 6. Create/Update Templates
- [x] New search_results.html
- [x] New doctor_register.html
- [x] New profile.html
- [x] Update index.html (add search)
- [x] Update doctor_profile.html (add contact, ratings)
- [x] Update my_appointments.html (add reschedule)
- [x] New doctor_dashboard.html
- [x] Update admin_panel.html (add user sections)
- [x] New contact_form.html
- [x] Update book_appoinment.html (add visit_type, slots)

## 7. Migration and Setup
- [ ] Run Alembic migration for model changes
- [ ] Install new dependencies

## 8. Testing
- [ ] Test role registrations (patient/doctor)
- [ ] Test booking, rescheduling, search
- [ ] Test admin approvals, notifications
- [ ] Verify DB integrity and email sending
