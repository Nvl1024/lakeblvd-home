from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# Declare extensions without binding to an app; bind in create_app
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()