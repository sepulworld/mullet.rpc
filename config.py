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
    APP_STATE = 'ApplicationState'
    NONCE = 'Nonce'

    # If using Gitlab a user name for the token is needed, Github will only need a token
    GIT_USER = os.environ.get("GIT_USER") or ""
    GIT_TOKEN = os.environ.get("GIT_TOKEN") or ""

    # Celery config
    CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379"
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379"
