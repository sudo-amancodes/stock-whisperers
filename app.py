from flask import Flask, abort, redirect, render_template, request, url_for
import os
from dotenv import load_dotenv
from models import db, users
from flask_login import current_user, login_required
from flask_wtf import FileField

load_dotenv()

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

@app.get('/')
def index():
    return render_template('index.html')

#Create Comments or add a temporary get/post request. That has a pass statement.
#Example:
#@app.get('/test')
#def testing():
#    pass
 




#TODO: Create a get request for the upload page.
@app.get('/upload')
def upload():
    pass

#TODO: Create a post request for the upload page.
@app.post('/upload')
def upload_post():
    pass

#TODO: Create a get request for the posts page.
@app.get('/posts')
def posts():
    pass


#TODO: Create a get request for the user login page.
@app.get('/login')
def login():
    return render_template('login.html')

@app.post('/login')
def verify_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username != '' and password != '':
        return 

    #to-do
    # fliter by(username)
    # if username is in database
        # check if password matches one stored in db
            #login and route to home page 
    # if username not in db
        # display error msg and do not redirect


@app.get('/register')
def register():
    return render_template('register.html')

@app.post('/register')
def create_user():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    username = request.form.get('username')
    password = request.form.get('password')

    if username != '' and password != '' and first_name != '' and last_name != '':
        return

        # if user and pass is already in db
            # display error 'user already exists'

        # else
            # if user is not unique
                # display error username not available
            # else 
                # add user to db

#TODO: Create a get request for the profile page.
app.get('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = current_user
    profile_picture = url_for('static', filename = 'profile_pics/' + user.profile_picture)

    return render_template('profile.html', user=user, profile_picture=profile_picture)

#TODO: Create a get request for live comments.
@app.get('/comment')
def live_comment():
    pass

# TODO: Implement the 'Post Discussions' feature
@app.get('/post discussions')
def Post_discussions():
    pass

app.post('/users/<int:user_id>')
def edit_profile(user_id: int):
    user = current_user

    user.email = request.form.get('email')
    user.username = request.form.get('username')

    profile_pic = request.files['profile_picture']
    db.session.add(user)
    db.session.commit()

    return redirect(f'/profile/{user_id}', user_id=user_id)