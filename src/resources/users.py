import json
from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity

from src.models.users import UserModel, UserRole
from src.schemas.users import UserSchema

from src.utils.api_response import APIResponse
from src.utils.hash import generate_hash


class GetUsersResource(Resource):
    @jwt_required
    def get(self):
        try:
            users = UserModel.get_all([
                UserModel.active == True
            ])
            result = UserSchema().dumps(users, many=True)

            response = json.loads(result)
            return APIResponse.success_200(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()

    @jwt_required
    def post(self):
        return APIResponse.error_403()


class GetUserResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            user = UserModel.get_first([
                UserModel.id == id,
                UserModel.active == True
            ])
            if user is None:
                return APIResponse.error_404()

            result = UserSchema().dumps(user)

            response = json.loads(result)
            return APIResponse.success_200(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()


class UpdateUserResource(Resource):
    @jwt_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Email required!')
        parser.add_argument('password', required=True, help='Password required!')
        roles = ("Admin", "User", "Developer")
        parser.add_argument('role', choices=roles, required=True, help='Invalid role!')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        data = parser.parse_args()

        try:
            user = UserModel.get_first([
                UserModel.id == id,
                UserModel.active == True
            ])
            if user is None:
                return APIResponse.error_404()

            user.email = data['email']
            user.password = generate_hash(data['password'])
            user.role = UserRole.role(data['role'])
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()

            result = UserSchema().dumps(user)

            response = json.loads(result)
            return APIResponse.success_200(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()


class DeleteUserResource(Resource):
    @jwt_required
    def delete(self, id):
        try:
            user = UserModel.get_first([
                UserModel.id == id,
                UserModel.active == True
            ])
            if user is None:
                return APIResponse.error_404()

            user.delete()
            response = {'message': 'Entity deleted'}
            return APIResponse.success_204(response)

        except Exception as e:
            print(e)
            return APIResponse.error_500()
