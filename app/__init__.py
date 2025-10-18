from flask import Flask
from .auth import bp as auth_bp
from config import section
from .extensions import db, csrf, login_manager
from os import environ
from .home import bp as home_bp

def create_app():
    app = Flask(__name__)
    SECRET_KEY = section("App")["SECRET_KEY"]
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL") or "sqlite:///lakeblvd-home.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)

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
