import json
from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.users import UserModel, UserRole
from src.schemas.users import UserSchema

from src.utils.api_response import APIResponse
from src.utils.hash import generate_hash, verify_hash


class GetProfileResource(Resource):
    @jwt_required
    def get(self):
        """
        Get profile
        ---
        tags:
          - profile
        description: Get logged in user's profile.
        operationId: getUserProfile
        security:
          - bearerAuth: []
        responses:
          200:
            description: Success
          401:
            description: Unauthorized.
          500:
            description: Internal server error
        """
        try:
            email = get_jwt_identity()
            user = UserModel.get_first([
                UserModel.email == email
            ])
            if user is None:
                return APIResponse.error_404("User not found!")

            result = UserSchema().dumps(user)

            response = json.loads(result)
            return APIResponse.success_200(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()


class UpdateProfileResource(Resource):
    @jwt_required
    def put(self):
        """
        Update profile
        ---
        tags:
          - profile
        description: Update profile with user information
        operationId: profileUpdate
        security:
          - bearerAuth: []
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  email:
                    type: string
                  role:
                    type: string
                    enum:
                      - User
                      - Developer
                      - Admin
                  first_name:
                    type: string
                  last_name:
                    type: string
                  phone_number:
                    type: string
                required:
                  - email
                  - role
                example:
                  email: user@mail.com
                  role: User
                  first_name: Test
                  last_name: User
                  phone_number: (234)567-8901
          description: email and role must be specified.
          required: true
        responses:
            200:
              description: Profile updated
            404:
              description: User not found
            500:
              description: Internal server error
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Email required!')
        roles = ("Admin", "User", "Developer")
        parser.add_argument('role', choices=roles, required=True, help='Invalid role!')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('phone_number')
        data = parser.parse_args()

        try:
            email = get_jwt_identity()
            user = UserModel.get_first([
                UserModel.email == email
            ])
            if user is None:
                return APIResponse.error_404("User not found!")

            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.role = UserRole.role(data['role'])
            user.phone_number = data['phone_number']

            user.save()
            result = UserSchema().dumps(user)
            response = json.loads(result)
            return APIResponse.success_200(response)

        except Exception as e:
            print(e)
            return APIResponse.error_500()


class PasswordResetResource(Resource):
    @jwt_required
    def post(self):
        """
        Password Reset
        ---
        tags:
          - profile
        description: Update old password with a new one.
        operationId: resetPassword
        security:
          - bearerAuth: []
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  email:
                    type: string
                  current_password:
                    type: string
                  new_password:
                    type: string
                  confirm_password:
                    type: string
                required:
                  - email
                  - current_password
                  - new_password
                  - confirm_password
                example:
                  email: user@mail.com
                  current_password: secret
                  new_password: new_secret
                  confirm_password: new_secret
          description: All fields must be specified.
          required: true
        responses:
            200:
              description: Password updated.
            400:
              description: Current password incorrect or confirm password not match.
            404:
              description: User not found
            500:
              description: Internal server error
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Email required!')
        parser.add_argument('current_password', required=True, help='Current password required!')
        parser.add_argument('new_password', required=True, help='New password required!')
        parser.add_argument('confirm_password', required=True, help='Confirm password confirm required!')
        data = parser.parse_args()

        try:
            email = get_jwt_identity()
            user = UserModel.get_first([
                UserModel.email == email
            ])
            if user is None:
                return APIResponse.error_404("User not found!")

            if not verify_hash(data['current_password'], user.password):
                return APIResponse.error_400("Current password not match!")

            if data['new_password'] != data['confirm_password']:
                return APIResponse.error_400("Confirm password not match!")

            user.password = generate_hash(data['new_password'])
            user.save()
            response = {'message': "Password reset success!"}
            return APIResponse.success_200(response)

        except Exception as e:
            print(e)
            return APIResponse.error_500()


class CloseProfileResource(Resource):
    @jwt_required
    def post(self):
        """
        Close Account
        ---
        tags:
          - profile
        description: Close account.
        operationId: closeAccount
        security:
          - bearerAuth: []
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  email:
                    type: string
                required:
                  - email
                example:
                  email: user@mail.com
          description: Email must be specified.
          required: true
        responses:
            204:
              description: Account closed.
            404:
              description: User not found
            500:
              description: Internal server error
        """
        try:
            email = get_jwt_identity()
            user = UserModel.get_first([
                UserModel.email == email
            ])
            if user is None:
                return APIResponse.error_404("User not found")

            user.active = False
            user.save()

            response = {'message': "User deactivated!"}
            return APIResponse.success_204(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()
