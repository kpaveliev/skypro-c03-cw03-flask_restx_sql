from typing import List, Dict

from flask import current_app
from sqlalchemy import desc

from .models import Movie
from .base import BaseDAO


class MovieDAO(BaseDAO):
    def get_all(self, page: str = None, sort: str = None) -> List[Movie]:
        """Get all movies from the db"""

        movies = self.session.query(Movie)

        if sort:
            movies = movies.order_by(desc(Movie.year))
        if page:
            movies = movies\
                .limit(current_app.config.get('ITEMS_PER_PAGE'))\
                .offset(page * current_app.config.get('ITEMS_PER_PAGE') - current_app.config.get('ITEMS_PER_PAGE'))

        return movies.all()

    def get_one(self, uid: int) -> Movie:
        """Get movie with the passed id from db"""
        return self.session.query(Movie).get(uid)
