from app import app
from src.repositories.post_repository import post_repository_singleton
from src.repositories.user_repository import user_repository_singleton
from tests.e2e.utils import reset_db


def test_delete_post():
    with app.app_context():
        reset_db()
        user_repository_singleton.add_user(first_name='Jad', last_name='Bizri', username='jadb', email='jadbizri@hotmail.com', password='Jad123', profile_picture='default-profile-pic.jpg')
        user = user_repository_singleton.get_user_by_username('jadb')
        assert user is not None
        post = post_repository_singleton.create_post(title='Test Title', content='Test Content', user_id=user.user_id)
        assert post is not None
        result =  post_repository_singleton.delete_post(post.post_id)
        assert result is True

def test_delete_non_existing_post():
    with app.app_context():
        reset_db()
        result =  post_repository_singleton.delete_post(1)
        assert result is False