# import bleach
# from flask import Blueprint, abort, jsonify, redirect, render_template, request, session, url_for, current_app
# from src.repositories.post_repository import post_repository_singleton
# from src.repositories.user_repository import user_repository_singleton
# import sqlalchemy
# from src.models import db
# import os
# from dotenv import load_dotenv
# import uuid
# from werkzeug.utils import secure_filename

# # Pillow for image processing
# from PIL import Image
# # Allowed file extensions for uploading
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# router = Blueprint('posts_router', __name__, url_prefix='/posts')

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @router.get('/')
# def posts():
#     if not user_repository_singleton.is_logged_in():
#         return redirect('/login')
#     all_posts = post_repository_singleton.get_all_posts_with_users()
#     user = user_repository_singleton.get_user_by_username(
#         user_repository_singleton.get_user_username())
#     if not user:
#         abort(401)
#     following_posts = post_repository_singleton.get_all_posts_of_followed_users(
#         user.user_id)

#     return render_template('posts.html', list_posts_active=True, all_posts=all_posts, user=user, sanitize_html=sanitize_html)

# @router.get('/edit/<int:post_id>')
# def edit_post(post_id):
#     if not user_repository_singleton.is_logged_in():
#         return redirect('/login')
#     post = post_repository_singleton.get_post_by_id(post_id)
#     user = user_repository_singleton.get_user_by_username(
#         user_repository_singleton.get_user_username())
#     if not post or not user:
#         abort(401)
#     if post.user_id is not user.user_id:
#         abort(401)
#     return render_template('edit_post.html', post=post, user=user)

# # update a post
# @router.post('/update/<int:post_id>')
# def update_post(post_id):
#     if post_id == '' or post_id is None:
#         abort(400)
#     post = post_repository_singleton.get_post_by_id(post_id)
#     user = user_repository_singleton.get_user_by_username(
#         user_repository_singleton.get_user_username())
#     if not post or not user:
#         abort(401)
#     if post.user_id is not user.user_id:
#         abort(401)
#     title = request.form.get('title')
#     description = request.form.get('text')
#     if title == '' or title is None:
#         abort(400)

#     image_upload = request.files.get('image_upload')

#     if image_upload is not None:
#         filename = secure_filename(
#             image_upload.filename) if image_upload.filename else ''
#         if filename and allowed_file(filename):
#             # Set UUID to prevent same file names
#             pic_name = str(uuid.uuid1()) + "_" + filename

#             # Save the file
#             image_upload.save(os.path.join(
#                 current_app.config['POST_UPLOAD_FOLDER'], pic_name))

#             # Verify the file is an image using Pillow
#             try:
#                 img = Image.open(os.path.join(
#                     current_app.config['POST_UPLOAD_FOLDER'], pic_name))
#                 img.verify()  # This will raise an exception if the file is not a valid image
#             except Exception as e:
#                 # Remove the invalid file
#                 os.remove(os.path.join(
#                     current_app.config['POST_UPLOAD_FOLDER'], pic_name))
#                 abort(400, description="Uploaded file is not a valid image.")
#             image_upload = pic_name

#     post_repository_singleton.update_post(
#         post_id, title, description, image_upload)
#     return redirect(f'/posts/{post_id}')

# # delete a post
# @router.post('/delete/<int:post_id>')
# def delete_post(post_id):
#     if post_id == '' or post_id is None:
#         abort(400)
#     post = post_repository_singleton.get_post_by_id(post_id)
#     user = user_repository_singleton.get_user_by_username(
#         user_repository_singleton.get_user_username())
#     if not post or not user:
#         abort(401)
#     if post.user_id is not user.user_id:
#         abort(401)
#     if post_repository_singleton.delete_post(post_id):
#         return redirect('/posts')
#     else:
#         abort(400)

# # when a user likes a post
# @router.post('/like')
# def like_post():
#     post_id = request.form.get('post_id')
#     user_id = request.form.get('user_id')
#     if post_id == '' or post_id is None or user_id == '' or user_id is None:
#         abort(400)
#     post_repository_singleton.add_like(post_id, user_id)

#     return jsonify({'status': 'success'})

# # when a user likes a comment
# @router.post('/like_comment')
# def like_comment():
#     comment_id = request.form.get('comment_id')
#     user_id = request.form.get('user_id')
#     if comment_id == '' or comment_id is None or user_id == '' or user_id is None:
#         abort(400)
#     post_repository_singleton.add_like_to_comment(comment_id, user_id)

#     return jsonify({'status': 'success'})

# # Function to sanitize HTML content
# def sanitize_html(content):
#     allowed_tags = ['p', 'div', 'em', 'strong', 'del', 'a', 'img', 'h1', 'h2',
#                     'h3', 'h4', 'h5', 'h6', 'blockquote', 'ul', 'ol', 'li', 'hr', 'br', 'pre']
#     allowed_attributes = {'*': ['class', 'style'], 'a': ['href', 'target']}

#     sanitized_content = bleach.clean(
#         content, tags=allowed_tags, attributes=allowed_attributes)
#     return sanitized_content

# # for comments and replies
# @router.post('/<int:post_id>/comment')
# @router.post('/<int:post_id>/comment/<int:parent_comment_id>')
# def comment_reply(post_id, parent_comment_id=0):
#     user = user_repository_singleton.get_user_by_username(
#         user_repository_singleton.get_user_username())
#     if user is None:
#         abort(401)
#     user_id = user.user_id
#     content = request.form.get('content')
#     reply = request.form.get('reply')
#     if reply is not None:
#         content = reply
#     if post_id == '' or post_id is None or content == '' or content is None:
#         abort(400)
#     if parent_comment_id == 0:
#         post_repository_singleton.add_comment(user_id, post_id, content)
#     else:
#         print('parent comment id: ', parent_comment_id)
#         post_repository_singleton.add_comment(
#             user_id, post_id, content, parent_comment_id)

#     return redirect(f'/posts/{post_id}')

# # Create a get request for the posts page, following posts.
# @router.get('/following')
# def following_posts():
#     if not user_repository_singleton.is_logged_in():
#         return redirect('/login')
#     user = user_repository_singleton.get_user_by_username(
#         user_repository_singleton.get_user_username())
#     if not user:
#         abort(401)
#     following_posts = post_repository_singleton.get_all_posts_of_followed_users(
#         user.user_id)

#     return render_template('posts.html', following_posts_active=True, following_posts=following_posts, user=user, sanitize_html=sanitize_html)

# # Create a get request for single post page.
# @router.get('/<int:post_id>')
# def post(post_id):
#     if not user_repository_singleton.is_logged_in():
#         return redirect('/login')
#     post = post_repository_singleton.get_post_by_id(post_id)
#     user = user_repository_singleton.get_user_by_username(
#         user_repository_singleton.get_user_username())
#     if not post or not user:
#         abort(400)

#     following = False

#     if user.is_following(post.creator):
#         following = True
#     return render_template('single_post.html', post=post, user=user, sanitize_html=sanitize_html, following=following)