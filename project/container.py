from .dao import MovieDAO
from .dao import UserDAO
from .services import MovieService
from .services import UserService
from .services import AuthService

from .setup_db import db

movie_dao = MovieDAO(session=db.session)
user_dao = UserDAO(session=db.session)

movie_service = MovieService(dao=movie_dao)
user_service = UserService(dao=user_dao)
auth_service = AuthService(user_service=user_service)