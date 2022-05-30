import datetime
import calendar
from typing import Union, Callable

import jwt
from flask import request, current_app
from flask_restx import abort

from .user import UserService
from project.dao.models import User


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def register_user(self, credentials) -> None:
        self.user_service.create(credentials)

    def generate_tokens(self, credentials, is_refresh=False) -> dict:
        """
        Generate access and refresh JWT tokens

        :raises HTTPException: If no user found or password is incorrect
        """

        # Unpack data
        email_passed = credentials.get('email')
        password_passed = credentials.get('password')

        # Get user and check existence
        user = self.user_service.get_by_email(email_passed)
        print(f'User found: {user}')
        if not user:
            abort(404, 'User not found')

        # Compare passwords
        if not is_refresh:
            password_is_correct = self.user_service.compare_passwords(user.password, password_passed)
            if not password_is_correct:
                abort(401, 'Password is incorrect')

        # Generate token data
        data = {
            'email': user.email
        }
        print(f'Data for JWT: {data}')
        # Generate access token
        min_add = datetime.datetime.utcnow() + datetime.timedelta(minutes=
                                                                  current_app.config.get('TOKEN_EXPIRE_MINUTES'))
        data['exp']: int = calendar.timegm(min_add.timetuple())
        access_token = jwt.encode(data,
                                  current_app.config.get('JWT_SECRET'),
                                  algorithm=current_app.config.get('JWT_ALGORITHM'))

        # Generate refresh token
        days_add = datetime.datetime.utcnow() + datetime.timedelta(days=
                                                                   current_app.config.get('TOKEN_EXPIRE_DAYS'))
        data['exp']: int = calendar.timegm(days_add.timetuple())
        refresh_token = jwt.encode(data,
                                   current_app.config.get('JWT_SECRET'),
                                   algorithm=current_app.config.get('JWT_ALGORITHM'))

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def approve_token(self, refresh_token: str) -> dict:
        """
        Approve refresh token and generate a new pair of tokens

        :raise HTTPException: if no valid token passed
        """
        # Check if token is valid
        try:
            print(refresh_token)
            data = jwt.decode(refresh_token,
                              current_app.config.get('JWT_SECRET'),
                              algorithms=[current_app.config.get('JWT_ALGORITHM')])
        except Exception:
            abort(401)
        # Generate new pair
        else:
            credentials = {
                'email': data.get('email'),
                'password': None
            }
            new_tokens = self.generate_tokens(credentials, is_refresh=True)
            return new_tokens
    #
    # @staticmethod
    # def auth_required(func: Callable):
    #     """Check token passed is correct"""
    #     def wrapper(*args, **kwargs):
    #         # Check if authorization credentials were passed and get token
    #         if 'Authorization' not in request.headers:
    #             abort(401, 'No authorization data passed')
    #
    #         data = request.headers['Authorization']
    #         token = data.split("Bearer ")[-1]
    #
    #         # Decode and check token
    #         try:
    #             jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    #         except Exception as e:
    #             abort(401, f'JWT decode error {e}')
    #
    #         return func(*args, **kwargs)
    #
    #     return wrapper
    #
    # @staticmethod
    # def admin_required(func: Callable) -> Callable:
    #     """Check if the role is admin"""
    #     def wrapper(*args, **kwargs):
    #         # Check if authorization credentials were passed and get token
    #         if 'Authorization' not in request.headers:
    #             abort(401)
    #
    #         data = request.headers['Authorization']
    #         token = data.split("Bearer ")[-1]
    #
    #         # Decode token and check role
    #         try:
    #             token_decoded = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    #             role = token_decoded.get('role')
    #             if role != 'admin':
    #                 abort(401, 'Role is not admin')
    #         except Exception as e:
    #             abort(401, f'JWT decode error {e}')
    #
    #         return func(*args, **kwargs)
    #
    #     return wrapper
