from flask import flash, render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required
from . import bp
from ..extensions import db
from .forms import LoginForm, RegisterForm, LogoutForm
from .models import User


@bp.route('/login', methods=["GET", "POST"])
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
    return render_template("login.html", login_form=form)

@bp.route('/register', methods=["GET", "POST"])
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
    return render_template("register.html", register_form=form)

@bp.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        if form.confirm.data:
            logout_user()
            flash("You have been logged out.")
            return redirect(url_for('home.index'))
        if form.cancel.data:
            return redirect(url_for('home.index'))
    return render_template("logout.html", logout_form=form)