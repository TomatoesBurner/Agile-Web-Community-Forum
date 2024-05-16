from hashlib import md5
from urllib.parse import urlsplit
from flask_avatars import Identicon
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from app.forms import RegisterForm, LoginForm
from app.models import UserModel
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=['GET', 'POST'])
@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('postCom.index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = UserModel.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember.data) # 在这里传递remember的参数
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('postCom.index')
        return redirect(next_page)
    # 对于 GET 请求和验证失败的 POST 请求，总是传递 form 对象
    return render_template("login.html", form=form)


# 如果没有指定method参数,默认就是get请求
# Get: 从服务器上获取数据
# Post: 将客户端的数据提交给服务器
@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  #
    form = RegisterForm()
    if form.validate_on_submit():
        # 表单提交且验证通过
        email = form.email.data
        username = form.username.data
        identicon = Identicon()
        filenames = identicon.generate(text=md5(email.encode("utf-8")).hexdigest())
        avatar = filenames[2]
        user = UserModel(email=email, username=username,avatar=avatar)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for("auth.login"))  # 成功后重定向到登录页面
    # GET 请求或表单验证失败，重新渲染注册页面
    print(form.errors)
    return render_template("register.html", form=form)  # 显示表单或重新渲染表单显示错误


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
