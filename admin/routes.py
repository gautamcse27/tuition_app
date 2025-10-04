from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import admin_bp
from models import Admin, Student, Tutor, TuitionRequirement, TutorProfile, db
from .forms import LoginForm, AdminRegisterForm


@admin_bp.route('/register', methods=['GET', 'POST'])
def register():
    if Admin.query.first():
        flash('Admin account already exists. Please login.', 'info')
        return redirect(url_for('admin.login'))
    form = AdminRegisterForm()
    if form.validate_on_submit():
        if Admin.query.filter_by(email=form.email.data).first():
            flash('Email already registered!', 'danger')
        else:
            admin = Admin(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)
            )
            db.session.add(admin)
            db.session.commit()
            flash('Admin registered successfully! Please login.', 'success')
            return redirect(url_for('admin.login'))
    return render_template('admin_register.html', form=form)


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    students = Student.query.all()
    tutors = Tutor.query.all()
    requirements = TuitionRequirement.query.all()
    return render_template('dashboard.html',
                           students=students,
                           tutors=tutors,
                           requirements=requirements)


@admin_bp.route('/approve_access/<int:req_id>')
@login_required
def approve_access(req_id):
    requirement = TuitionRequirement.query.get_or_404(req_id)
    requirement.approved = True
    db.session.commit()
    flash('Access approved for tutor.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/revoke_access/<int:req_id>')
@login_required
def revoke_access(req_id):
    requirement = TuitionRequirement.query.get_or_404(req_id)
    requirement.approved = False
    db.session.commit()
    flash('Access revoked for tutor.', 'warning')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/student/<int:student_id>')
@login_required
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('view_student.html', student=student)


@admin_bp.route('/toggle_student/<int:student_id>')
@login_required
def toggle_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.active = not getattr(student, 'active', True)
    db.session.commit()
    flash(f"Student {'enabled' if student.active else 'disabled'}.", 'info')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/remove_student/<int:student_id>')
@login_required
def remove_student(student_id):
    student = Student.query.get_or_404(student_id)
    TuitionRequirement.query.filter_by(student_id=student.id).delete()
    db.session.delete(student)
    db.session.commit()
    flash('Student and associated tuition requirements removed.', 'danger')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/toggle_tutor/<int:tutor_id>')
@login_required
def toggle_tutor(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)
    tutor.active = not getattr(tutor, 'active', True)
    db.session.commit()
    flash(f"Tutor {'enabled' if tutor.active else 'disabled'}.", 'info')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/remove_tutor/<int:tutor_id>')
@login_required
def remove_tutor(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)
    db.session.delete(tutor)
    db.session.commit()
    flash('Tutor and all related data removed.', 'danger')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/receipt_verification')
@login_required
def receipt_verification():
    pending_requirements = TuitionRequirement.query.filter(
        TuitionRequirement.receipt_data.isnot(None),
        TuitionRequirement.payment_verified == False
    ).all()
    return render_template('receipt_verification.html', pending_requirements=pending_requirements)


@admin_bp.route('/verify_payment/<int:req_id>')
@login_required
def verify_payment(req_id):
    req = TuitionRequirement.query.get_or_404(req_id)
    req.payment_verified = True
    req.tutor_id = req.tutor_id or current_user.id
    db.session.commit()
    flash('Payment verified. Details are unmasked to tutor.', 'success')
    return redirect(url_for('admin.receipt_verification'))


@admin_bp.route('/reject_payment/<int:req_id>')
@login_required
def reject_payment(req_id):
    req = TuitionRequirement.query.get_or_404(req_id)
    req.payment_verified = False
    db.session.commit()
    flash('Payment rejected.', 'danger')
    return redirect(url_for('admin.receipt_verification'))


@admin_bp.route('/tutor_assignments')
@login_required
def tutor_assignments():
    assignments = db.session.query(TuitionRequirement, TutorProfile).join(TutorProfile).all()
    return render_template('tutor_assignments.html', assignments=assignments)
