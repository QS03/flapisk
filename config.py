import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class DevelopmentConfig(object):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

    if 'MYSQL_HOST' not in os.environ:
        dotenv_path = os.path.join(BASE_DIR, '.env.development')
        load_dotenv(dotenv_path)

    SYS_CONFIG_DIR = os.getenv('SYS_CONFIG_DIR')

    """Application configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY')
    JSONIFY_PRETTYPRINT_REGULAR = True
    DEBUG = True

    """SQLAlchemy configuration"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'.format(
        USER=os.getenv('MYSQL_USER'),
        PASSWORD=os.getenv('MYSQL_PASSWORD'),
        HOST=os.getenv('MYSQL_HOST'),
        PORT=os.getenv('MYSQL_PORT'),
        DATABASE=os.getenv('MYSQL_DATABASE')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    """JWT configuration"""
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 7
    JWT_HEADER_TYPE = 'Bearer'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = True

    """AWS configuration"""
    AWS_REGION = os.getenv('AWS_REGION')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


    """Tmp path"""
    TMP_UPLOAD_PATH = "/tmp/upload/"
    os.makedirs(TMP_UPLOAD_PATH, exist_ok=True)

    TMP_DOWNLOAD_PATH = "/tmp/download/"
    os.makedirs(TMP_DOWNLOAD_PATH, exist_ok=True)

    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    HOST_NAME = os.getenv('HOST_NAME')
    SERVICE_NAME = os.getenv('SERVICE_NAME')
    SERVICE_EMAIL = os.getenv('SERVICE_EMAIL')


class ProductionConfig(object):
    DEBUG = False
