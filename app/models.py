from .extensions import db
from datetime import datetime
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    return db.session.get(UserModel, int(user_id))


class UserModel(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    avatar = db.Column(db.String(100))
    aboutme = db.Column(db.String(100))
    join_time = db.Column(db.DateTime, default=datetime.now)
    points = db.Column(db.Integer, default=0)
    #relationship
    posts = db.relationship('PostModel', backref='author', lazy=True)
    comments = db.relationship('CommentModel', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PostModel(db.Model):
    # post的数据模型
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_done = db.Column(db.Boolean, default=False)
    post_type = db.Column(db.String(10))
    # 外键
    accepted_answer_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # 关系
    accepted_answer = db.relationship('CommentModel', foreign_keys=[accepted_answer_id], post_update=True)


class CommentModel(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_accepted = db.Column(db.Boolean, default=False)
    # 外键
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # 关系
    post = db.relationship(PostModel, foreign_keys=[post_id], backref=db.backref("comments", order_by=create_time.desc()))
