from src.models import *
from src.repositories.user_repository import user_repository_singleton
from app import bcrypt
from tests.e2e.utils import reset_db

def test_successful_login_using_username(test_client):
    reset_db()
    user_repository_singleton.add_user('Zaid', 'Jebril', 'ZaidJebril', 'zaid@yahoo.com', bcrypt.generate_password_hash('Zaid123').decode(), 'default-profile-pic.jpg')

    response = test_client.post('/login', data = {
        'username' : 'ZaidJebril',
        'password' : 'Zaid123'
    }, follow_redirects = True)

    response_data = response.data.decode('utf-8')
    # Testing that user was redirected after successful login
    assert response.status_code == 200

    # Testing that user is logged in and info is stored in session
    with test_client.session_transaction() as sess:
        assert 'user' in sess
        user_session_data = sess['user']
        # resseting sess for next test
        del sess['user']

        assert user_session_data['username'] == 'ZaidJebril'
        assert user_session_data['email'] == 'zaid@yahoo.com'
        assert user_session_data['first_name'] == 'Zaid'
        assert user_session_data['last_name'] == 'Jebril'

    assert 'Successfully logged in, Zaid!' in response_data

def test_successful_login_using_email(test_client):
    reset_db()
    # clear_session()
    user_repository_singleton.add_user('Zaid', 'Jebril', 'ZaidJebril', 'zaid@yahoo.com', bcrypt.generate_password_hash('Zaid123').decode(), 'default-profile-pic.jpg')

    response = test_client.post('/login', data = {
        'username' : 'zaid@yahoo.com',
        'password' : 'Zaid123'
    }, follow_redirects= True)

    response_data = response.data.decode('utf-8')

    # Testing that user was redirected after successful login
    assert response.status_code == 200

    # Testing that user is logged in and info is stored in session
    with test_client.session_transaction() as sess:
        assert 'user' in sess
        user_session_data = sess['user']
        # resseting sess for next test
        del sess['user']

        assert user_session_data['username'] == 'ZaidJebril'
        assert user_session_data['email'] == 'zaid@yahoo.com'
        assert user_session_data['first_name'] == 'Zaid'
        assert user_session_data['last_name'] == 'Jebril'

    assert 'Successfully logged in, Zaid!' in response_data

def test_invalid_username_login(test_client):
    reset_db()
    # clear_session()
    user_repository_singleton.add_user('Zaid', 'Jebril', 'ZaidJ', 'zaid@yahoo.com', bcrypt.generate_password_hash('Zaid123').decode(), 'default-profile-pic.jpg')

    response = test_client.post('/login', data = {
        'username' : 'Zaid_JJ',
        'password' : 'Zaid123'
    }, follow_redirects= True)

    response_data = response.data.decode('utf-8')

    assert response.status_code == 200

    # Testing that user is not stored in sess after invalid login
    with test_client.session_transaction() as sess:
        assert 'user' not in sess

    assert 'Username does not exist' in response_data

def test_invalid_password_login(test_client):
    reset_db()
    # clear_session()
    user_repository_singleton.add_user('Zaid', 'Jebril', 'ZaidJ', 'zaid@yahoo.com', bcrypt.generate_password_hash('Zaid123').decode(), 'default-profile-pic.jpg')

    response = test_client.post('/login', data = {
        'username' : 'ZaidJ',
        'password' : 'Zaid1234'
    }, follow_redirects= True)

    response_data = response.data.decode('utf-8')

    assert response.status_code == 200

    # Testing that user is not stored in sess after invalid login
    with test_client.session_transaction() as sess:
        assert 'user' not in sess

    assert 'Incorrect username or password' in response_data

def test_user_logout(test_client):
    reset_db()

    # setting session to test if user is deleted later
    with test_client.session_transaction() as sess:
        sess['user'] = 'Zaid'

    test_client.post('/logout', data = {}, follow_redirects = True)

    with test_client.session_transaction() as sess:
        assert 'user' not in sess


