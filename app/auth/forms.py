from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms import StringField, PasswordField, SubmitField, SelectField
from .models import User
from config import section

CSRF_SECRET = section("Form")['CSRF_SECRET']

def username_valid(form, field):
    """WTForms validator: raises ValidationError if username is not valid.

    Uses User.is_valid_name to decide validity. Keep this function side-effect free.
    """
    username = field.data or ""
    if not User.is_valid_name(username):
        raise ValidationError("This username is already taken.")

class RegisterForm(FlaskForm):
    username = StringField(
        label="Username", validators=[DataRequired(), username_valid])
    password = PasswordField(
        label="Enter your password:", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        label="Confirm your password:",
        validators=[DataRequired(),
                    EqualTo('password.data', message='password must match')]
                    )

class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    remember_me = SelectField(label="Remember me")
    submit = SubmitField(label="Submit")

# TODO: logout form with button confirmation
class LogoutForm(FlaskForm):
    confirm = SubmitField(label="Confirm")
    cancel = SubmitField(label="Cancel")
