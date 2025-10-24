"""
app configurations
defined as class objects, used with `app.config.from_object(config_obj)`
"""
import os


def _normalize_db_url(url: str) -> str:
    # SQLAlchemy wants postgresql:// not postgres://
    return url.replace("postgres://", "postgresql://", 1) if url.startswith("postgres://") else url

class Base:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # flask app secret key
    if "FLASK_KEY" not in os.environ:
        raise RuntimeError("FLASK_KEY must be set")
    if "DATABASE_URL" not in os.environ:
        raise RuntimeError("DATABASE_URL must be set")
    SECRET_KEY = os.getenv("FLASK_KEY")
    # sqlite uri
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    assert isinstance(SQLALCHEMY_DATABASE_URI, str), "DATABASE_URL must be set in production"
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(SQLALCHEMY_DATABASE_URI)
    # talisman instance configs
    TALISMAN_FORCE_HTTPS = False      # sensible default; we’ll override in prod
    TALISMAN_CSP = {
        "default-src": "'self'",
        "img-src": ["'self'", "data:", "blob:"],
        "style-src": ["'self'"],      # tighten in prod if you don’t inline
        "script-src": ["'self'"],
        "font-src": ["'self'", "data:"],
        "connect-src": ["'self'"],
        "frame-ancestors": "'none'",
        "object-src": "'none'",
        "base-uri": "'self'",
        "form-action": "'self'",
    }

class Development(Base):
    DEBUG = True
    # Relax if you’re using inline styles/scripts while building:
    TALISMAN_CSP = {
        **Base.TALISMAN_CSP,
        "default-src": "'self'",
        "img-src": ["'self'", "data:", "blob:"],
        "style-src": ["'self'", "'unsafe-inline'"],  # tighten as you fix inline styles (or use nonces)
        "script-src": ["'self'"],
    }
    SECRET_KEY = "/csp-report"
    SQLALCHEMY_DATABASE_URI = "sqlite:///lakeblvd-home.db"
    TALISMAN_FORCE_HTTPS = False
    # FIXME: Setting content_security_policy_report_only to True also requires
    # a URI to be specified in content_security_policy_report_uri
    # NOTE: check how to setup uri
    # TALISMAN_REPORT_URI = ...
    TALISMAN_REPORT_ONLY = False

class Production(Base):
    TALISMAN_FORCE_HTTPS = True

class Testing(Base):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
