from flask import Flask, abort, redirect, render_template, request, flash
from flask_bcrypt import Bcrypt 
import os
from dotenv import load_dotenv
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from src.repositories.post_repository import post_repository_singleton
from src.models import db, users, live_posts
from sqlalchemy import or_

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app) 
app.secret_key = 'try'
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.get('/')
def index():
    # temp_user = users.query.get(3)
    # db.session.delete(temp_user)
    # db.session.commit()
    return render_template('index.html', user=current_user)

#Create Comments or add a temporary get/post request. That has a pass statement.
#Example:
#@app.get('/test')
#def testing():
#    pass

#TODO: Create a get request for the upload page.
@app.get('/upload')
def upload():
    return render_template('upload.html', user = current_user)

#TODO: Create a post request for the upload page.
@app.post('/upload')
def upload_post():
    title = request.form.get('title')
    description = request.form.get('text')
    if title == '' or title is None:
        abort(400)
    created_post = post_repository_singleton.create_post(title, description)
    return redirect('/posts')

#TODO: Create a get request for the posts page.
@app.get('/posts')
def posts():
    all_posts = post_repository_singleton.get_all_posts()
    return render_template('posts.html', list_posts_active=True, posts=all_posts, user = current_user)


#TODO: Create a get request for the user login page.
@app.get('/login')
def login():
    return render_template('login.html', user=current_user)

@app.post('/login')
def verify_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == '' or password == '':
        abort(400) 

    # temp_username = users.query.filter_by(username = username).first()

    temp_username = users.query.filter(or_(users.username == username, users.email == username)).first()

    if temp_username is not None:
        if bcrypt.check_password_hash(temp_username.password, password):
            flash('Successfully logged in, ' + temp_username.first_name + '!', category= 'success') 
            login_user(temp_username, remember=True)
            return redirect('/')
        else:
            flash('Incorrect username or password', category='error')
    else:
        flash('Username does not exist', category='error')

    return redirect('/login')

@app.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.get('/register')
def register():
    return render_template('register.html', user=current_user)

@app.post('/register')
def create_user():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if username == '' or password == '' or first_name == '' or last_name == '' or email == '':
        abort(400)

    temp_user = users.query.filter(or_(users.username == username, users.email == email)).first()
    if temp_user is not None:
        if temp_user.email is not None:
            flash('email already exists', category= 'error')
        elif temp_user.username is not None:
            flash('username already exists', category= 'error')
            
        return redirect('/register')
    
    if len(first_name) <= 1:
        flash('First name must be greater than 1 character', category='error')
    elif len(last_name) <= 1:
        flash('Last name must be greater than 1 character', category='error')
    elif len(username) < 4:
        flash('Username name must be at least 4 characters', category='error')
    elif len(password) < 8:
        flash('Password must be contain at least 8 characters, a number, and a special character', category='error')
    else:
        temp_user = users(first_name, last_name, username, email, bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(temp_user)
        db.session.commit()
        login_user(temp_user, remember = True)
        flash('account successfully created!', category = 'success')
        return redirect('/')

    return redirect('/register')

#TODO: Create a get request for the profile page.
app.get('/profile')
def profile():
    pass  

#TODO: Create a get request for live comments.
@app.get('/comment')
def live_comment():
    pass

# # TODO: Implement the 'Post Discussions' feature
# @app.get('post discussions')
# def Post_discussions():
#     pass
