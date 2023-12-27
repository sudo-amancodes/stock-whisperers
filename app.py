import uuid
from flask import Flask, abort, redirect, render_template, request, url_for, flash, jsonify, session, blueprints
from flask_wtf.file import FileField, FileAllowed

# from flask_wtf import FileField
# Market Data
import yfinance as yf

# Server Setup
from flask_socketio import SocketIO, emit, send
from threading import Lock
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from src.repositories.post_repository import post_repository_singleton
from src.repositories.user_repository import user_repository_singleton
from sqlalchemy import or_, func
from flask_mail import Mail, Message
from src.models import db, users, live_posts, Post, friendships
from datetime import datetime, timedelta
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from werkzeug.utils import secure_filename
# Bleach to prevent cross-site scripting (XSS) attacks, possible when user is posting a comment
import bleach
from src.blueprints.posts_blueprint import router as posts_router, sanitize_html
# from src.blueprints.login_blueprint import router as login_router
from src.blueprints.profile_blueprint import router as profile_router

# Pillow for image processing
from PIL import Image
import secrets

# Allowed file extensions for uploading
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

thread = None
thread_lock = Lock()
load_dotenv()

# Flask Initialization
app = Flask(__name__)

# Bcrypt Initialization
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY', 'default')

# If bugs occur with sockets then try:
# app.config['SECRET_KEY'] = 'ABC'

# Sockets Initialization
socketio = SocketIO(app, cors_allowed_origins='*')

app.debug = True

app.register_blueprint(posts_router)
# app.register_blueprint(login_router, bcrypt = bcrypt)
app.register_blueprint(profile_router)


# DB connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

# Deploy DB connection
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')

UPLOAD_FOLDER = 'static/profile_pics/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['POST_UPLOAD_FOLDER'] = 'static/post_pics/'

db.init_app(app)

# Make sure you are not on school wifi when trying to send emails, it will not work.
# Mail Initialization
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'the.stock.whisperers@gmail.com'
app.config['MAIL_PASSWORD'] = 'spwlegjkdfjabdhx'
mail = Mail(app)

# Variables to use for email verification
code = 0
temp_user_info = []

# Override Yahoo Finance
yf.pdr_override()
global current_symbol

def background_thread():
    print("Generating random sensor values")
    global current_symbol
    ticker = current_symbol
    while True:
        symbol = yf.Ticker(ticker)
        df = symbol.history(period='1d', interval='1m')

        last_close_price = correct_graph_cols(df.tail(2))
        df = correct_graph_cols(df.tail(1))
        
        # time = df.iloc[-1]['date']

        open = last_close_price.iloc[-2]['close']

        if 'high' in locals() and high < df.iloc[-1]['high']:
            high = df.iloc[-1]['high']
        elif 'high' not in locals():
            high = df.iloc[-1]['high']

        if 'low' in locals() and low > df.iloc[-1]['low']:
            low = df.iloc[-1]['low']
        elif 'low' not in locals():
            low = df.iloc[-1]['low']

        close = df.iloc[-1]['close']

        df.loc[0,'open'] = open
        df.loc[0,'high'] = high
        df.loc[0,'low'] = low
        df.loc[0,'close'] = close
        
        if ticker == current_symbol:
            socketio.emit('updateSensorData', {'value': df.to_json()})
        else:
            del open
            del high
            del low
            del close
        ticker = current_symbol
        socketio.sleep(5)


def correct_graph_cols(df):
    df = df.reset_index()
    df.columns = df.columns.str.lower()
    return df.rename(columns={"datetime": "date"})

# Retrieve stock data frame (df) from yfinance API at an interval of 1m
def previous_graph(ticker):

    global current_symbol
    current_symbol = ticker
    print(current_symbol)
    symbol = yf.Ticker(ticker)
    df = symbol.history(period='5d', interval='1m')
    return correct_graph_cols(df)

@app.get('/')
def index():
    return render_template('index.html', user=session.get('user'))

@app.get('/data')
def data(): 
    ticker = 'SPY'
    
    df = previous_graph(ticker)
    return df.to_json(orient='records')

@app.post('/data')
def set_data():
    jsonData = request.get_json()
    if jsonData != None:
        ticker = jsonData['Stock']

    df = previous_graph(ticker)
    return df.to_json(orient='records')

@app.post('/watchlist')
def get_watchlist():
    ticker = request.get_json()['ticker']
    data = yf.Ticker(ticker).history(period='1y')
    print(data.iloc[-1].Open)
    return jsonify({'currentPrice': data.iloc[-1].Close,
                    'openPrice':data.iloc[-1].Open})

