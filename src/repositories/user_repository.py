from datetime import datetime, timedelta
from src.models import Post, db, friendships, users, live_posts, likes, comment_likes, Comment
from flask import abort, flash, session
from sqlalchemy import or_

class UserRepository:
    # check if a password meets all requirements
    def validate_input(self, first_name, last_name, username, password):
        if len(first_name) <= 1:
            flash('First name must be greater than 1 character', category='error')
            return False
        elif len(last_name) <= 1:
            flash('Last name must be greater than 1 character', category='error')
            return False
        elif len(username) < 4:
            flash('Username name must be at least 4 characters', category='error')
            return False
        elif (len(password) < 6) or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password) or any(char.isspace() for char in password):
            flash('Password must contain at least 6 characters, a letter, a number, and no spaces', category='error')
            return False
        return True
    
    def add_user(self, first_name, last_name, username, email, password, profile_picture):
        temp_user = users(first_name, last_name, username, email, password, profile_picture)
        db.session.add(temp_user)
        db.session.commit()
        
    def remove_user(self, username):
        user = users.query.filter_by(username = username).first()
        if not user:
            abort(400)
        existing_friendship = friendships.query.filter(or_(friendships.user1_id == user.user_id, friendships.user2_id == user.user_id)).first()
        if existing_friendship:
            db.session.delete(existing_friendship)
            db.session.commit()
        user_live_posts = live_posts.query.filter_by(user_id = user.user_id).all()
        if user_live_posts:
            for live_post in user_live_posts:
                db.session.delete(live_post)
                db.session.commit()
        posts = Post.query.filter_by(user_id = user.user_id).all()
        if posts:
            for post in posts:
                db.session.delete(post)
                db.session.commit()
        comments = Comment.query.filter_by(user_id = user.user_id).all()
        if comments:
            for comment in comments:
                db.session.delete(comment)
                db.session.commit()
        if user:
            db.session.delete(user)
            db.session.commit()


    def login_user(self, user):
        session['user'] = {
            'username' : user.username,
            'user_id' : user.user_id,
            'email' : user.email,
            'first_name' : user.first_name,
            'last_name' : user.last_name
        }
        # user = users.query.filter_by(username=username).first()
        if user:
            user.last_login = datetime.utcnow()

    def logout_user(self):
        del session['user']

    def is_logged_in(self):
        return 'user' in session
    
    def get_user_by_user_id(self, user_id):
        return users.query.filter_by(user_id=user_id).first()
    
    def get_user_by_username(self, username):
        return users.query.filter_by(username=username).first()
    
    def get_user_username(self):
        return session['user']['username']
    
    def get_user_user_id(self):
        return session['user']['user_id']
    
    def get_user_email(self):
        return session['user']['email']
    
    def get_user_first_name(self):
        return session['user']['first_name']
    
    def get_user_last_name(self):
        return session['user']['last_name']
    
    # follow a user
    def follow_user(self, user_id, user_to_follow_id):
        friendship = friendships.query.filter_by(user1_id = user_id, user2_id = user_to_follow_id).first()
        if friendship:
            db.session.delete(friendship)
            db.session.commit()
        else:
            friendship = friendships(user_id,user_to_follow_id)
            db.session.add(friendship)
            db.session.commit()

# Singleton to be used in other modules
user_repository_singleton = UserRepository()