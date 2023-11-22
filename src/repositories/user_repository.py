from src.models import Post, db, users

class UserRepository:
    # check if a password meets all requirements
    def validate_password(self, password):
        if (len(password) < 6):
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isalpha() for char in password):
            return False
        if any(char.isspace() for char in password):
            return False
        return True

# Singleton to be used in other modules
user_repository_singleton = UserRepository()