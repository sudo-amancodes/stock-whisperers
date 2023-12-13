from app import app
from src.repositories.post_repository import post_repository_singleton
from src.repositories.user_repository import user_repository_singleton
from tests.e2e.utils import reset_db


def test_create_post():
    with app.app_context():
        reset_db()
        user_repository_singleton.add_user(first_name='Jad', last_name='Bizri', username='jadb', email='jadbizri@hotmail.com', password='Jad123', profile_picture='default-profile-pic.jpg')
        user = user_repository_singleton.get_user_by_username('jadb')
        assert user != None
        post_repository_singleton.create_post(title='Test Title', content='Test Content', user_id=user.user_id)
        temp_list = post_repository_singleton.get_all_posts_with_users()
        # Tests to see if class is list
        assert type(temp_list) == type([])
        for post, user in temp_list:
            assert post.title == 'Test Title'
            assert post.content == 'Test Content'
            assert post.user_id == user.user_id
            assert 0<=post.post_id<=100_000
    
def test_create_post_bad_data():
    with app.app_context():
        reset_db()
        user_repository_singleton.add_user(first_name='Jad', last_name='Bizri', username='jadb', email='jadbizri@hotmail.com', password='Jad123', profile_picture='default-profile-pic.jpg')
        user = user_repository_singleton.get_user_by_username('jadb')
        assert user != None
        post_repository_singleton.create_post(title='Fake Title', content='Fake Content', user_id=user.user_id)
        temp_list = post_repository_singleton.get_all_posts_with_users()
        # Tests to see if class is list
        assert type(temp_list) == type([])
        for post, user in temp_list:
            assert post.title != 'Test Title'
            assert post.content != 'Test Content'
            assert post.user_id != 2545
            assert 0<=post.post_id<=100_000

def test_create_post_no_data():
    with app.app_context():
        reset_db()
        temp_list = post_repository_singleton.get_all_posts_with_users()
        # Tests to see if class is list
        assert type(temp_list) == type([])
        assert len(temp_list) == 0
        