from typing import List, Dict, Any

from project.dao.models import Movie
from project.dao import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO) -> None:
        self.dao = dao

    def get_all(self, page: str = None, sort: str = None) -> List[Movie]:
        return self.dao.get_all(page, sort)

    def get_one(self, uid: int) -> Movie:
        return self.dao.get_one(uid)
