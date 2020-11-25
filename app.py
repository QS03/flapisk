import config
from celery import Celery
from src import create_app

celery = Celery(
    __name__,
    backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/0',
)

app = create_app(config.DevelopmentConfig)

celery.conf.update(app.config)


@app.route("/")
def health_check():
    return {"message": "API server is live!"}


@app.shell_context_processor
def make_shell_context():
    """Adds imports to default shell context for easier use"""
    from src.models.users import UserModel
    from src.models.revoked_tokens import RevokedTokenModel
    return {
        "user": UserModel,
        "revoked_token": RevokedTokenModel,
    }


from src.services.jwt import jwt


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    from src.models.revoked_tokens import RevokedTokenModel
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


if __name__ == '__main__':
    app.run(debug=True)
