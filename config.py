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
