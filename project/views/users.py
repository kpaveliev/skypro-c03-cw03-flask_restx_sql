from flask import request
from flask_restx import Resource, Namespace, fields, abort
from marshmallow import ValidationError
from werkzeug.exceptions import MethodNotAllowed

from project.dao.models import UserSchema
from project.container import user_service, auth_service
from project.exceptions import ItemNotFound, IncorrectPassword

user_ns = Namespace('user', description="Views for users")
user_schema = UserSchema()

# Define api model for documentation
user_model = user_ns.model('User', {
    'id': fields.Integer(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'name': fields.String(required=True),
    'surname': fields.String(),
    'favorite_genre_id': fields.Integer()
})


@user_ns.route('/')
class UserView(Resource):
    @auth_service.auth_required
    @user_ns.doc(description='Get user by id')
    @user_ns.response(200, 'Success', user_model)
    @user_ns.response(404, 'Not Found')
    def get(self):
        try:
            uid = request.json.get('id')
            user = user_service.get_one(uid)
            user_dict = user_schema.dump(user)
            return user_dict, 200
        except ItemNotFound:
            abort(404, 'User not found')

    @user_ns.doc(description='Get user by id')
    @user_ns.response(200, 'User updated', user_model)
    @user_ns.response(405, 'Method not allowed')
    @user_ns.response(404, 'Not Found')
    def patch(self):
        try:
            # Update with data passed if found
            updated_data = user_schema.dump(request.json)
            user_service.update_info(updated_data)
            return "", 200
        except MethodNotAllowed:
            abort(405, "You're not allowed to change the data passed")
        except ItemNotFound:
            abort(404, 'User not found')

@user_ns.route('/password')
class PasswordView(Resource):
    @user_ns.doc(description='Update user password')
    @user_ns.response(200, 'Password updated', user_model)
    @user_ns.response(404, 'Not Found')
    @user_ns.response(405, 'Method not allowed')
    def put(self):
        try:
            passwords = request.json
            user_service.update_password(passwords)
            return "", 200
        except ItemNotFound:
            abort(404, 'User not found')
        except IncorrectPassword:
            abort(401, 'Password is incorrect')
        except MethodNotAllowed:
            abort(405, 'Invalid data passed')


# @user_ns.route('/')
# class UsersView(Resource):
#     @user_ns.doc(description='Get users')
#     @user_ns.response(200, 'Success', user_model)
#     def get(self):
#         all_users = user_service.get_all()
#         result = UserSchema(many=True).dump(all_users)
#         return result, 200

    # @user_ns.doc(description='Add new user', body=user_model)
    # @user_ns.response(201, 'Created')
    # @user_ns.response(400, 'ValidationError')
    # def post(self):
    #     data = request.json
    #     try:
    #         user_dict = UserSchema().dump(data)
    #     except ValidationError as e:
    #         return f"{e}", 400
    #     else:
    #         user = user_service.create(user_dict)
    #         return "", 201, {"location": f"/users/{user.id}"}


#
#     @user_ns.doc(description='Delete user by id')
#     @user_ns.response(204, 'User deleted', user_model)
#     @user_ns.response(404, 'Not Found')
#     def delete(self, uid):
#         # Check if user exist
#         user = user_service.get_one(uid)
#         if not user:
#             return "", 404
#
#         # Delete if found
#         user_service.delete(uid)
#         return "", 204
