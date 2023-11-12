from flask_sqlalchemy import SQLAlchemy
# from app import app
from sqlalchemy.sql import func

db = SQLAlchemy()

#users table
class users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(255), nullable = False)

    last_name = db.Column(db.String(255), nullable = False)

    username = db.Column(db.String(255), nullable = False)

    email = db.Column(db.String(255), nullable = False)

    password = db.Column(db.String(255), nullable = False)

    role = db.Column(db.String(255), nullable = True)

    registration_date = db.Column(db.DateTime, nullable=True, default=func.now())

    profile_picture = db.Column(db.String(255), nullable = True)

    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        # self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f'users({self.first_name}, {self.last_name})'


#live posts table
class live_posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable = True, default = func.now())
    
    # Foreign key referencing the users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # Establish the relationship with the User model
    user = db.relationship('users', backref=db.backref('live_posts', lazy=True))

    def __init__(self, post_id:int,content: str, user_id):
        self.post_id = post_id
        self.content = content
        self.user_id = user_id

    def __repr__(self) -> str:
        return f'users({self.post_id}, {self.content}, {self.user_id})'