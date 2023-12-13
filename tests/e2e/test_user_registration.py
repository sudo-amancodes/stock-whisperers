from flask import get_flashed_messages
from app import bcrypt, app
from src.models import *
from src.repositories.user_repository import user_repository_singleton
from tests.e2e.utils import reset_db

def test_successful_user_registration(test_client):
    reset_db()

    # testing that user is not logged in when registering
    with test_client.session_transaction() as sess:
        assert 'user' not in sess

    response = test_client.post('/register', data = {
        'first-name' : 'Zaid',
        'last-name' : 'Jebril',
        'username' : 'ZaidJ',
        'email' : 'Zaid@yahoo.com',
        'password' : 'Zaid123'
    }, follow_redirects=True )

    response_data = response.data.decode('utf-8')
    # Since sign up requires code validation sent through email, 
    # testing that user was redirecting and then adding temp user for testing purposes
    assert response.status_code == 200
    user_repository_singleton.add_user('Zaid', 'Jebril', 'ZaidJ', 'zaid@yahoo.com', bcrypt.generate_password_hash('Zaid123').decode(), 'default-profile-pic.jpg')

    # assert user was added and is logged in after successful registration
    user = users.query.filter_by(username = 'ZaidJ').first()
    assert user is not None

    assert 'success', 'Successfully created an account. Welcome, Zaid!' in response_data

def test_failed_user_registration(test_client):
    reset_db()
    # testing invalid registration : password too short 
    response = test_client.post('/register', data = {
        'first-name' : 'Zaid',
        'last-name' : 'Jebril',
        'username' : 'ZaidJ',
        'email' : 'ZaidJ@yahoo.com',
        'password' : 'Zaid'
    }, follow_redirects= True )

    response_data = response.data.decode('utf-8')

    assert response.status_code == 200 
    user = users.query.filter_by(username = 'ZaidJ').first()
    assert user is None
    with test_client.session_transaction() as sess:
        assert 'user' not in sess
    assert 'Password must contain at least 6 characters, a letter, a number, and no spaces' in response_data
    
def test_duplicate_user_registration(test_client):
    reset_db()
    user_repository_singleton.add_user('Zaid', 'Jebril', 'ZaidJ', 'zaid@yahoo.com', bcrypt.generate_password_hash('Zaid123').decode(), 'default-profile-pic.jpg')

    response = test_client.post('/register', data = {
        'first-name' : 'Zaid',
        'last-name' : 'Jebril',
        'username' : 'ZaidJ2',
        'email' : 'Zaid@yahoo.com',
        'password' : 'Zaid123'
    }, follow_redirects= True )

    response_data = response.data.decode('utf-8')

    assert response.status_code == 200 
    with test_client.session_transaction() as sess:
        assert 'user' not in sess
    assert 'email already exists' in response_data
    



