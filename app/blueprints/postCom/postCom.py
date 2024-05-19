from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user,login_required
from app.models import PostModel, CommentModel
from app.forms import PostForm, CommentForm
from app.extensions import db
from config import Config
from app.utils.wordsban import filter_bad_words

postCom_bp = Blueprint("postCom", __name__)

# Route for the main page displaying posts
@postCom_bp.route('/index')
@login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    post_type = request.args.get('type')
    page = request.args.get('page', 1, type=int)
    per_page = Config.POSTS_PER_PAGE
    if post_type:
        posts = PostModel.query.filter_by(post_type=post_type).order_by(PostModel.create_time.desc()).paginate(
            page=page, per_page=per_page, error_out=False)
    else:
        posts = PostModel.query.order_by(PostModel.create_time.desc()).paginate(page=page, per_page=per_page,
                                                                                error_out=False)
    return render_template('index.html', posts=posts.items, pagination=posts, post_type=post_type)


# Route for creating a new post
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

# Route for creating a new comment
@postCom_bp.route("/comment/create", methods=['GET', 'POST'])
@login_required
def create_comment():
    form = CommentForm()
    if form.validate_on_submit():
        content = filter_bad_words(form.content.data)
        post_id = form.post_id.data

        # Create the comment
        comment = CommentModel(
            content=content,
            post_id=post_id,
            author_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()

        # Update user points
        update_user_points(current_user, 5)

        # Retrieve the post's author information
        post = db.session.query(PostModel).filter_by(id=post_id).first()
        if post and post.author:  # 确保帖子和作者存在
            # 使用作者用户对象调用add_notification
            truncated_title = ' '.join(post.title.split()[:5])
            message_data = {
                'message': f"Your post ('{truncated_title}...') has received a new comment by '{current_user.username}'."}
            post.author.add_notification('new_comment', message_data, post_id=post_id)
            db.session.commit()
        return redirect(url_for("postCom.post_detail", post_id=post_id))
    post_id = form.post_id.data or request.form.get("post_id")
    return redirect(url_for("postCom.post_detail", post_id=post_id))

# Route for viewing post details and comments
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

# Function to update user points
def update_user_points(user, points):
    if user.points is None:
        user.points = 0
    user.points += points
    db.session.commit()

# Route for searching posts
@postCom_bp.route('/search')
def search():
    query = request.args.get('query', '')
    scope = request.args.get('scope', 'all')  # default all
    page = request.args.get('page', 1, type=int)
    per_page = Config.POSTS_PER_PAGE

    if query:
        if scope == 'title':
            posts_query = PostModel.query.filter(PostModel.title.ilike(f'%{query}%'))
        elif scope == 'content':
            posts_query = PostModel.query.filter(PostModel.content.ilike(f'%{query}%'))
        elif scope == 'postcode':
            posts_query = PostModel.query.filter(PostModel.postcode == query)
        else:
            posts_query = PostModel.query.filter(
                db.or_(
                    PostModel.title.ilike(f'%{query}%'),
                    PostModel.content.ilike(f'%{query}%')
                )
            )
    else:
        posts_query = PostModel.query.filter_by()

    pagination = posts_query.order_by(PostModel.create_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items

    return render_template('index.html', posts=posts, pagination=pagination, query=query, scope=scope)

# Route for accepting a comment as the answer to a post
@postCom_bp.route('/accept_comment/<int:post_id>/<int:comment_id>', methods=['POST'])
@login_required
def accept_comment(post_id, comment_id):
    comment = CommentModel.query.get_or_404(comment_id)
    post = PostModel.query.get_or_404(post_id)

    if current_user.id != post.author_id or post.accepted_answer_id is not None:
        return redirect(url_for('postCom.post_detail', post_id=post_id))

    if comment.author_id == post.author_id:
        return redirect(url_for("postCom.post_detail", post_id=post_id))

    comment.is_accepted = True
    post.accepted_answer_id = comment.id
    db.session.commit()

    return redirect(url_for('postCom.post_detail', post_id=post_id))
