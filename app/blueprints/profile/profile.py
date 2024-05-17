from flask import Blueprint, send_from_directory, current_app, redirect, url_for, render_template, flash,request
from flask_login import current_user, login_required
from app.forms import UploadImageForm, EditAboutMeForm, EditUsernameForm
from hashlib import md5
from app.extensions import db
from app.utils.wordsban import filter_bad_words
from app.models import UserModel, PostModel, CommentModel, Notification
import os
import time

profile_bp = Blueprint("profile", __name__)

# View function to display user profile overview
@profile_bp.route("/profile")
@login_required
def overview_profile():
    user = UserModel.query.get_or_404(current_user.id)
    posts = PostModel.query.filter_by(author_id=current_user.id).order_by(PostModel.create_time.desc()).all()
    comments = CommentModel.query.filter_by(author_id=current_user.id).order_by(CommentModel.create_time.desc()).all()

    avatar_form = UploadImageForm()
    about_me_form = EditAboutMeForm(obj=user)
    username_form = EditUsernameForm(obj=user)

    return render_template('profile.html',
                           user=user,
                           posts=posts,
                           comments=comments,
                           avatar_form=avatar_form,
                           about_me_form=about_me_form,
                           username_form=username_form)

# Route to serve user avatars
@profile_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config["AVATARS_SAVE_PATH"], filename)



# View function to handle username edit form submission
@profile_bp.post("/profile/edit/username")
@login_required
def edit_username():
    username_form = EditUsernameForm()
    if username_form.validate_on_submit():
        new_username = filter_bad_words(username_form.username.data)
        current_user.username = new_username
        db.session.commit()
        return redirect(url_for('profile.overview_profile'))
    else:
        return redirect(url_for('profile.overview_profile'))

# View function to handle post deletion
@profile_bp.post("/posts/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    post = PostModel.query.get_or_404(post_id)

    # Check if the current user is the author of the post
    if post.author_id != current_user.id:
        flash("You are not authorized to delete this post.", "error")
        return redirect(url_for('profile.overview_profile'))

    else:
        # Delete comments related to the post
        comments = CommentModel.query.filter_by(post_id=post_id).all()
        for comment in comments:
            db.session.delete(comment)

        # Delete notifications related to the post
        notifications = Notification.query.filter_by(post_id=post_id).all()
        for notification in notifications:
            db.session.delete(notification)

        # Delete the post itself
        db.session.delete(post)
        db.session.commit()


    tab = request.args.get('tab', 'Posts')
    return redirect(url_for('profile.overview_profile', tab=tab))

# View function to handle avatar upload
@profile_bp.post("/avatars/upload")
@login_required
def update_avatar():
    avatar_form = UploadImageForm()
    if avatar_form.validate_on_submit():
        image = avatar_form.image.data
        filename = image.filename
        _, ext = os.path.splitext(filename)
        filename = md5((current_user.email + str(time.time())).encode("utf-8")).hexdigest() + ext
        image_path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], filename)
        image.save(image_path)
        current_user.avatar = filename
        db.session.commit()
        return redirect(url_for('profile.overview_profile'))
    else:
        print(avatar_form.errors)
        return redirect(url_for('profile.overview_profile'))

# View function to handle comment deletion
@profile_bp.post("/comments/delete/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    comment = CommentModel.query.get_or_404(comment_id)

    # Check if the current user is the author of the comment
    if comment.author_id != current_user.id:
        flash("You are not authorized to delete this comment.", "error")
        return redirect(url_for('profile.overview_profile'))

    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted successfully.", "success")

    tab = request.args.get('tab', 'Posts')
    return redirect(url_for('profile.overview_profile', tab=tab))