from typing import List

from flask import current_app
from sqlalchemy import desc

from .models import User
from .base import BaseDAO


class UserDAO(BaseDAO):

    def get_one(self, uid: int) -> User:
        """Get user by id"""
        user = self.session.query(User).get(uid)
        return user

    def get_all(self) -> List[User]:
        """Get all users"""
        users = self.session.query(User).all()
        return users

    def get_by_email(self, email: str) -> User:
        """Get user by the username"""
        user = self.session.query(User).filter(User.email == email).one()
        return user


    def create(self, data: dict) -> User:
        """Add user to the database"""
        user = User(**data)
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, uid: int) -> None:
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, data: dict) -> None:
        """Update user with data"""
        self.session.query(User).filter(User.id == data['id']).update(data)
        self.session.commit()


