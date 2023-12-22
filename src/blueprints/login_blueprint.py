# from datetime import datetime, timedelta
# from random import random
# from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, session, url_for, current_app
# from src.repositories.post_repository import post_repository_singleton
# from src.repositories.user_repository import user_repository_singleton
# from src.models import db, users
# from sqlalchemy import or_, func
# from flask_mail import Mail, Message
# # from app import bcrypt

# # current_app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# # current_app.config['MAIL_PORT'] = 587
# # current_app.config['MAIL_USE_TLS'] = True
# # current_app.config['MAIL_USERNAME'] = 'the.stock.whisperers@gmail.com'
# # current_app.config['MAIL_PASSWORD'] = 'spwlegjkdfjabdhx'
# router = Blueprint('login_router', __name__,)
# mail = Mail()
# code = 0
# temp_user_info = []
# # bcrypt = current_app.extensions['bcrypt']

# def send_verification_email(email):
#     mail.init_app(current_app)
#     if not email:
#         abort(403)
#     global code
#     code = random.randint(100000, 999999)
#     msg = Message('Verification code',
#                   sender='noreply@stock-whisperers.com', recipients=[email])
#     msg.body = f'''Enter the 6-digit code below to verify your identity.

# {code}

# If you did not make this request, please ignore this email
# '''
#     mail.send(msg)

# @router.get('/login')
# def login():
#     if user_repository_singleton.is_logged_in():
#         flash('You are already logged in', category='error')
#         return redirect('/')
#     return render_template('login.html', user=session.get('user'))

# @router.post('/login')
# def verify_login():
#     # bcrypt = current_app.config['bcrypt']
#     if user_repository_singleton.is_logged_in():
#         flash('You are already logged in', category='error')
#         return redirect('/')
#     username = request.form.get('username')
#     password = request.form.get('password')

#     if not username or not password:
#         flash('Please enter a username and a password', category='error')
#         return redirect('/login')

#     temp_username = users.query.filter((func.lower(users.username) == username.lower()) | (
#         func.lower(users.email) == username.lower())).first()
#     if temp_username is not None:
#         if bcrypt.check_password_hash(temp_username.password, password):
#             time_difference = datetime.utcnow() - temp_username.last_login

#             if time_difference > timedelta(days=14):
#                 send_verification_email(temp_username.email)
#                 return redirect(f'/verify_user/{temp_username.username}/login')
#             else:
#                 flash('Successfully logged in, ' +
#                       temp_username.first_name + '!', category='success')
#                 user_repository_singleton.login_user(temp_username)
#                 return redirect('/')
#         else:
#             flash('Incorrect username or password', category='error')
#     else:
#         flash('Username does not exist', category='error')

#     return redirect('/login')

# @router.get('/register')
# def register():
#     if user_repository_singleton.is_logged_in():
#         flash('You are already logged in. Logout to make a new account', category='error')
#         return redirect('/')
#     return render_template('register.html', user=session.get('user'))

# @router.post('/register')
# def create_user():
#     bcrypt = current_app.extensions['bcrypt']
#     if user_repository_singleton.is_logged_in():
#         flash('You are already logged in. Logout to make a new account', category='error')
#         return redirect('/')
#     first_name = request.form.get('first-name')
#     last_name = request.form.get('last-name')
#     username = request.form.get('username')
#     email = request.form.get('email')
#     password = request.form.get('password')

#     profile_picture = 'default-profile-pic.jpg'

#     if not username or not password or not first_name or not last_name or not email:
#         flash('Please fill out all of the fields')
#         return redirect('/register')

#     temp_user = users.query.filter((func.lower(users.username) == username.lower()) | (
#         func.lower(users.email) == email.lower())).first()
#     if temp_user is not None:
#         if temp_user.email.lower() == email.lower():
#             flash('email already exists', category='error')
#         elif temp_user.username.lower() == username.lower():
#             flash('username already exists', category='error')

#         return redirect('/register')

#     if user_repository_singleton.validate_input(first_name, last_name, username, password):
#         global temp_user_info
#         temp_user_info = [first_name, last_name, username, email,
#                         bcrypt.generate_password_hash(password).decode(), profile_picture]
#         send_verification_email(email)
#         return redirect(f'/verify_user/{username}/signup')

