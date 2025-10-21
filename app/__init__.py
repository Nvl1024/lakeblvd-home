from os import environ
from flask import Flask
from .extensions import db, csrf, login_manager
from .auth import bp as auth_bp
from .home import bp as home_bp
from .profile import bp as profile_bp


def create_app():
    app = Flask(__name__)
    if environ.get('HEROKU_PROD_ENV'):
        SECRET_KEY = environ.get('FLASK_KEY')
        SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
        assert isinstance(SQLALCHEMY_DATABASE_URI, str), "DATABASE_URL not found"
        if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
                "postgres://", "postgresql://", 1
            )
    else:
        from config import section
        SECRET_KEY = section("App")["SECRET_KEY"]
        SQLALCHEMY_DATABASE_URI = "sqlite:///lakeblvd-home.db"
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)

    # Create tables in dev if needed
    with app.app_context():
        from .auth import models  # ensure models are imported
        # Configure Flask-Login user loader
        from .auth.models import User
        @login_manager.user_loader
        def load_user(user_id: str):  # pragma: no cover - tiny glue code
            try:
                return User.query.get(int(user_id))
            except (TypeError, ValueError):
                return None
        db.create_all()

    return app

app = create_app()
