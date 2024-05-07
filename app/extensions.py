from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_avatars import Avatars
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login = LoginManager()
avatars = Avatars()
csrf = CSRFProtect()