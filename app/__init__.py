from os import environ
import warnings
from flask import Flask
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
# load environment variables from .env file
load_dotenv(override=False)  # existing env vars prioritize
from .app_config import Development, Production, Testing
from .extensions import db, csrf, login_manager, migrate
from .auth import bp as auth_bp
from .home import bp as home_bp
from .profile import bp as profile_bp


CONFIGS = {
    'dev': Development,
    'prod': Production,
    'test': Testing
    }

def create_app():   
    app = Flask(__name__)
    app_env = environ.get('APP_ENV')
    # HARDCODE: setup app env on heroku, then remove if condition
    if environ.get('HEROKU_PROD_ENV'):
        app_env = 'prod'
    elif app_env not in CONFIGS.keys():
        warnings.warn(f"app env name {app_env or 'empty'} not defined, default use dev")
    assert isinstance(app_env, str)
    app.config.from_object(CONFIGS.get(app_env, Development))

    # to trust proxy headers injected by PaaS
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1, # 2 in case placing cloudflare in front
        x_proto=1, x_host=1, x_port=1)
    # Talisman CSP and security enhancement
    Talisman(
        app,
        content_security_policy=app.config["TALISMAN_CSP"],
        content_security_policy_report_only=app.config.get("TALISMAN_REPORT_ONLY", False),
        content_security_policy_report_uri=app.config.get("TALISMAN_REPORT_URI"),
        content_security_policy_nonce_in=["script-src", "style-src"],
        force_https=app.config.get("TALISMAN_FORCE_HTTPS"),
        strict_transport_security=app.config.get("TALISMAN_FORCE_HTTPS"),
        strict_transport_security_max_age=31536000,
        frame_options='DENY',
        referrer_policy='no-referrer',
        permissions_policy={"geolocation": "()"},
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)

    # Create tables in dev if needed
    with app.app_context():
        from . import models  # ensure models are imported
        # Configure Flask-Login user loader
        from .models import User
        @login_manager.user_loader
        def load_user(user_id: str):  # pragma: no cover - tiny glue code
            try:
                return User.query.get(int(user_id))
            except (TypeError, ValueError):
                return None
        db.create_all()

    return app

app = create_app()
