from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import LargeBinary
from flask_login import UserMixin
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)


class Student(db.Model):
    __tablename__ = 'student_registration'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column('mobile_no', db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    active = db.Column(db.Boolean, default=True)

    requirements = db.relationship('TuitionRequirement', backref='student', cascade='all, delete-orphan', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



class Tutor(db.Model, UserMixin):
    __tablename__ = 'tutor_registration'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column('mobile_no', db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    active = db.Column(db.Boolean, default=True)

    profile = db.relationship('TutorProfile', backref='tutor', cascade='all, delete-orphan', uselist=False)
    requirements = db.relationship(
        'TuitionRequirement',
        back_populates='tutor',
        lazy='dynamic',
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Optionally, if you want to customize is_active property based on active column:
    @property
    def is_active(self):
        return self.active

class TutorProfile(db.Model):
    __tablename__ = 'tutor_profile'

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor_registration.id'), unique=True, nullable=False)

    subjects = db.Column(db.ARRAY(db.String), nullable=False)
    mode = db.Column(db.String(10), nullable=False)
    skill = db.Column(db.String(20), nullable=False)
    methodology = db.Column(db.Text, nullable=False)


class TuitionRequirement(db.Model):
    __tablename__ = 'tuition_requirement'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_registration.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor_registration.id'), nullable=True)  # link to tutor_registration

    subject = db.Column(db.String(120), nullable=False)
    student_class = db.Column(db.String(50), nullable=False)
    mode = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    description = db.Column(db.String(300))
    pdf_data = db.Column(LargeBinary)
    approved = db.Column(db.Boolean, default=False)
    receipt_data = db.Column(LargeBinary)  # Store uploaded receipt file
    receipt_filename = db.Column(db.String(255))  # Optional original filename
    payment_verified = db.Column(db.Boolean, default=False)  # Admin approval flag

    tutor = db.relationship('Tutor', back_populates='requirements')


class AccessRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor_registration.id'), nullable=False)
    requirement_id = db.Column(db.Integer, db.ForeignKey('tuition_requirement.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # could be 'pending', 'approved', 'rejected'

    tutor = db.relationship('Tutor', backref=db.backref('access_requests', lazy=True))
    requirement = db.relationship('TuitionRequirement', backref=db.backref('access_requests', lazy=True))
