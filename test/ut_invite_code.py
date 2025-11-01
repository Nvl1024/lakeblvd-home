"""
test functionality 
"""
import os
os.environ["REQUIRE_INVITATION"]="true"
os.environ["APP_ENV"]="test"
import sys
sys.path.insert(1, os.path.normpath(os.path.join(__file__, "../..")))
import unittest
import datetime
from flask import url_for
from app import app
from app.extensions import db
from app.models import InviteCode, User, UserRoles



class TestInviteCode(unittest.TestCase):
    INVITE_CODE = 'LB-TEST-1024'
    MAX_USES = 32

    def test_1_setup(self):
        """
        check environment setup
        """
        
        # check that require_invitation is set
        require_invitation = os.getenv("REQUIRE_INVITATION")
        assert require_invitation == "true", \
            f"expecting require_invitation 'true', not {str(require_invitation)}"
        # setup app with test environment

    def test_2_create_code(self):
        """
        initiate InviteCode instance, test its properties
        """
        # create instance
        with app.app_context():
            invite_code = InviteCode(
                role=UserRoles.default,
                code=self.INVITE_CODE,
                # max_uses=MAX_USES,
                # uses=0,
            )
            # Test attributes:
            # 1. write invite code into db
            db.session.add(invite_code)
            db.session.commit()
    
    def test_3_read_code(self):
        with app.app_context():
            # 1. should be able to lookup the invite code
            invite_code = InviteCode.lookup_code(self.INVITE_CODE)
            assert isinstance(invite_code, InviteCode)
            # 2. should be valid
            assert InviteCode.is_valid_code(self.INVITE_CODE)
            assert invite_code.is_valid
            # 3. invalid code should return false
            wrong_invite_code = "LB-TEST-2024"
            assert not InviteCode.is_valid_code(wrong_invite_code), \
                "expecting to reject wrong invite code"
            # 4. the invite code should be available
            assert invite_code.is_valid, \
                "expecting invite code available for use"
            assert invite_code.code == self.INVITE_CODE, \
                "expecting invite code consistent, {invite_code.code}: {self.INVITE_CODE}"
            # 5. timestamps are correct
            assert invite_code.created_at < datetime.datetime.now(datetime.timezone.utc), \
                "expecting created time earlier than now"
            assert invite_code.expires_at > datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3), \
                "expecting expiry date more than 3 days ahead"

    def test_4_use_code(self): 
        """
        create user with the invite code
        """
        # Arrange: seed one InviteCode
        with app.app_context():
            # should be able to lookup code
            invite_code = InviteCode.lookup_code(self.INVITE_CODE)
            invite_code_id = invite_code.id  # ForeignKey points to invite_code_table.id
            # add two users
            new_user_1 = User(
                name="ic-test-user-1", invite_code=invite_code_id)
            new_user_2 = User(
                name="ic-test-user-2", invite_code=invite_code_id)
            db.session.add(new_user_1)
            invite_code.use_code()
            db.session.add(new_user_2)
            invite_code.use_code()
            db.session.commit()
            invited_users = User.query.filter(User.invite_code == invite_code_id).all()
            for user in invited_users:
                assert user.role is UserRoles.default, \
                f"expecting {user.name} role to be 'UserRoles.default', not {user.role}"

    def test_5_cleanup(self):
        """
        clean up the test invite code
        """
        # roll back without commit
        with app.app_context():
            invite_code = InviteCode.query.filter(InviteCode.code==self.INVITE_CODE).first()
            assert invite_code is not None, "expecting to find invite code "
            invite_code_id = invite_code.id
            # delete users associated with the invitation
            invited_users = User.query.filter(User.invite_code == invite_code_id).all()
            for user in invited_users:
                db.session.delete(user)
                db.session.commit()
            # delete invitation code
            db.session.delete(invite_code)
            db.session.commit()
            # confirm invite code is deleted, can no longer look up
            self.assertRaises(LookupError, InviteCode.lookup_code, self.INVITE_CODE)
            remaining_users = len(User.query.filter(User.invite_code == invite_code_id).all())
            assert remaining_users == 0, \
                f"expecting no users with invite_code after cleanup, but got {remaining_users}"

if __name__ == '__main__':
    unittest.main()
