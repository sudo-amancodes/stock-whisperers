from flask import g, session
from src.models import *

def reset_db():
    users.query.delete()
    friendships.query.delete()
    live_posts.query.delete()
    Comment.query.delete()
    Post.query.delete() 
    db.session.commit()
