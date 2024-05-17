from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app.models import PostModel, CommentModel
from app.forms import PostForm, CommentForm
from app.extensions import db
from app.utils.wordsban import filter_bad_words

postCom_bp = Blueprint("postCom", __name__)


@postCom_bp.route('/index')
@login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    post_type = request.args.get('type')
    if post_type:
        posts = PostModel.query.filter_by(post_type=post_type).order_by(PostModel.create_time.desc()).all()
    else:
        posts = PostModel.query.order_by(PostModel.create_time.desc()).all()

    return render_template('index.html', posts=posts, post_type=post_type)



@postCom_bp.route("/posts/create", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = filter_bad_words(form.title.data)
        content = filter_bad_words(form.content.data)
        post = PostModel(
            title=title,
            content=content,
            post_type=form.post_type.data,
            author_id=current_user.id,
            postcode=form.postcode.data,
        )
        db.session.add(post)
        db.session.commit()
        update_user_points(current_user, 10)
        return redirect(url_for("postCom.post_detail", post_id=post.id))
    print(form.errors)
    return render_template("posts.html", form=form)


@postCom_bp.post("/comments/create")
@login_required
def create_comment():
    form = CommentForm()
    if form.validate_on_submit():
        content = filter_bad_words(form.content.data)
        post_id = form.post_id.data
        comment = CommentModel(
            content=content,
            post_id=post_id,
            author_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        update_user_points(current_user, 5)
        return redirect(url_for("postCom.post_detail", post_id=post_id))
    post_id = form.post_id.data or request.form.get("post_id")
    return redirect(url_for("postCom.post_detail", post_id=post_id))


@postCom_bp.route("/posts/detail/<int:post_id>")
def post_detail(post_id):
    post = PostModel.query.get_or_404(post_id)
    comments = CommentModel.query.filter_by(post_id=post_id).all()
    form = CommentForm()
    is_done = post.accepted_answer_id is not None
    return render_template("post-detail.html",
                           post=post,
                           comments=comments,
                           form=form,
                           is_done=is_done)


def update_user_points(user, points):
    if user.points is None:
        user.points = 0
    user.points += points
    db.session.commit()


@postCom_bp.route('/search')
def search():
    query = request.args.get('query', '')
    scope = request.args.get('scope', 'all')  # 获取搜索范围参数，默认搜索全部
    if query:
        if scope == 'title':
            posts = PostModel.query.filter(PostModel.title.ilike(f'%{query}%')).all()
        elif scope == 'content':
            posts = PostModel.query.filter(PostModel.content.ilike(f'%{query}%')).all()
        else:
            posts = PostModel.query.filter(
                db.or_(
                    PostModel.title.ilike(f'%{query}%'),
                    PostModel.content.ilike(f'%{query}%')
                )
            ).all()
    else:
        posts = []
    return render_template('index.html', posts=posts, query=query, scope=scope)


@postCom_bp.route('/accept_comment/<int:post_id>/<int:comment_id>', methods=['POST'])
@login_required
def accept_comment(post_id, comment_id):
    comment = CommentModel.query.get_or_404(comment_id)
    post = PostModel.query.get_or_404(post_id)

    # 确保只有帖子作者可以采纳评论
    if current_user.id != post.author_id or post.accepted_answer_id is not None:
        return redirect(url_for('postCom.post_detail', post_id=post_id))

    comment.is_accepted = True
    post.accepted_answer_id = comment.id
    db.session.commit()

    return redirect(url_for('postCom.post_detail', post_id=post_id))
