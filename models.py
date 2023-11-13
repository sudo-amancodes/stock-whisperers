from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#users table
class users():
    user_id = db.Column(db.Integer, primary_key = True)
    # first_name VARCHAR(255),
    first_name = db.Column(db.String(255), nullable = False)
    # last_name VARCHAR(255),
    last_name = db.Column(db.String(255), nullable = False)
    # username VARCHAR(255) UNIQUE,
    username = db.Column(db.String(255), nullable = False)
    # email VARCHAR(255) UNIQUE,
    email = db.Column(db.String(255), nullable = False)
    # password VARCHAR(255),
    password = db.Column(db.String(255), nullable = False)
    # role VARCHAR(50),
    # role = db.Column(db.String(255), nullable = False)
    # registration_date TIMESTAMP,
    # profile_picture VARCHAR(255)
    profile_picture = db.Column(db.String(255), nullable = True)

    def __init__(self, user_id:int, first_name: str, last_name: str, username: str, email: str, password: str):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f'users({self.first_name}, {self.last_name})'


#live posts table
class Live_Posts():
    pass


#post
class Post(db.model):
    # PRIMARY KEY post_id SERIAL,
    post_id = db.Column(db.Integer, primary_key = True)

    # title VARCHAR(255) NOT NULL,
    title = db.Column(db.String(255), nullable = False)

    # content TEXT,
    content = db.Column(db.Text, nullable = True)

    # date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_posted = db.Column(db.DateTime, nullable = False)

    # likes INT NOT NULL DEFAULT 0,
    likes = db.Column(db.Integer, nullable = True, default = 0)

    # image BLOB,
    image = db.Column(db.LargeBinary, nullable = True)

    # user_id INT,
    # FOREIGN KEY (user_id) references users(user_id)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)

    # each user's posts
    posts = db.relationship('users', backref='posts')

    def __init__(self, post_id: int, user_id: int, title: str, content: str, date_posted: str, likes: int):
        self.post_id = post_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.date_posted = date_posted
        self.likes = likes

    def __repr__(self) -> str:
        return f'Post #{self.post_id} by {self.user_id})'

#post comments
class Comment(db.model):
    # PRIMARY KEY comment_id SERIAL,
    comment_id = db.Column(db.Integer, primary_key = True)

    # content TEXT,
    content = db.Column(db.Text, nullable = True)

    # date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_posted = db.Column(db.DateTime, nullable = False)

    # likes INT NOT NULL DEFAULT 0,
    likes = db.Column(db.Integer, nullable = True, default = 0)

    # user_id INT,
    # FOREIGN KEY (user_id) references users(user_id)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)

    # post_id INT,
    # FOREIGN KEY (post_id) references posts(post_id)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable = False)

    # each user's comments
    comments = db.relationship('users', backref='comments')

    # each post's comments
    comments = db.relationship('posts', backref='comments')

    def __init__(self, comment_id: int, user_id: int, post_id: int, content: str, date_posted: str, likes: int):
        self.comment_id = comment_id
        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.date_posted = date_posted
        self.likes = likes

    def __repr__(self) -> str:
        return f'{self.content}'