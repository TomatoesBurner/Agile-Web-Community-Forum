from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user


postCom_bp = Blueprint("postCom", __name__)

@postCom_bp.route('/index')
def index():
    if current_user.is_authenticated:
        posts = [
            {
                'author': {'username': 'John'},
                'body': 'Beautiful day in Portland!'
            },
            {
                'author': {'username': 'Susan'},
                'body': 'The Avengers movie was so cool!'
            }
        ]
        return render_template("index.html", title='Home Page', posts=posts)
    return redirect(url_for('auth.login'))
