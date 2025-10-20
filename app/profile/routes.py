"""
user profile page
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from ..auth.models import User
from ..auth.forms import LogoutForm
from .forms import ChangePasswordForm
from . import bp

@bp.route(f'/profile', methods=["GET", "POST"])
@login_required
def account():
    return render_template(
        'profile/account.html',
        user=current_user,
        )

@bp.route('/profile/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    change_password_form = ChangePasswordForm()
    if request.method == "POST":
        if change_password_form.validate_on_submit():
            user = current_user
            assert isinstance(user, User)
            # check if old password match
            current_password = change_password_form.current_password.data
            new_password = change_password_form.new_password.data
            if user.check_password(current_password):
                user.change_password(new_password)
                flash("password successfully updated")
                return redirect(url_for("profile.account"))
            else:
                flash("current password incorrect")
                raise RuntimeError("password incorrect")
        else:
            error = "; ".join(error for error in change_password_form.errors)
            raise RuntimeError(error)
    return render_template(
        "profile/change_password.html",
        change_password_form = change_password_form
        )
