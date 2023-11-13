from flask import Flask, abort, redirect, render_template, request, flash
from flask_bcrypt import Bcrypt 
import os
from dotenv import load_dotenv
from models import users, db, live_posts
from flask_login import login_user, login_required, logout_user, current_user, LoginManager

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
    return render_template('login.html', user=current_user)

@app.post('/login')
def verify_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == '' or password == '':
        abort(400) 

    temp_username = users.query.filter_by(username = username).first()

    if temp_username is not None:
        if bcrypt.check_password_hash(temp_username.password, password):
            flash('Successfully logged in, ' + temp_username.first_name + '!', category= 'success') 
            login_user(temp_username, remember=True)
            # figure out how to send this msg to home page
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
    # email = request.form.get('email')
    password = request.form.get('password')

    if username == '' or password == '' or first_name == '' or last_name == '':
        abort(400)

    temp_user = users.query.filter_by(username = username).first()
    if temp_user is not None:
        flash('Username already exists', category= 'error')

    if len(first_name) <= 1:
        flash('First name must be greater than 1 character', category='error')
    elif len(last_name) <= 1:
        flash('Last name must be greater than 1 character', category='error')
    elif len(username) < 4:
        flash('Username name must be at least 4 characters', category='error')
    elif len(password) < 8:
        flash('Password must be contain at least 8 characters, a number, and a special character', category='error')
    else:
        temp_user = users(first_name, last_name, username, bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(temp_user)
        db.session.commit()
        login_user(temp_user, remember= True)
        flash('account successfully created!', category= 'success')
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

# TODO: Implement the 'Post Discussions' feature
@app.get('post discussions')
def Post_discussions():
    pass
