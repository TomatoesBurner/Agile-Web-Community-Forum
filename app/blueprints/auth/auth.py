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


# Route for logging in users, accessible via both "/" and "/login"
@auth_bp.route("/", methods=['GET', 'POST'])
@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    # Redirect authenticated users to the main page
    if current_user.is_authenticated:
        return redirect(url_for('postCom.index'))

    # Create an instance of the login form
    form = LoginForm()

    # Validate the form when submitted
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = UserModel.query.filter_by(email=email).first()

        # Check if the user exists and the password is correct
        if user is None or not user.check_password(password):
            flash('Invalid username or password')  # Flash message for invalid login attempt
            return render_template("login.html", form=form), 200

        # Log in the user
        login_user(user, remember=form.remember.data)

        # Redirect to the next page if specified, otherwise to the main page
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('postCom.index')
        return redirect(next_page)

    # Render the login template
    return render_template("login.html", form=form)


# Route for registering new users
@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    # Redirect authenticated users to the main page
    if current_user.is_authenticated:
        return redirect(url_for('postCom.index'))

    # Create an instance of the registration form
    form = RegisterForm()

    # Validate the form when submitted
    if form.validate_on_submit():
        email = form.email.data
        username = filter_bad_words(form.username.data)  # Filter bad words from username

        # Generate an identicon for the user's avatar
        identicon = Identicon()
        filenames = identicon.generate(text=md5(email.encode("utf-8")).hexdigest())
        avatar = filenames[2]

        # Create a new user instance
        user = UserModel(
            email=email,
            username=username,
            avatar=avatar,
            security_question=form.security_question.data
        )

        # Set the user's password and security answer
        user.set_password(form.password.data)
        user.set_security_question = form.security_question.data
        user.set_security_answer(form.security_answer.data)

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')  # Flash message for successful registration
        return redirect(url_for("auth.login"))

    # Render the registration template
    return render_template("register.html", form=form)

# Route for handling forgotten passwords
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
    return render_template('forgot-password.html', forgot_form=form, email_error=email_error)


# Route for verifying security questions during password reset
@auth_bp.route('/security_question', methods=['GET', 'POST'])
def security_question():
    email = request.args.get('email')
    user = UserModel.query.filter_by(email=email).first()

    # Check if the user exists
    if not user:
        flash('Invalid email address', 'error')  # Flash message for invalid email
        return redirect(url_for('auth.forgot-password'))

    # Create an instance of the security question form
    form = SecurityQuestionForm()

    # Validate the form when submitted
    if form.validate_on_submit():
        # Check if the security answer is correct
        if user.check_security_answer(form.security_answer.data):
            # Check if the new password and confirmation match
            if form.new_password.data != form.confirm_password.data:
                form.confirm_password.errors.append('Passwords do not match')  # Error for mismatched passwords
            else:
                # Update the user's password
                user.set_password(form.new_password.data)
                db.session.commit()
                flash('Your password has been reset!')  # Flash message for successful password reset
                return redirect(url_for('auth.login'))
        else:
            form.security_answer.errors.append(
                'Incorrect answer to the security question')  # Error for incorrect answer

    # Render the security question template
    return render_template('security-question.html', form=form, question=user.security_question, email=email)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))