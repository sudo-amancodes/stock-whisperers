from flask_sqlalchemy import SQLAlchemy
from app import app

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