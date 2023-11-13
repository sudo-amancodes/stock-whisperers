from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import UserMixin

db = SQLAlchemy()

#users table
class users(db.Model, UserMixin):  
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
    
    def get_id(self):
        return str(self.user_id)


#live posts table
class live_posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable = True, default = func.now())
    
    # Foreign key referencing the users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # Establish the relationship with the User model
    user = db.relationship('users', backref=db.backref('live_posts', lazy=True))

    def __init__(self, content: str, user_id:int):
        self.content = content
        self.user_id = user_id

    def __repr__(self) -> str:
        return f'live_posts({self.post_id}, {self.content}, {self.user_id})'