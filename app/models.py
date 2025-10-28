"""
models across the website
"""
import datetime
import ulid
from flask_login import UserMixin
from enum import Enum
from sqlalchemy import Enum as SaEnum
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


# MIXINS

class TimestampMixin:
  created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
  def update_time(self):
    self.updated_at = datetime.datetime.now()

class IdMixin:
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class UlidMixin:
  id = db.Column(db.String(26), default=str(ulid.ULID()), primary_key=True)

class MarkdownMixin(UlidMixin, TimestampMixin):
  title = db.Column(db.String, default="Untitled", nullable=False)
  content = db.Column(db.String, default="", nullable=False)
  edited = db.Column(db.Boolean, default=False, nullable=False)

  def update_title(self, new_title: str):
    self.title = new_title
    self.edited = True
    self.update_time()

  def update_content(self, new_content: str):
    self.content = new_content
    self.edited = True
    self.update_time()

# MODEL CLASSES
# USER AUTHENTICATION

# definition of user roles
class UserRoles(Enum):
  default = "default"
  admin = "admin"
  beta = "beta"

class User(IdMixin, UserMixin, TimestampMixin, db.Model):
  __tablename__ = "user_table"
  name = db.Column(db.String(100), unique=True)
  password_hash = db.Column(db.String(255))
  invite_code = db.Column(db.ForeignKey("invite_code_table.id"))
  role = db.Column(
    SaEnum(UserRoles, name="role", native_enum=True),
    nullable=False, default=UserRoles.default
    )

  def set_password(self, password: str) -> None:
    """Hash and store a plaintext password into `hash`."""
    self.password_hash = generate_password_hash(password)

  def check_password(self, password: str) -> bool:
    """Verify a plaintext password against the stored hash."""
    if not self.password_hash:
      return False
    return check_password_hash(self.password_hash, password)

  def change_password(self, password: str) -> None:
    self.password_hash = generate_password_hash(password)

  @staticmethod
  def is_valid_name(username: str) -> bool:
    """Return True if the username is available/valid; False otherwise.
    Adjust logic as needed (e.g., add regex/length checks).
    """
    exists = User.query.filter(User.name == username).first() is not None
    return not exists

  def __repr__(self) -> str:
    return f"<User id={self.id} name={self.name}>"

# REGISTRATION CONTROL

class InviteCode(UlidMixin, TimestampMixin, db.Model):
  __tablename__ = "invite_code_table"
  role = db.Column(
    SaEnum(UserRoles, name="role", native_enum=True),
    nullable=False, default=UserRoles.default
    )
  code = db.Column(db.String(26), default=id)
  max_uses = db.Column(db.Integer, default=1)
  uses = db.Column(db.Integer, default=0)

  @property
  def is_available(self):
    if self.uses < self.max_uses:
      return True
    return False

  def __str__(self) -> str:
    return self.id
  def __repr__(self) -> str:
    return f"<InvitationCode id={self.id}>"

# MARKDOWN POST

# TODO: migrate to notes blueprint
class Posts(UlidMixin, TimestampMixin, db.Model):
  __tablename__ = "post_table"
  title = db.Column(db.String(100))
  content = db.Column(db.String(100))
  author_id = db.Column(db.ForeignKey("user.id"))


## Table creation is handled in the app factory; avoid calling at import time.
