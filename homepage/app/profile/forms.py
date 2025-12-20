from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, AnyOf
from wtforms import BooleanField, PasswordField, SubmitField

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current password:")
    new_password = PasswordField("New password:")
    confirm_password = PasswordField(
        "Confirm password:",
        validators=[DataRequired(), EqualTo('new_password', message='password must match')])
    submit = SubmitField("Submit")

class DeleteProfileForm(FlaskForm):
    confirm_delete = BooleanField(
        label="I confirm to permanently delete my account.",
        validators=[AnyOf([True])])
    submit = SubmitField("Submit")