"""Flask app config and initialization"""
import logging.config
from flask import Flask


def create_app(config_obj=None):
    app = Flask(__name__)

    if not config_obj:
        logging.warning("No config specified; defaulting to development")

        import config
        config_obj = config.DevelopmentConfig

    app.config.from_object(config_obj)

    # CORS allow
    from flask_cors import CORS
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # DB service
    from src.services.db import db
    db.init_app(app)
    db.app = app

    # Migration service
    from src.services.migrate import migrate
    migrate.init_app(app, db)

    # Marshmallow service
    from src.services.marshmallow import ma
    ma.init_app(app)

    # JWT service
    from src.services.jwt import jwt
    jwt.init_app(app)

    from src.services.flagger import swagger
    swagger.init_app(app)

    # Router service
    from src.routes import api_router
    api_router.init_app(app)

    from src.resources.auth import SignInResource, SignUpResource, SignOutResource, TokenRefreshResource, \
        UserVerifyResource, ResendVerifyEmailResource, UpdateEmailResource
    api_router.add_resource(SignInResource, "/auth/sign-in")
    api_router.add_resource(SignUpResource, "/auth/sign-up")
    api_router.add_resource(SignOutResource, "/auth/sign-out")
    api_router.add_resource(TokenRefreshResource, "/auth/refresh")
    api_router.add_resource(UserVerifyResource, "/auth/verify/<verifyToken>", methods=['GET'])
    api_router.add_resource(ResendVerifyEmailResource, "/auth/email-resend/<email>", methods=['GET'])
    api_router.add_resource(UpdateEmailResource, "/auth/email-update/<old_email>/<new_email>", methods=['GET'])

    from src.resources.profile import GetProfileResource, UpdateProfileResource, \
        PasswordResetResource, CloseProfileResource
    api_router.add_resource(GetProfileResource, "/profile", methods=['GET'])
    api_router.add_resource(UpdateProfileResource, "/profile", methods=['PUT'])
    api_router.add_resource(PasswordResetResource, "/profile/password-reset", methods=['POST'])
    api_router.add_resource(CloseProfileResource, "/profile/close", methods=['POST'])

    from src.resources.users import GetUserResource, GetUsersResource, \
        UpdateUserResource, DeleteUserResource
    api_router.add_resource(GetUsersResource, "/users/", methods=['GET'])
    api_router.add_resource(GetUserResource, "/users/<id>", methods=['GET'])
    api_router.add_resource(UpdateUserResource, "/users/<id>", methods=['PUT'])
    api_router.add_resource(DeleteUserResource, "/users/<id>", methods=['DELETE'])

    api_router.register_routes()

    return app