# Create a get request for the upload page.
@app.get('/upload')
def upload():
    if not user_repository_singleton.is_logged_in():
        return redirect('/login')
    return render_template('upload.html', user=session.get('user'))

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a post request for the upload page.
@app.post('/upload')
def upload_post():
    title = request.form.get('title')
    description = request.form.get('text')
    if title == '' or title is None:
        abort(400)
    user = user_repository_singleton.get_user_by_username(
        user_repository_singleton.get_user_username())

    if user is None:
        abort(401)

    created_post = post_repository_singleton.create_post(
        title, description, user.user_id)

    image_upload = request.files.get('image_upload')

    if image_upload is not None:
        filename = secure_filename(
            image_upload.filename) if image_upload.filename else ''
        if filename and allowed_file(filename):
            # Set UUID to prevent same file names
            pic_name = str(uuid.uuid1()) + "_" + filename

            # Save the file
            image_upload.save(os.path.join(
                app.config['POST_UPLOAD_FOLDER'], pic_name))

            # Verify the file is an image using Pillow
            try:
                img = Image.open(os.path.join(
                    app.config['POST_UPLOAD_FOLDER'], pic_name))
                img.verify()  # This will raise an exception if the file is not a valid image
            except Exception as e:
                # Remove the invalid file
                os.remove(os.path.join(
                    app.config['POST_UPLOAD_FOLDER'], pic_name))
                abort(400, description="Uploaded file is not a valid image.")

            created_post.file_upload = pic_name
            db.session.commit()

    return redirect('/posts')

# when a user follows another user
@app.post('/follow/<int:user_to_follow_id>')
def follow_user(user_to_follow_id):
    user_id = user_repository_singleton.get_user_user_id()
    if user_id == '' or user_id is None or user_to_follow_id == '' or user_to_follow_id is None or user_id == user_to_follow_id:
        abort(400)
    user_repository_singleton.follow_user(user_id, user_to_follow_id)

    return jsonify({'status': 'success'})

# format timestamp to display how long ago a post was made
@app.template_filter('time_ago')
def time_ago_filter(timestamp):
    now = datetime.now()
    time_difference = now - timestamp

    if time_difference < timedelta(minutes=1):
        return 'just now'
    elif time_difference < timedelta(hours=1):
        minutes = int(time_difference.total_seconds() / 60)
        return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
    elif time_difference < timedelta(days=1):
        hours = int(time_difference.total_seconds() / 3600)
        return f'{hours} hour{"s" if hours != 1 else ""} ago'
    else:
        days = int(time_difference.total_seconds() / (3600 * 24))
        return f'{days} day{"s" if days != 1 else ""} ago'

@app.get('/login')
def login():
    if user_repository_singleton.is_logged_in():
        flash('You are already logged in', category='error')
        return redirect('/')
    return render_template('login.html', user=session.get('user'))

@app.post('/login')
def verify_login():
    if user_repository_singleton.is_logged_in():
        flash('You are already logged in', category='error')
        return redirect('/')
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Please enter a username and a password', category='error')
        return redirect('/login')

    temp_username = users.query.filter((func.lower(users.username) == username.lower()) | (
        func.lower(users.email) == username.lower())).first()
    if temp_username is not None:
        if bcrypt.check_password_hash(temp_username.password, password):
            time_difference = datetime.utcnow() - temp_username.last_login

            if time_difference > timedelta(days=14):
                send_verification_email(temp_username.email)
                return redirect(f'/verify_user/{temp_username.username}/login')
            else:
                flash('Successfully logged in, ' +
                      temp_username.first_name + '!', category='success')
                user_repository_singleton.login_user(temp_username)
                return redirect('/')
        else:
            flash('Incorrect username or password', category='error')
    else:
        flash('Username does not exist', category='error')

    return redirect('/login')

def send_verification_email(email):
    if not email:
        abort(403)
    global code
    code = secrets.SystemRandom().randint(100000, 999999)
    msg = Message('Verification code',
                  sender='noreply@stock-whisperers.com', recipients=[email])
    msg.body = f'''Enter the 6-digit code below to verify your identity.

{code}

If you did not make this request, please ignore this email
'''
    mail.send(msg)
    
@app.post('/logout')
def logout():
    if not user_repository_singleton.is_logged_in():
        flash('Unable to logout because you are not logged in.', category='error')
        return redirect('/')
    user_repository_singleton.logout_user()
    return redirect('/login')

@app.get('/register')
def register():
    if user_repository_singleton.is_logged_in():
        flash('You are already logged in. Logout to make a new account', category='error')
        return redirect('/')
    return render_template('register.html', user=session.get('user'))

@app.post('/register')
def create_user():
    if user_repository_singleton.is_logged_in():
        flash('You are already logged in. Logout to make a new account', category='error')
        return redirect('/')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    profile_picture = 'default-profile-pic.jpg'

    if not username or not password or not first_name or not last_name or not email:
        flash('Please fill out all of the fields')
        return redirect('/register')

    temp_user = users.query.filter((func.lower(users.username) == username.lower()) | (
        func.lower(users.email) == email.lower())).first()
    if temp_user is not None:
        if temp_user.email.lower() == email.lower():
            flash('email already exists', category='error')
        elif temp_user.username.lower() == username.lower():
            flash('username already exists', category='error')

        return redirect('/register')

    if user_repository_singleton.validate_input(first_name, last_name, username, password):
        global temp_user_info
        temp_user_info = [first_name, last_name, username, email,
                        bcrypt.generate_password_hash(password).decode(), profile_picture]
        send_verification_email(email)
        return redirect(f'/verify_user/{username}/signup')

    return redirect('/register')

