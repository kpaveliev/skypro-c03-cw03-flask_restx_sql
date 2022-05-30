from flask import request
from flask_restx import Resource, Namespace, fields
from marshmallow import ValidationError

from project.dao.models import UserSchema
from project.container import user_service

user_ns = Namespace('user', description="Views for users")

# Define api model for documentation
user_model = user_ns.model('User', {
    'id': fields.Integer(required=False),
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(required=True)
})


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


@user_ns.route('/')
class UserView(Resource):
    # @user_ns.doc(description='Get user by id')
    # @user_ns.response(200, 'Success', user_model)
    # @user_ns.response(404, 'Not Found')
    def get(self):
        uid = request.json.get('id')
        user = user_service.get_one(uid)
        if not user:
            return "", 404
        user_dict = UserSchema().dump(user)
        return user_dict, 200

    def patch(self):
        # Check if user exist
        uid = request.json.get('id')
        user = user_service.get_one(uid)
        print(user)
        if not user:
            return "", 404

        # Update with data passed if found
        updated_data = request.json
        user_service.update_info(UserSchema().dump(updated_data))
        return "", 200


#     @user_ns.doc(description='Update user by id')
#     @user_ns.response(201, 'User updated', user_model)
#     @user_ns.response(404, 'Not Found')
    def put(self):
        # Check if user exist
        uid = request.json.get('id')
        user = user_service.get_one(uid)
        if not user:
            return "", 404

        # Update with data passed if found
        passwords = request.json

        user_service.update_password(passwords)
        return "", 201


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
