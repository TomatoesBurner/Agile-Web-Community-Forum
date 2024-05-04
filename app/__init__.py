from flask import Flask
from config import Config
from .extensions import db, login
from flask_migrate import Migrate
from app.blueprints.auth.auth import auth_bp
from app.blueprints.postCom.postCom import postCom_bp


app = Flask(__name__)
# 数据库配置文件
app.config.from_object(Config)

## 初始化db
db.init_app(app)

## 初始化flask-login
login.init_app(app)
login.login_view = 'auth.login'

migrate = Migrate(app, db)

# 用户发出请求后,先用一个对象存储用户的user_id，然后再去执行视图函数
# flask db init:只需要执行一次
# flask db migrate:将orm模型生成迁移脚本
# flask db upgrade:将迁移脚本映射到数据库中

# 视图函数全部放在蓝图当中
app.register_blueprint(auth_bp)
app.register_blueprint(postCom_bp)