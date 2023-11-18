from flask import Flask, abort, redirect, render_template, request, url_for, flash
# from flask_wtf import FileField
#Market Data
import yfinance as yf
import plotly.graph_objs as go 
import json
import plotly
import plotly.express as px
import pandas as pd

#Server Setup
from flask_socketio import SocketIO, emit
from threading import Lock
from flask_bcrypt import Bcrypt 
import os
from dotenv import load_dotenv
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from src.repositories.post_repository import post_repository_singleton
from src.models import db, users, live_posts
from sqlalchemy import or_
from flask_mail import Mail, Message

thread = None
thread_lock = Lock()
load_dotenv()

#Flask Initialization 
app = Flask(__name__)

#Bcrypt Initialization
bcrypt = Bcrypt(app) 
app.secret_key = 'try'


# If bugs occur with sockets then try: 
# app.config['SECRET_KEY'] = 'ABC'

#Sockets Initialization
socketio = SocketIO(app, cors_allowed_origins='*')

app.debug = True

# DB connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

db.init_app(app)

# Login Initialization
login_manager = LoginManager(app)
login_manager.login_view = '/login'

# Mail Initialization
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USER")
app.config['MAIL_PASS'] = os.getenv("EMAIL_PASS")
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

#Override Yahoo Finance
yf.pdr_override()

#Create input field for our desired stock
def get_plotly_json(stock):
    #Retrieve stock data frame (df) from yfinance API at an interval of 1m
    df = yf.download(tickers=stock,period='1d',interval='1m', threads = True)
    df['Datetime'] = df.index.strftime('%I:%M %p')

    print(df)
    #Declare plotly figure (go)
    fig=go.Figure()

    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name = 'market data'))

    fig.update_layout(
        title= str(stock)+' Live Share Price:',
        yaxis_title='Stock Price (USD per Shares)')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

def background_thread():
    print("Generating graph sensor values")
    while True:
        value = get_plotly_json('AAPL')  # Corrected stock symbol
        socketio.emit('updateGraph', {'value': value})  # Corrected event name
        socketio.sleep(10)


@app.get('/')
def index():
    graph = get_plotly_json('AAPL')
    return render_template('index.html', user=current_user, plot=graph)

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
    return render_template('posts.html', list_posts_active=True, posts=all_posts)

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

# Route for requesting password reset
app.get('/request_password_reset')
def rquest_password_form():
    return render_template('request_password_reset')

app.post('/request_password_reset')
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('index.html'))
    email = request.form.get('email')
    temp_user = users.query.filter_by(email = email).first()
    if temp_user is None:
        flash('User with associated email address does not exist. Please register first.')
        return redirect('/request_password_reset')
    
    token = users.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@stock-whisperers.com', recipients=[temp_user.email])
    msg.body = f'''To reset your password, click the following link:
    {url_for('reset_password', token = token, _external =True)}

    If you did not make this request, please ignore this email
    '''
    
    flash('An email has been sent with instructions to reset your password')
    return redirect(url_for('login.html'))
    
app.get('/password_reset')
def password_reset_form():
    return render_template('reset_password')

# Route for resetting a password
app.post('/password_reset/<token>')
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('index.html'))
    user = users.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'error')
        return redirect(url_for('reset_password_request'))
    
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    if password != confirm_password:
        flash('Passwords do not match')
        return redirect('/password_reset')
    user.password = password
    db.session.add(user)
    db.session.commit()

    return redirect('/login')
    

#TODO: Create a get request for the profile page.
@app.get('/profile/<int:user_id>')
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

@app.post('/users/<int:user_id>')
def edit_profile(user_id: int):
    user = current_user

    user.email = request.form.get('email')
    user.username = request.form.get('username')

    profile_pic = request.files['profile_picture']
    db.session.add(user)
    db.session.commit()

    return redirect(f'/profile/{user_id}', user_id=user_id)

# # TODO: Implement the 'Post Discussions' feature
# @app.get('post discussions')
# def Post_discussions():
#     pass

@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)
