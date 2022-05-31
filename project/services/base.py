from typing import Union, List

from project.dao import MovieDAO, GenreDAO, UserDAO, DirectorDAO
from project.exceptions import ItemNotFound


class BaseService:
    def __init__(self, dao: Union[MovieDAO, GenreDAO, DirectorDAO, UserDAO]) -> None:
        """DAO needs to be submitted when creating service object"""
        self.dao = dao

    def get_one(self, uid: int) -> object:
        """Get one item from the db"""
        item = self.dao.get_one(uid)
        if not item:
            raise ItemNotFound
        return item

    def get_all(self, page: str = None) -> List[object]:
        """
        Get all items from the db

        :param page: Page number (optional)
        :raises ItemNotFound: If no items found
        """
        items = self.dao.get_all(page, sort=False)
        if not items:
            raise ItemNotFound
        return items