#     return redirect('/register')


# @router.get('/verify_user/<username>/<method>')
# def verify_user(username, method):
#     return render_template('verify_user.html', username=username, method=method)


# @router.post('/verify_user/<username>/<method>')
# def verify_code(username, method):
#     global code
#     user_code = request.form.get('user-code')
#     if not user_code:
#         flash('Please enter in a code.', category='error')
#         return redirect(f'/verify_user/{username}/{method}')
#     if str(code) != str(user_code):
#         flash('Incorrect code. Try Again', category='error')
#         return redirect(f'/verify_user/{username}/{method}')

#     if method == "signup":
#         user_repository_singleton.add_user(
#             temp_user_info[0], temp_user_info[1], temp_user_info[2], temp_user_info[3], temp_user_info[4], temp_user_info[5])
#         user = user_repository_singleton.get_user_by_username(
#             temp_user_info[2])
#         if not user:
#             abort(403)
#         user_repository_singleton.login_user(user)
#         flash('Successfully created an account. Welcome, ' +
#               user.first_name + '!', category='success')
#         return redirect('/')

#     user = user_repository_singleton.get_user_by_username(username)
#     if not user:
#         abort(403)
#     flash('Successfully logged in, ' + user.first_name + '!', category='success')
#     user_repository_singleton.login_user(user)
#     return redirect('/')

# # Route for requesting password reset
# @router.get('/request_password_reset')
# def request_password_form():
#     return render_template('request_password_reset.html')


# @router.post('/request_password_reset')
# def request_password_reset():
#     if user_repository_singleton.is_logged_in():
#         return redirect(url_for('index.html'))
#     email = request.form.get('email')
#     if not email:
#         flash('please enter an email address.', category='error')
#         return redirect('/request_password_reset')
#     temp_user = users.query.filter_by(email=email).first()
#     if not temp_user:
#         flash('User with associated email address does not exist. Please register first.', category='error')
#         return redirect('/request_password_reset')
#     token = temp_user.get_reset_token()
#     msg = Message('Password Reset Request',
#                 sender='noreply@stock-whisperers.com', recipients=[temp_user.email])
#     msg.body = f'''To reset your password, click the following link:
# {url_for('password_reset', token = token, _external = True)}

# If you did not make this request, please ignore this email
# '''
#     mail.send(msg)
#     flash('An email has been sent with instructions to reset your password',
#         category='success')
#     return redirect(url_for('verify_login'))


# @router.get('/password_reset/<token>')
# def password_reset_form(token):
#     if user_repository_singleton.is_logged_in():
#         return redirect('/')
#     user = users.verify_reset_token(token)
#     if not user:
#         flash('Invalid or expired token', category='error')
#         return redirect('/login')
#     return render_template('reset_password.html', token=token)

# # Route for resetting a password
# @router.post('/password_reset/<token>')
# def password_reset(token):
#     # bcrypt = current_app.config['bcrypt']
#     if user_repository_singleton.is_logged_in():
#         return redirect('/')
#     user = users.verify_reset_token(token)
#     if user is None:
#         flash('Invalid or expired token', category='error')
#         return redirect('/request_password_reset')

#     password = request.form.get('password')
#     confirm_password = request.form.get('confirm-password')
#     if not password or not confirm_password:
#         flash('Please fill out all of the fileds',  category='error')
#     elif password != confirm_password:
#         flash('Passwords do not match',  category='error')
#     elif (len(password) < 6) or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password) or any(char.isspace() for char in password):
#         flash('Password must contain at least 6 characters, a letter, a number, and no spaces', category='error')
#     else:
#         user.password = bcrypt.generate_password_hash(password).decode()
#         db.session.commit()
#         flash('Your password has been updated!', category = 'success')
#         return redirect('/login')

#     return redirect(f'/password_reset/{token}')

# @router.post('/logout')
# def logout():
#     if not user_repository_singleton.is_logged_in():
#         flash('Unable to logout because you are not logged in.', category='error')
#         return redirect('/')
#     user_repository_singleton.logout_user()
#     return redirect('/login')
