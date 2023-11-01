from flask import Flask, abort, redirect, render_template, request

app = Flask(__name__)
app.debug = True


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
    pass

#TODO: Create a post request for the user login page.
@app.post('/login')
def verify_login():
    pass

#TODO: Create a get request for the registration page.
@app.get('/register')
def register():
    pass

#TODO: Create a post request for the registration page.
@app.post('/register')
def create_user():
    pass

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
