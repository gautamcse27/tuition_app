from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectMultipleField,
    widgets,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from flask_wtf.file import FileField, FileAllowed


class StudentRegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=7, max=15)])
    password = PasswordField(
        'Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')]
    )
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class TutorRegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=7, max=15)])
    password = PasswordField(
        'Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')]
    )
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class StudentLoginForm(FlaskForm):
    email = StringField('Email (optional)', validators=[Optional(), Email()])
    phone = StringField('Phone (optional)', validators=[Optional(), Length(min=7, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate(self, *args, **kwargs):
        rv = super().validate(*args, **kwargs)
        if not rv:
            return False
        if not (self.email.data or self.phone.data):
            error_msg = 'Provide either email or phone number.'
            self.email.errors.append(error_msg)
            self.phone.errors.append(error_msg)
            return False
        return True


class TutorLoginForm(FlaskForm):
    email = StringField('Email (optional)', validators=[Optional(), Email()])
    phone = StringField('Phone (optional)', validators=[Optional(), Length(min=7, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate(self, *args, **kwargs):
        rv = super().validate(*args, **kwargs)
        if not rv:
            return False
        if not (self.email.data or self.phone.data):
            error_msg = 'Provide either email or phone number.'
            self.email.errors.append(error_msg)
            self.phone.errors.append(error_msg)
            return False
        return True


class TuitionRequirementForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    student_class = StringField('Class', validators=[DataRequired()])
    mode = SelectField(
        'Mode', choices=[('online', 'Online'), ('offline', 'Offline')], validators=[DataRequired()]
    )
    address = StringField('Address', validators=[Optional()])
    description = TextAreaField(
        'Requirement Details',
        validators=[DataRequired(), Length(max=300)],
        render_kw={"rows": 3}
    )
    pdf = FileField('Attach a PDF', validators=[
        FileAllowed(['pdf'], 'PDFs only!'),
        Optional()
    ])
    submit = SubmitField('Post Requirement')


# Custom MultiCheckboxField for selecting multiple subjects
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class TutorProfileForm(FlaskForm):
    subjects = StringField('Subjects Taught', validators=[DataRequired()])
    mode = SelectField(
        'Mode of Teaching',
        choices=[('online', 'Online'), ('offline', 'Offline'), ('both', 'Both')],
        validators=[DataRequired()],
    )
    skill = SelectField(
        'Skill Level',
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('expert', 'Expert')],
        validators=[DataRequired()],
    )
    methodology = TextAreaField(
        'Teaching Methodology',
        validators=[DataRequired(), Length(min=100, max=200)],
        render_kw={"rows": 4},
    )
    submit = SubmitField('Update Profile')
