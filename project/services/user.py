import base64
import hashlib
import hmac
from typing import List

from flask import current_app
from flask_restx import abort

from project.dao import UserDAO
from project.dao.models import User


class UserService:
    def __init__(self, dao: UserDAO) -> None:
        self.dao = dao

    def get_all(self) -> List[User]:
        """Get all users"""
        return self.dao.get_all()

    def get_by_email(self, email: str) -> User:
        """Get user data by username"""
        user = self.dao.get_by_email(email)
        return user

    def get_one(self, uid: int) -> User:
        """Get user by id"""
        return self.dao.get_one(uid)

    def create(self, data: dict) -> User:
        """Add user to the database"""
        # Hash password
        data['password'] = self.hash_password(data.get('password'))
        # Add user to the database
        user = self.dao.create(data)
        return user

    def update_info(self, data: dict) -> None:
        """Partially update user information"""
        # Check data is okay
        if 'password' not in data.keys() and 'email' not in data.keys():
            self.dao.update(data)
        else:
            abort(405, f"You can't change email and password using this method")

    def update_password(self, data: dict) -> None:
        """Partially update user information"""
        # Check data is okay
        uid = data.get('id')
        current_password = data.get('password_1')
        new_password = data.get('password_2')

        if None in [uid, current_password, new_password]:
            abort(405, f"Wrong arguments passed")

        user = self.get_one(uid)
        if not self.compare_passwords(user.password, current_password):
            abort(405, f"Wrong password passed")

        data = {
            'id': uid,
            'password': self.hash_password(new_password)
        }

        self.dao.update(data)


    #
    # def delete(self, uid: int) -> None:
    #     """Delete user"""
    #     self.dao.delete(uid)

    def hash_password(self, password: str)-> bytes:

        hash_digest = self.create_hash(password)
        encoded_digest = base64.b64encode(hash_digest)
        return encoded_digest

    def create_hash(self, password: str) -> bytes:
        """Hash password passed with sha256"""

        hash_digest: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            current_app.config.get('PWD_HASH_SALT'),
            current_app.config.get('PWD_HASH_ITERATIONS')
        )

        return hash_digest

    def compare_passwords(self, password_hash: str, password_passed: str) -> bool:
        """Compare password passed with user password in db"""

        # Decode password from the database into binary
        decoded_digest: bytes = base64.b64decode(password_hash)

        # Hash password passed
        passed_hash: bytes = self.create_hash(password_passed)

        is_equal = hmac.compare_digest(decoded_digest, passed_hash)

        return is_equal
