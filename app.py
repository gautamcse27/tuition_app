import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort, Response
from models import db, Student, Tutor, TuitionRequirement, TutorProfile
from forms import (
    StudentRegisterForm,
    TutorRegisterForm,
    StudentLoginForm,
    TutorLoginForm,
    TuitionRequirementForm,
    TutorProfileForm,
)
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Use a secure 32-byte base64 encoded key, saved securely in environment/config
secret_key = b'QJ3v7gmvuN_azg7BALhL6O_AdcFeTsFdlnlSaYP7Z7w='  # replace with your own key

fernet = Fernet(secret_key)

db.init_app(app)
migrate = Migrate(app, db)

#with app.app_context():
 #   db.create_all()

@app.route('/')
def home():
    return 'Tuition App Running'
    #tuition_requirements = TuitionRequirement.query.order_by(TuitionRequirement.created_at.desc()).all()
    #return render_template('home.html', tuition_requirements=tuition_requirements)


@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    form = StudentRegisterForm()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        student.password_hash = generate_password_hash(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash("Student registered successfully! Please login.", "success")
        return redirect(url_for('student_login'))
    return render_template('student_register.html', form=form)


@app.route('/tutor/register', methods=['GET', 'POST'])
def tutor_register():
    form = TutorRegisterForm()
    if form.validate_on_submit():
        tutor = Tutor(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        tutor.password_hash = generate_password_hash(form.password.data)
        db.session.add(tutor)
        db.session.commit()
        flash("Tutor registered successfully! Please login.", "success")
        return redirect(url_for('tutor_login'))
    return render_template('tutor_register.html', form=form)


@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    form = StudentLoginForm()
    if form.validate_on_submit():
        user = None
        if form.email.data:
            user = Student.query.filter_by(email=form.email.data).first()
        elif form.phone.data:
            user = Student.query.filter_by(phone=form.phone.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['student_id'] = user.id
            flash("Logged in successfully.", "success")
            return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid email/phone or password.", "danger")
    return render_template('student_login.html', form=form)


@app.route('/tutor/login', methods=['GET', 'POST'])
def tutor_login():
    form = TutorLoginForm()
    if form.validate_on_submit():
        user = None
        if form.email.data:
            user = Tutor.query.filter_by(email=form.email.data).first()
        elif form.phone.data:
            user = Tutor.query.filter_by(phone=form.phone.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['tutor_id'] = user.id
            flash("Logged in successfully.", "success")
            return redirect(url_for('tutor_dashboard'))
        else:
            flash("Invalid email/phone or password.", "danger")
    return render_template('tutor_login.html', form=form)


@app.route('/student/dashboard', methods=['GET', 'POST'])
def student_dashboard():
    if 'student_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('student_login'))
    student_id = session.get('student_id')
    student = Student.query.get_or_404(student_id)

    form = TuitionRequirementForm()
    if form.validate_on_submit():
        address = form.address.data if form.mode.data == 'offline' else None

        pdf_data = None
        if form.pdf.data:
            file_bytes = form.pdf.data.read()
            pdf_data = fernet.encrypt(file_bytes)

        req = TuitionRequirement(
            student_id=student.id,
            subject=form.subject.data,
            student_class=form.student_class.data,
            mode=form.mode.data,
            address=address,
            description=form.description.data,
            pdf_data=pdf_data,
        )
        db.session.add(req)
        db.session.commit()
        flash("Tuition requirement posted!", "success")
        return redirect(url_for('student_dashboard'))

    requirements = TuitionRequirement.query.filter_by(student_id=student.id).all()
    return render_template('student_dashboard.html', student=student, form=form, requirements=requirements)


@app.route('/requirement_pdf/<int:req_id>')
def requirement_pdf(req_id):
    req = TuitionRequirement.query.get_or_404(req_id)
    if not req.pdf_data:
        abort(404)
    decrypted_pdf = fernet.decrypt(req.pdf_data)
    return Response(decrypted_pdf, mimetype='application/pdf')


@app.route('/tutor/dashboard', methods=['GET', 'POST'])
def tutor_dashboard():
    if 'tutor_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('tutor_login'))
    tutor_id = session.get('tutor_id')
    tutor = Tutor.query.get_or_404(tutor_id)

    form = TutorProfileForm()
    profile = TutorProfile.query.filter_by(tutor_id=tutor.id).first()

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
        return redirect(url_for('tutor_dashboard'))

    return render_template('tutor_dashboard.html', tutor=tutor, form=form)


@app.route('/student/logout')
def student_logout():
    session.pop('student_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('student_login'))


@app.route('/tutor/logout')
def tutor_logout():
    session.pop('tutor_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('tutor_login'))


@app.route('/requirements')
def all_requirements():
    page = request.args.get('page', 1, type=int)
    per_page = 9
    pagination = TuitionRequirement.query.order_by(TuitionRequirement.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    requirements = pagination.items
    return render_template('all_requirements.html', requirements=requirements, pagination=pagination)


@app.route('/student/requirement/close/<int:req_id>', methods=['POST'])
def close_requirement(req_id):
    if 'student_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('student_login'))

    student_id = session.get('student_id')
    req = TuitionRequirement.query.get_or_404(req_id)
    if req.student_id != student_id:
        abort(403)

    db.session.delete(req)
    db.session.commit()
    flash("Tuition requirement closed and removed successfully.", "success")
    return redirect(url_for('student_dashboard'))


@app.route('/payment/<int:req_id>')
def payment(req_id):
    if 'tutor_id' not in session:
        flash("Please login as tutor to make payment.", "warning")
        return redirect(url_for('tutor_login'))

    requirement = TuitionRequirement.query.get_or_404(req_id)
    student = requirement.student

    return render_template('payment.html', req_id=req_id, student=student, requirement=requirement)


if __name__ == '__main__':
    app.run(debug=True)
