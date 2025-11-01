"""
models across the website
"""
import datetime
import ulid
from flask_login import UserMixin
from enum import Enum
from sqlalchemy import Enum as SaEnum
from sqlalchemy import text, Interval
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


# MIXINS

class TimestampMixin:
  created_at = db.Column(
    db.DateTime(timezone=True),
    default=lambda: datetime.datetime.now(datetime.timezone.utc),
    nullable=False
    )
  updated_at = db.Column(
    db.DateTime(timezone=True),
    default=datetime.datetime.now(datetime.timezone.utc),
    nullable=False
    )
  def update_time(self):
    self.updated_at = datetime.datetime.now(datetime.timezone.utc)

class IdMixin:
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class UlidMixin:
  id = db.Column(db.String(26), default=lambda: str(ulid.ULID()), primary_key=True)

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

USER_DEFAULT_ROLE = UserRoles.default

class User(IdMixin, UserMixin, TimestampMixin, db.Model):
  __tablename__ = "reguser"
  name = db.Column(db.String(100), unique=True)
  password_hash = db.Column(db.String(255))
  invite_code = db.Column(db.String(26), db.ForeignKey("invite_code.id"))
  role = db.Column(
    SaEnum(UserRoles, name="role", native_enum=True), nullable=False,
    default=USER_DEFAULT_ROLE, server_default = USER_DEFAULT_ROLE.value
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
  __tablename__ = "invite_code"
  role = db.Column(
    SaEnum(UserRoles, name="role", native_enum=True),
    nullable=False,
    default=USER_DEFAULT_ROLE, server_default=USER_DEFAULT_ROLE.value
    )
  code = db.Column(
    db.String(26), nullable=False, unique=True,
    default=lambda: str(ulid.ULID())
    )
  max_uses = db.Column(
    db.Integer, nullable=False,
    default=-1, server_default="-1"
    )
  uses = db.Column(
    db.Integer, nullable=False,
    default=0, server_default="0"
    )
  duration = db.Column(
    db.Interval, nullable=False,
    default=datetime.timedelta(weeks=2),
    server_default=text("interval '2 weeks'")
    )

  @staticmethod
  def lookup_code(invite_code: str):
    invite_code_obj = InviteCode.query.filter(InviteCode.code == invite_code).first()
    if invite_code_obj is None:
      raise LookupError(f"Invite code not found: {invite_code}")
    # checking it's the correct type, should always pass
    assert isinstance(invite_code_obj, InviteCode)
    return invite_code_obj

  @property
  def is_valid(self) -> bool:
    '''
    check if the invite code itself is valid
    this is useful in cleaning up invalid invitations from the db
    '''
    # B. the invite code should not exceed max uses (-1 means unlimited)
    if self.max_uses != -1 and self.uses >= self.max_uses:
      return False
    # C. should not pass expiry date
    if datetime.datetime.now(datetime.timezone.utc) > self.expires_at:
      return False
    return True

  @property
  def expires_at(self):
    return self.created_at + self.duration

  @staticmethod
  def is_valid_code(invite_code: str) -> bool:
    # A. the invite code should exist
    try:
      invite_code_obj = InviteCode.lookup_code(invite_code)
    except LookupError:
      return False
    # check inside the instance
    return invite_code_obj.is_valid
    

  def use_code(self):
    self.uses += 1

  def __str__(self) -> str:
    return self.id
  def __repr__(self) -> str:
    return f"<InvitationCode:{(" " + self.code) if self.code != self.id else ""} id={self.id}>"

# MARKDOWN POST

# TODO: migrate to notes blueprint
class Posts(UlidMixin, TimestampMixin, db.Model):
  __tablename__ = "markdown_post"
  title = db.Column(db.String(100))
  content = db.Column(db.String(100))
  author_id = db.Column(db.Integer, db.ForeignKey("reguser.id"))


## Table creation is handled in the app factory; avoid calling at import time.
