import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    # Avatars
    AVATARS_SAVE_PATH = os.path.join(BASE_DIR, "media", "avatars")

    #session time
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)

    # Pagination
    POSTS_PER_PAGE =10

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'  #
    TESTING = True

    WTF_CSRF_ENABLED = False  # ban CSRF protection

    SERVER_NAME = '127.0.0.1:5001' # Using an in-memory database

    APPLICATION_ROOT = '/'

    PREFERRED_URL_SCHEME = 'http'

class SeleniumTestingConfig(TestConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'tests', 'testapp.db')

