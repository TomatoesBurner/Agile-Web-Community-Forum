from hashlib import md5
from urllib.parse import urlsplit
from flask_avatars import Identicon
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user
from app.forms import RegisterForm, LoginForm, SecurityQuestionForm, ForgotPasswordForm
from app.models import UserModel
from app.extensions import db
from app.utils.wordsban import filter_bad_words

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
    return render_template("login.html", form=form)

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = filter_bad_words(form.username.data)
        identicon = Identicon()
        filenames = identicon.generate(text=md5(email.encode("utf-8")).hexdigest())
        avatar = filenames[2]
        user = UserModel(
            email=email,
            username=username,
            avatar=avatar,
            security_question=form.security_question.data
        )
        user.set_password(form.password.data)
        user.set_security_question = form.security_question.data
        user.set_security_answer(form.security_answer.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth_bp.route('/check_email', methods=['POST'])
def check_email():
    email = request.form.get('email')
    user = UserModel.query.filter_by(email=email).first()
    if user:
        return jsonify({'exists': True, 'question': user.security_question})
    else:
        return jsonify({'exists': False})

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    email_error = None
    if form.validate_on_submit():
        email = form.email.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            return redirect(url_for('auth.security_question', email=email))
        else:
            email_error = 'Email does not exist'
    return render_template('forgot_password.html', forgot_form=form, email_error=email_error)

@auth_bp.route('/security_question', methods=['GET', 'POST'])
def security_question():
    email = request.args.get('email')
    user = UserModel.query.filter_by(email=email).first()
    if not user:
        flash('Invalid email address', 'error')
        return redirect(url_for('auth.forgot_password'))

    form = SecurityQuestionForm()
    if form.validate_on_submit():
        if user.check_security_answer(form.security_answer.data):
            if form.new_password.data != form.confirm_password.data:
                form.confirm_password.errors.append('Passwords do not match')
            else:
                user.set_password(form.new_password.data)
                db.session.commit()
                flash('Your password has been reset!')
                return redirect(url_for('auth.login'))
        else:
            form.security_answer.errors.append('Incorrect answer to the security question')

    return render_template('security_question.html', form=form, question=user.security_question, email=email)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))