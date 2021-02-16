from datetime import datetime
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt
from flask import current_app as app

from src.models.revoked_tokens import RevokedTokenModel
from src.models.users import UserModel, UserRole

from src.utils.hash import generate_hash, verify_hash

from src.utils.api_response import APIResponse

from src.utils.auth_token import generate_confirmation_token, confirm_token
from src.utils.email import send_registration_email


class SignUpResource(Resource):
    def post(self):
        """
        Sign Up
        ---
        tags:
          - auth
        description: Signup with user information
        operationId: userSignup
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  email:
                    type: string
                  password:
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
                required:
                  - email
                  - password
                  - role
                  - first_name
                  - last_name
                example:
                  email: user@mail.com
                  password: secret
                  role: User
                  first_name: Test
                  last_name: User
          description: email and password must be specified.
          required: true
        responses:
            200:
              description: Signup success
            409:
              description: Conflict user
            500:
              description: Internal server error
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Email required!')
        parser.add_argument('password', required=True, help='Password required!')
        roles = ("Admin", "User", "Developer")
        parser.add_argument('role', choices=roles, required=True, help='Invalid role!')
        parser.add_argument('first_name',  required=True, help='First name required!')
        parser.add_argument('last_name',  required=True, help='Last name required!')
        data = parser.parse_args()

        try:
            user = UserModel.get_first([
                UserModel.email == data['email']
            ])

            if user is not None:
                if user.verified:
                    return APIResponse.error_409("User already exist!")
            else:
                user = UserModel(email=data['email'])

            user.password = generate_hash(data['password'])
            user.role = UserRole.USER
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.verified = False

            token = generate_confirmation_token(data['email'])
            payload = {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'service_name': app.config['SERVICE_NAME'],
                'host_name': app.config['HOST_NAME']
            }

            send_registration_email(payload, token)
            user.save()

            response = {'message': 'Email sent!'}
            return APIResponse.success_200(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()


class SignInResource(Resource):
    def post(self):
        """
        Sign In
        ---
        tags:
          - auth
        description: Authenticate user with supplied credentials.
        operationId: userSignin
        requestBody:
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    email:
                      type: string
                    password:
                      type: string
                required:
                  - email
                  - password
                example:
                  email: user@mail.com
                  password: secret
        consumes:
            - application/json
        produces:
            - application/json
        responses:
          200:
            description: Login success
          400:
            description: Invalid password
          403:
            description: User not verified
          500:
            description: Internal server error
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Email required!')
        parser.add_argument('password', required=True, help='Password required!')
        data = parser.parse_args()

        try:
            email = data['email']

            user = UserModel.get_first([
                UserModel.email == email
            ])
            if user is None:
                return APIResponse.error_404("User not found!")

            if user.verified:
                if verify_hash(data['password'], user.password):
                    response = {
                        'access_token': create_access_token(identity=email),
                        'refresh_token': create_refresh_token(identity=email)
                    }
                    return APIResponse.success_200(response)
                else:
                    return APIResponse.error_400("Invalid password!")
            else:
                return APIResponse.error_403("User not verified!")

        except Exception as e:
            print(e)
            return APIResponse.error_500()


class SignOutResource(Resource):
    @jwt_required
    def post(self):
        """
        Sign out
        ---
        tags:
          - auth
        description: Signout user.
        operationId: userSignout
        produces:
            - application/json
        security:
            - bearerAuth: []
        responses:
          204:
            description: Signout success
          401:
            description: Unauthorized
          500:
            description: Internal server error
        """
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            response = {'message': 'Token revoked'}
            return APIResponse.success_204(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()


class TokenRefreshResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        Refresh access token
        ---
        tags:
          - auth
        description: Refresh access token.
        operationId: tokenRefresh
        security:
          - bearerAuth: []
        responses:
          204:
            description: Token refresh success
          401:
            description: Refresh token not provided or invalid
          500:
            description: Internal server error
        """
        try:
            email = get_jwt_identity()
            response = {
                'access_token': create_access_token(identity=email),
                'refresh_token': create_refresh_token(identity=email)
            }
            return APIResponse.success_200(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()


class UserVerifyResource(Resource):
    def get(self, verifyToken):
        """
        Verify email
        ---
        tags:
          - auth
        description: Verify email for sign up.
        operationId: signupVerify
        parameters:
          - in: path
            name: verifyToken
            schema:
              type: string
            required: true
            description: Token in verification email sent for sign up.
        responses:
          200:
            description: Email verify success
          400:
            description: User already verified.
          404:
            description: Invalid or expired token.
          500:
            description: Internal server error
        """
        try:
            email = confirm_token(verifyToken)

            if email is None:
                return APIResponse.error_404("The link has been expired or invalid.")

            user = UserModel.get_first([UserModel.email == email])
            if user.verified:
                return APIResponse.error_400("User already verified.")

            user.verified = True
            user.verified_at = datetime.utcnow()
            user.save()
            response = {"message": "User has been verified."}
            return APIResponse.success_200(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()


class ResendVerifyEmailResource(Resource):
    def get(self, email):
        """
        Resend verify email
        ---
        tags:
          - auth
        description: Resend verify email for sign up.
        operationId: signupEmailResend
        parameters:
          - in: path
            name: email
            schema:
              type: string
            required: true
            description: Email used for sign up.
        responses:
          200:
            description: Email sent
          404:
            description: Email not found.
          500:
            description: Internal server error
        """
        try:
            user = UserModel.get_first([UserModel.email == email])
            if user.verified:
                return APIResponse.error_404("User not found.")

            payload = {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            token = generate_confirmation_token(email)
            send_registration_email(payload, token)

            response = {"message": "Email sent again."}
            return APIResponse.success_200(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()


class UpdateEmailResource(Resource):
    def get(self, old_email, new_email):
        """
        Update email used for sign up.
        ---
      tags:
        - auth
      operationId: signupEmailUpdate
      parameters:
        - in: path
          name: old_email
          schema:
            type: string
          required: true
          description: Email used for sign up.
        - in: path
          name: new_email
          schema:
            type: string
          required: true
          description: New email for sign up.
      responses:
          200:
            description: Email sent
          404:
            description: Old email not found.
          409:
            description: New email already exist.
          500:
            description: Internal server error
        """
        try:
            user = UserModel.get_first([
                UserModel.email == old_email
            ])
            if user is None:
                return APIResponse.error_404("User not found")

            new_user = UserModel.get_first([
                UserModel.email == new_email
            ])
            if new_user is not None:
                return APIResponse.error_409("Email already exist.")

            user.email = new_email
            token = generate_confirmation_token(new_email)
            payload = {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'service_name': app.config['SERVICE_NAME'],
                'host_name': app.config['HOST_NAME']
            }
            send_registration_email(payload, token)

            user.save()
            response = {'message': 'Email updated'}
            return APIResponse.success_200(response)
        except Exception as e:
            print(e)
            return APIResponse.error_500()
