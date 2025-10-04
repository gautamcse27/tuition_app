from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length,Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=48, message="Username must be between 3 and 48 characters.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=6, max=128, message="Password must be at least 6 characters.")
    ])
    submit = SubmitField('Login')
class AdminRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField('Register')