@app.get('/verify_user/<username>/<method>')
def verify_user(username, method):
    return render_template('verify_user.html', username=username, method=method)

@app.post('/verify_user/<username>/<method>')
def verify_code(username, method):
    global code
    user_code = request.form.get('user-code')
    if not user_code:
        flash('Please enter in a code.', category='error')
        return redirect(f'/verify_user/{username}/{method}')
    if str(code) != str(user_code):
        flash('Incorrect code. Try Again', category='error')
        return redirect(f'/verify_user/{username}/{method}')

    if method == "signup":
        user_repository_singleton.add_user(
            temp_user_info[0], temp_user_info[1], temp_user_info[2], temp_user_info[3], temp_user_info[4], temp_user_info[5])
        user = user_repository_singleton.get_user_by_username(
            temp_user_info[2])
        if not user:
            abort(403)
        user_repository_singleton.login_user(user)
        flash('Successfully created an account. Welcome, ' +
              user.first_name + '!', category='success')
        return redirect('/')

    user = user_repository_singleton.get_user_by_username(username)
    if not user:
        abort(403)
    flash('Successfully logged in, ' + user.first_name + '!', category='success')
    user_repository_singleton.login_user(user)
    return redirect('/')

# Route for requesting password reset
@app.get('/request_password_reset')
def request_password_form():
    return render_template('request_password_reset.html')

@app.post('/request_password_reset')
def request_password_reset():
    if user_repository_singleton.is_logged_in():
        return redirect(url_for('index.html'))
    email = request.form.get('email')
    if not email:
        flash('please enter an email address.', category='error')
        return redirect('/request_password_reset')
    temp_user = users.query.filter_by(email=email).first()
    if not temp_user:
        flash('User with associated email address does not exist. Please register first.', category='error')
        return redirect('/request_password_reset')
    token = temp_user.get_reset_token()
    msg = Message('Password Reset Request',
                sender='noreply@stock-whisperers.com', recipients=[temp_user.email])
    msg.body = f'''To reset your password, click the following link:
{url_for('password_reset', token = token, _external = True)}

If you did not make this request, please ignore this email
'''
    mail.send(msg)
    flash('An email has been sent with instructions to reset your password',
        category='success')
    return redirect(url_for('verify_login'))

@app.get('/password_reset/<token>')
def password_reset_form(token):
    if user_repository_singleton.is_logged_in():
        return redirect('/')
    user = users.verify_reset_token(token)
    if not user:
        flash('Invalid or expired token', category='error')
        return redirect('/login')
    return render_template('reset_password.html', token=token)

# Route for resetting a password
@app.post('/password_reset/<token>')
def password_reset(token):
    if user_repository_singleton.is_logged_in():
        return redirect('/')
    user = users.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', category='error')
        return redirect('/request_password_reset')

    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    if not password or not confirm_password:
        flash('Please fill out all of the fileds',  category='error')
    elif password != confirm_password:
        flash('Passwords do not match',  category='error')
    elif (len(password) < 6) or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password) or any(char.isspace() for char in password):
        flash('Password must contain at least 6 characters, a letter, a number, and no spaces', category='error')
    else:
        user.password = bcrypt.generate_password_hash(password).decode()
        db.session.commit()
        flash('Your password has been updated!', category = 'success')
        return redirect('/login')

    return redirect(f'/password_reset/{token}')

@app.get('/comment')
def live_comment():
    comments = live_posts.query.order_by(live_posts.date.desc()).limit(15)
    comments_data = []
    for comment in comments:
        # print(comment)
        user = user_repository_singleton.get_user_by_user_id(comment.user_id)
        # print(user)
        if not user:
            abort(400)
        comment_data = {
            'post_id': comment.post_id,
            'content': comment.content,
            'user_id': comment.user_id,
            'username': user.username,
            'date': comment.date.strftime("%Y/%m/%d %H:%M:%S"),
        }
        comments_data.append(comment_data)
    comments_data.reverse()
    return jsonify(comments_data)

@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)
    if not user_repository_singleton.is_logged_in():
        return socketio.emit('redirect', {'url': url_for('login')})
    else:
        user_id = user_repository_singleton.get_user_user_id()
        content = message

        # store comments
        new_comment = live_posts(content=content, user_id=user_id)
        db.session.add(new_comment)
        db.session.commit()

        # emitting new comments:
        socketio.emit('message', {'user_id': user_id, 'content': content,
            'post_id': new_comment.post_id, 'username' : session['user']['username']})

@socketio.on('connect')
def connect():
    global thread
    print('Server connected')
    global current_symbol
    current_symbol = 'SPY'

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
