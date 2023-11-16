from src.models import users, db
from app import app

class UserRepository:

    def get_all_users(self):
        # TODO get all users from the DB
        return users.query.all()
    
    def get_user_by_id(self, user_id):
        # TODO get a single user from the DB using the ID
        return users.query.get(user_id)
    
    
