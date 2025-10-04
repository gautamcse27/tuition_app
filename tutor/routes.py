from flask import render_template,session, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from . import tutor_bp
from models import Tutor, TutorProfile, TuitionRequirement, db
from forms import TutorLoginForm, TutorRegisterForm, TutorProfileForm
import os

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@tutor_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = TutorRegisterForm()
    if form.validate_on_submit():
        tutor = Tutor(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(tutor)
        db.session.commit()
        flash('Tutor registered successfully! Please login.', 'success')
        return redirect(url_for('tutor.login'))
    return render_template('tutor_register.html', form=form)




@tutor_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = TutorLoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('tutor.dashboard'))
    if form.validate_on_submit():
        tutor = None
        if form.email.data:
            tutor = Tutor.query.filter_by(email=form.email.data).first()
        elif form.phone.data:
            tutor = Tutor.query.filter_by(phone=form.phone.data).first()
        if tutor and check_password_hash(tutor.password_hash, form.password.data):
            login_user(tutor)
            session['tutor_id'] = tutor.id  # Sync session with logged-in tutor
            flash("Logged in successfully.", "success")
            return redirect(url_for('tutor.dashboard'))
        else:
            flash("Invalid email/phone or password.", "danger")
    return render_template('tutor_login.html', form=form)

@tutor_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('tutor.login'))


@tutor_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    tutor = current_user
    requirements = TuitionRequirement.query.filter_by(tutor_id=tutor.id).all()
    profile = TutorProfile.query.filter_by(tutor_id=tutor.id).first()
    form = TutorProfileForm(obj=profile)

    # Populate form if GET and profile exists
    if request.method == 'GET' and profile:
        form.subjects.data = ', '.join(profile.subjects) if profile.subjects else ''
        form.mode.data = profile.mode
        form.skill.data = profile.skill
        form.methodology.data = profile.methodology

    if form.validate_on_submit():
        if not profile:
            profile = TutorProfile(tutor_id=tutor.id)
        profile.subjects = [s.strip() for s in form.subjects.data.split(',')] if form.subjects.data else []
        profile.mode = form.mode.data
        profile.skill = form.skill.data
        profile.methodology = form.methodology.data
        db.session.add(profile)
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('tutor.dashboard'))

    return render_template('tutor_dashboard.html', tutor=tutor, requirements=requirements, form=form)


@tutor_bp.route('/upload_receipt/<int:req_id>', methods=['GET', 'POST'])
@login_required
def upload_receipt(req_id):
    requirement = TuitionRequirement.query.get_or_404(req_id)
    # Ensure only the assigned tutor uploads a receipt
    if requirement.tutor_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        file = request.files.get('receipt')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            requirement.receipt_data = file.read()
            requirement.receipt_filename = filename
            db.session.commit()
            flash('Receipt uploaded successfully. Waiting for admin verification.', 'info')
            return redirect(url_for('tutor.dashboard'))
        else:
            flash('Invalid or missing file. Allowed types: pdf, jpg, jpeg, png.', 'warning')
    return render_template('upload_receipt.html', requirement=requirement)
