from flask_login import UserMixin
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), unique=True)
  password_hash = db.Column(db.String(200))

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

# TODO: migrate to notes blueprint
class Posts(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(100))
  content = db.Column(db.String(100))


## Table creation is handled in the app factory; avoid calling at import time.
