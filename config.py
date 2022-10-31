import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # Insert your emails for admins in this list
    ADMINS = ['']
    REDIS_HOST = os.environ.get('REDIS_HOST') or ''

    # oauth config
    APP_STATE = 'ApplicationState'
    NONCE = 'SampleNonce'
    CLIENT_ID = os.environ.get('CLIENT_ID') or ''
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET') or ''
    REDIRECT_URI = os.environ.get('REDIRECT_URI') or ''
    AUTH_URI = os.environ.get('AUTH_URI') or ''
    TOKEN_URI = os.environ.get('TOKEN_URI') or ''
    ISSUER = os.environ.get('ISSUER') or ''
    USERINFO_URI = os.environ.get('USERINFO_URI') or ''
    TOKEN_INTROSPECTION_URI = os.environ.get('TOKEN_INTROSPECTION_URI') or ''

    # If using Gitlab a user name for the token is needed, Github will only need a token
    GIT_USER = os.environ.get("GIT_USER") or ""
    GIT_TOKEN = os.environ.get("GIT_TOKEN") or ""

    # Celery config
    CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379"
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379"
