import os
from flask import flash, render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required
from . import bp
from .. import limiter
from ..extensions import db
from .forms import LoginForm, RegisterForm, LogoutForm
from ..models import User


REQUIRE_INVITATION = os.getenv('REQUIRE_INVITATION', 'false').lower() == 'true'

@bp.route('/login', methods=["GET", "POST"])
@limiter.limit("")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.name == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home.index'))
        flash("Incorrect username or password.")
    elif request.method == "POST":
        # Only flash errors on POST
        for field, errors in form.errors.items():
            for err in errors:
                flash(f"{field}: {err}")
    return render_template("auth/login.html", login_form=form)

@bp.route('/register', methods=["GET", "POST"])
@limiter.limit("5 per hour")
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.username.data)
        user.set_password(str(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for('auth.login'))
    elif request.method == "POST":
        for field, errors in form.errors.items():
            for err in errors:
                flash(f"{field}: {err}")
    return render_template(
        "auth/register.html",
        register_form=form,
        require_invitation=REQUIRE_INVITATION)

@bp.route('/logout', methods=["GET", "POST"])
@limiter.limit("")
@login_required
def logout():
    form = LogoutForm()
    # FIXME: confirm button doesn't respond, possibly due to validation error
    if request.method == "POST":
        if form.validate_on_submit():
            logout_user()
            flash("You have been logged out.")
            return redirect(url_for('home.index'))
        else:
            error_msg = ';'.join(error for error in form.errors)
            # flash(error_msg)
            raise RuntimeError(error_msg)
    return render_template("auth/logout.html", logout_form=form)
