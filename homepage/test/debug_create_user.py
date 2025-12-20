import sys
import getpass
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models import User


db = SQLAlchemy()
app = create_app()
with app.app_context():
	db.create_all()

def create_user(username: str, password: str, group: int = 0) -> User:
	"""Create and persist a new user using the current model.

	Args:
		username: The user's unique name (User.name).
		password: Plaintext password; will be hashed into User.hash.
		group: Integer group identifier; defaults to 0.

	Returns:
		The persisted User instance (with id populated).
	"""
	if not username or not username.strip():
		raise ValueError("Username cannot be empty")
	if password is None or password == "":
		raise ValueError("Password cannot be empty")

	pw_hash = generate_password_hash(password)

	with app.app_context():
		user = User(name=username.strip(), hash=pw_hash, group=int(group))
		db.session.add(user)
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()
			raise ValueError(f"User '{username}' already exists")
		return user


def _parse_args(argv):
	"""Simple argv parser: username [password] [group]"""
	username = None
	password = None
	group = 0

	if len(argv) >= 2:
		username = argv[1]
	if len(argv) >= 3:
		password = argv[2]
	if len(argv) >= 4:
		try:
			group = int(argv[3])
		except ValueError:
			print("Group must be an integer; defaulting to 0", file=sys.stderr)
			group = 0
	return username, password, group


if __name__ == "__main__":
	username, password, group = _parse_args(sys.argv)
	if not username:
		username = input("Username: ").strip()
	if not password:
		password = getpass.getpass("Password: ")

	try:
		user = create_user(username, password, group)
		print(f"Created user id={user.id}, name='{user.name}', group={user.group}")
	except Exception as e:
		print(f"Failed to create user: {e}", file=sys.stderr)
		sys.exit(1)