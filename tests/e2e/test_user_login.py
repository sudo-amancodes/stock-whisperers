from src.models import *
from src.repositories.user_repository import user_repository_singleton
from app import bcrypt
from utils import reset_db

def test_successful_login_using_username(test_client):
    user_repository_singleton.add_user('Zaid', 'Jebril', 'ZaidJebril7', 'zaidJ7@yahoo.com', bcrypt.generate_password_hash('Zaid123').decode(), 'default-profile-pic.jpg')

    response = test_client.post('/login', data = {
        'username' : 'ZaidJebril7',
        'password' : 'Zaid123'
    }, follow_redirects = True)

    # print(response.get_data(as_text=True))

    assert response.status_code == 302

    response = test_client.get(response.location)

    assert 'user' in test_client.session
    assert test_client.session['user']['username'] == 'ZaidJebril4'
    assert test_client.session['user']['email'] == 'zaidJ4@yahoo.com'
    assert test_client.session['user']['first_name'] == 'Zaid'
    assert test_client.session['user']['last_name'] == 'Jebril'

def test_successful_login_using_email(test_client):
    user_repository_singleton.add_user('Zaid', 'Jebril', 'ZaidJ', 'zaid@yahoo.com', 'Zaid123', 'default-profile-pic.jpg')

    response = test_client.post('/login', data = {
        'username' : 'zaid@yahoo.com',
        'password' : 'Zaid123'
    }, follow_redirects= True)

    assert response.status_code == 302
    response = test_client.get(response.location)

    assert 'user' in test_client.session
    assert test_client.session['user']['username'] == 'ZaidJebril4'
    assert test_client.session['user']['email'] == 'zaidJ4@yahoo.com'
    assert test_client.session['user']['first_name'] == 'Zaid'
    assert test_client.session['user']['last_name'] == 'Jebril'

def test_invalid_username_login(test_client):
    user_repository_singleton.add_user('Zaid', 'Jebril', 'ZaidJ', 'zaid@yahoo.com', 'Zaid123', 'default-profile-pic.jpg')

    response = test_client.post('/login', data = {
        'username' : 'Zaid_JJ',
        'password' : 'Zaid123'
    }, follow_redirects= True)

    assert response.status_code == 200
    response = test_client.get(response.location)
    assert 'user' not in test_client.session

def test_invalid_password_login(test_client):
    user_repository_singleton.add_user('Zaid', 'Jebril', 'ZaidJ', 'zaid@yahoo.com', 'Zaid123', 'default-profile-pic.jpg')

    response = test_client.post('/login', data = {
        'username' : 'ZaidJ',
        'password' : 'Zaid1234'
    }, follow_redirects= True)

    assert response.status_code == 200
    response = test_client.get(response.location)
    assert 'user' not in test_client.session
