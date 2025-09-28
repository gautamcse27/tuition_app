from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import LargeBinary

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student_registration'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column('mobile_no', db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Tutor(db.Model):
    __tablename__ = 'tutor_registration'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column('mobile_no', db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class TuitionRequirement(db.Model):
    __tablename__ = 'tuition_requirement'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_registration.id'), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    student_class = db.Column(db.String(50), nullable=False)
    mode = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    description = db.Column(db.String(300))  # For 3-4 sentence details
    pdf_data = db.Column(LargeBinary)        # Encrypted binary file data stored in DB

    student = db.relationship('Student', backref=db.backref('requirements', lazy=True))


class TutorProfile(db.Model):
    __tablename__ = 'tutor_profile'

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor_registration.id', ondelete='CASCADE'), unique=True, nullable=False)

    subjects = db.Column(db.ARRAY(db.String), nullable=False)
    mode = db.Column(db.String(10), nullable=False)
    skill = db.Column(db.String(20), nullable=False)
    methodology = db.Column(db.Text, nullable=False)

    tutor = db.relationship('Tutor', backref=db.backref('profile', uselist=False))
