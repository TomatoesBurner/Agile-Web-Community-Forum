from flask import Flask
from flask_login import current_user
from config import Config
from .extensions import db, login, avatars, csrf
from sqlalchemy import func
from .models import UserModel, PostModel, CommentModel
from .blueprints.postCom.postCom import postCom_bp
from .blueprints.profile.profile import profile_bp
from .blueprints.auth.auth import auth_bp
from app.blueprints.notification.notification import notify_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    login.init_app(app)
    avatars.init_app(app)
    csrf.init_app(app)
    login.login_view = 'auth.login'

    # 上下文处理器
    @app.context_processor
    def inject_user_statistics():
        if current_user.is_authenticated:
            total_posts = db.session.query(func.count(PostModel.id)).filter_by(author_id=current_user.id).scalar()
            total_comments = db.session.query(func.count(CommentModel.id)).filter_by(author_id=current_user.id).scalar()
        else:
            total_posts = 0
            total_comments = 0
        return dict(total_posts=total_posts, total_comments=total_comments)

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(postCom_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(notify_bp)

    return app
