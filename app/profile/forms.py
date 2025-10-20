from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms import PasswordField, SubmitField

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current password:")
    new_password = PasswordField("New password:")
    confirm_password = PasswordField("Confirm password:")
    submit = SubmitField("Submit")

