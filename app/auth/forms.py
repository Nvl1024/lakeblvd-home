from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from .models import User


def username_valid(form, field):
    """WTForms validator: raises ValidationError if username is not valid.

    Uses User.is_valid_name to decide validity. Keep this function side-effect free.
    """
    username = field.data or ""
    if not User.is_valid_name(username):
        raise ValidationError("This username is already taken.")

class RegisterForm(FlaskForm):
    username = StringField(
        label="Username:",
        validators=[
            DataRequired(), username_valid])
    password = PasswordField(
        label="Enter your password:",
        validators=[
            DataRequired(),
            Length(min=8, message='password length at least 8 characters')])
    confirm_password = PasswordField(
        label="Confirm your password:",
        validators=[DataRequired(),
                    EqualTo('password', message='password must match')]
                    )
    submit = SubmitField(label="Submit")

class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    remember_me = BooleanField(label="Remember me")
    submit = SubmitField(label="Submit")

class LogoutForm(FlaskForm):
    submit = SubmitField(label="Confirm")
