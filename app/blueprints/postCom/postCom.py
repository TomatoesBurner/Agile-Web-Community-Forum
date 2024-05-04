from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user,login_required
from app.models import PostModel, CommentModel
from app.forms import PostForm, CommentForm
from app.extensions import db


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


@postCom_bp.route("/posts/create", methods=['GET', 'POST'])
@login_required
def create_question():
    form = PostForm()
    if form.validate_on_submit():
        post = PostModel(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("postCom.post_detail", post_id=post.id))
    return render_template("posts.html", form=form)

@postCom_bp.post("/comments/create")
@login_required
def create_comment():
    form = CommentForm()
    if form.validate_on_submit():
        content = form.content.data
        post_id = form.post_id.data
        comment = CommentModel(
            content=content,
            post_id=post_id,
            author_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("postCom.post_detail", post_id=post_id))

    post_id = form.post_id.data or request.form.get("post_id")
    return redirect(url_for("postCom.post_detail", post_id=post_id))

@postCom_bp.route("/posts/detail/<int:post_id>")
def post_detail(post_id):
    post = PostModel.query.get_or_404(post_id)
    comments = CommentModel.query.filter_by(post_id=post_id).all()
    form = CommentForm()
    return render_template("post-detail.html", post=post, comments=comments, form=form)