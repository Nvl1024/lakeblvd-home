"""
insert invite code into test environment
"""
# set environment variables
import os
os.environ["REQUIRE_INVITATION"]="true"
os.environ["APP_ENV"]="test"
# set import path
import sys
sys.path.insert(1, os.path.normpath(os.path.join(__file__, "../..")))
# imports
from abc import abstractmethod
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import argparse
from app import app
from app.extensions import db
from app.models import InviteCode, User


class AppDbMixin:
    """
    mixin app and db attributes
    """
    app: Flask = app
    db: SQLAlchemy = db

class Inject:
    """
    the abstract class
    for inserting and deleting instance into test environment
    """
    @abstractmethod
    def insert(self, *args, **kwargs):
        """insert instance into db"""
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        """delete instance from db"""
        pass

class InjectInviteCode(AppDbMixin, Inject):
    """
    implementations
    for inserting and deleting invite code into test environment
    """
    def insert(self, code: str):
        with self.app.app_context():
            invite_code = InviteCode(code=code)
            self.db.session.add(invite_code)
            self.db.session.commit()

    def delete(self, code: str):
        with self.app.app_context():
            invite_code = InviteCode.lookup_code(code)
            self.db.session.delete(invite_code)
            self.db.session.commit()

class InjectUser(AppDbMixin, Inject):
    def insert(self, *args, **kwargs):
        with self.app.app_context():
            user = User(*args, **kwargs)
            self.db.session.add(user)
            self.db.session.commit()
    
    def delete(self, *args, **kwargs):
        with self.app.app_context():
            user = User.query.filter(**kwargs)
        raise NotImplementedError()


ALLOWED_TARGETS = {
    "code": {
        "class": InjectInviteCode,
        "actions": {"insert", "remove"},
    },
    "user": {
        "class": User,
        "actions": {"insert", "remove"},
    }
}

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="injection",
        description="Inject instances into flask app database."
    )
    parser.add_argument("--dry-run", action="store_true", help="Don't actually perform actions.")
    parser.add_argument("--verbose", "-v", action="count", default=0, help="Increase verbosity.")

    subparsers = parser.add_subparsers(dest="target",  required=True, help="Target object [code|user]")
    p_code = subparsers.add_parser("code", help="Operations for invite codes")
    code_sub = p_code.add_subparsers(dest="action", required=True, help="Action to perform")

    # TODO: define parser
    p_insert = code_sub.add_parser("insert", help="insert an ")
    return parser

if __name__ == '__main__':
    # HARDCODE
    inject_code = InjectInviteCode()
    inject_code.insert(code='TEST-1024')
    print('debug...')
