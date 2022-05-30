from flask import request
from flask_restx import Resource, Namespace, fields

from project.container import auth_service

auth_ns = Namespace('auth', description='Authorization and authentication')

# Define api model for documentation
auth_model = auth_ns.model('Authentication', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

tokens_model = auth_ns.model('Tokens', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True)
})

@auth_ns.route('/register')
class AuthView(Resource):
    # @auth_ns.doc(description='User registrations authentication info', body=auth_model)
    # @auth_ns.response(201, 'Tokens created', tokens_model)
    # @auth_ns.response(400, 'Bad Request')
    # @auth_ns.response(401, 'Unauthorized')
    # @auth_ns.response(404, 'Not Found')
    def post(self):
        # Get and check credentials passed
        credentials = {
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }

        if None in credentials.values():
            return "", 400

        # Register service
        user = auth_service.register_user(credentials)
        return "", 201


@auth_ns.route('/login')
class AuthView(Resource):
    # @auth_ns.doc(description='Send authentication info', body=auth_model)
    # @auth_ns.response(201, 'Tokens created', tokens_model)
    # @auth_ns.response(400, 'Bad Request')
    # @auth_ns.response(401, 'Unauthorized')
    # @auth_ns.response(404, 'Not Found')
    def post(self):
        # Get and check credentials passed
        credentials = {
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }

        if None in credentials.values():
            return "", 400

        # Generate tokens
        tokens = auth_service.generate_tokens(credentials)
        return tokens, 201

    # @auth_ns.doc(description='Update user by id')
    # @auth_ns.response(201, 'Tokens created', tokens_model)
    # @auth_ns.response(404, 'Not Found')
    def put(self):
        refresh_token = request.json.get('refresh_token')
        tokens = auth_service.approve_token(refresh_token)
        return tokens, 201
