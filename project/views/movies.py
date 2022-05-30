from flask import request
from flask_restx import Resource, Namespace, abort
from marshmallow import ValidationError

from project.exceptions import ItemNotFound
from project.container import movie_service
from project.dao.models import MovieSchema

# Declare namespace and define marshmallow schema
movie_ns = Namespace('movies', description='Views for movies')
movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


@movie_ns.route('/')
class MoviesViews(Resource):
    @movie_ns.doc(description='Get movies',
                  params={'page': 'Page number',
                          'status': 'new - to show recent films first'})
    @movie_ns.response(200, 'Success')
    @movie_ns.response(404, 'Not found')
    def get(self):

        page = request.args.get('page', type=int)
        status = request.args.get('status')

        movies_found = movie_service.get_all(page, status)

        if not movies_found:
            abort(404, message='Movies not found')

        return movies_schema.dump(movies_found), 200


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    @movie_ns.doc(description='Get movie by id')
    @movie_ns.response(200, 'Success')
    @movie_ns.response(404, 'Not found')
    def get(self, uid):
        # Find row
        movie = movie_service.get_one(uid)

        # Throw not found if uid not found
        if not movie:
            abort(404, f'Movie with id={uid} not found')

        return movie_schema.dump(movie), 200
