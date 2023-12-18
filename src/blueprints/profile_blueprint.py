import os
import uuid
import bleach
from flask import Blueprint, Flask, abort, redirect, render_template, request, url_for, flash, jsonify, session, blueprints, current_app
from src.models import users, db
from src.repositories.user_repository import user_repository_singleton
from src.repositories.post_repository import post_repository_singleton
from werkzeug.utils import secure_filename
from PIL import Image

router = Blueprint('profile_router', __name__, url_prefix='/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_html(content):
    allowed_tags = ['p', 'div', 'em', 'strong', 'del', 'a', 'img', 'h1', 'h2',
                    'h3', 'h4', 'h5', 'h6', 'blockquote', 'ul', 'ol', 'li', 'hr', 'br', 'pre']
    allowed_attributes = {'*': ['class', 'style'], 'a': ['href', 'target']}

    sanitized_content = bleach.clean(
        content, tags=allowed_tags, attributes=allowed_attributes)
    return sanitized_content

@router.post('/<string:username>/edit/delete')
def delete(username):
    if not user_repository_singleton.is_logged_in():
        flash('Unable to delete account because you are not logged in.', category='error')
        return redirect('/')
    user_repository_singleton.remove_user(username)
    user_repository_singleton.logout_user()
    flash('Account deleted', category='success')
    return redirect('/register')

# Create a get request for the profile page.
@router.get('/<string:username>')
def profile(username: str):
    if not user_repository_singleton.is_logged_in():
        return redirect('/login')
        # user = user_repository_singleton.get_user_by_username(username)
        # if not user:
        #     abort(403)
        # profile_picture = url_for(
        #     'static', filename='profile_pics/' + user.profile_picture)

    user = user_repository_singleton.get_user_by_username(username)
    if not user:
        abort(403)

    logged_in_user = user_repository_singleton.get_user_by_user_id(user_repository_singleton.get_user_user_id())
    if not logged_in_user:
        abort(403)
    is_following = False
    if logged_in_user.is_following(user):
        is_following = True
    
    posts = post_repository_singleton.get_user_posts(user.user_id)

    profile_picture = url_for(
        'static', filename='profile_pics/' + user.profile_picture)
    return render_template('profile.html', user=user, profile_picture=profile_picture, posts=posts, followers = user.get_all_followers(), following = user.get_all_following(), sanitize_html=sanitize_html, is_following=is_following)



@router.get('/<string:username>/edit')
def get_edit_profile_page(username: str):
    if not user_repository_singleton.is_logged_in():
        abort(401)

    user_to_edit = users.query.filter_by(username=username).first()
    if user_to_edit is None:
        redirect(f'/profile/{username}')
    return render_template('edit_profile.html', user=user_to_edit)


@router.post('/<string:username>')
def update_profile(username: str):
    if 'user' not in session:
        abort(401)

    user_to_edit = users.query.filter_by(username=username).first()

    if not user_to_edit:
        abort(403)

    new_email = request.form.get('email')
    new_username = request.form.get('username')
    new_fname = request.form.get('first_name')
    new_lname = request.form.get('last_name')

    existing_user = users.query.filter_by(username=new_username).first()
    existing_email = users.query.filter_by(email=new_email).first()

    if existing_user and existing_user != user_to_edit:
        flash('Username already in use', 'error')
        return redirect(f'/profile/{username}/edit')
    if existing_email and existing_email != user_to_edit:
        flash('Email already in use', 'error')
        return redirect(f'/profile/{username}/edit')

    profile_picture = request.files['image_upload']
    if profile_picture:
        filename = secure_filename(profile_picture.filename)
        if filename and allowed_file(filename):
        # Set UUID to prevent same file names
            pic_name = str(uuid.uuid1()) + "_" + filename
            profile_picture.save(os.path.join(
            current_app.config['UPLOAD_FOLDER'], pic_name))
            try:
                img = Image.open(os.path.join(
                current_app.config['UPLOAD_FOLDER'], pic_name))
                img.verify()
            except Exception as e:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name))
                abort(400, description="Upload file is not a valid image")
            user_to_edit.profile_picture = pic_name

    user_to_edit.email = new_email
    user_to_edit.username = new_username
    user_to_edit.first_name = new_fname
    user_to_edit.last_name = new_lname

    user_repository_singleton.login_user(user_to_edit)

    db.session.add(user_to_edit)
    db.session.commit()

    return redirect(f'/profile/{new_username}')