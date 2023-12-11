# from src.models import *
# from src.repositories.user_repository import user_repository_singleton

# def test_successful_user_registration(test_client):
#     # testing successful registration
#     assert not user_repository_singleton.is_logged_in()
#     response = test_client.post('/register', data = {
#         'first-name' : 'Zaid',
#         'last-name' : 'Jebril',
#         'username' : 'ZaidJ',
#         'email' : 'ZaidJ@yahoo.com',
#         'password' : 'Zaid123'
#     }, follow_redirects=True )

#     assert response.status_code == 302  #redirected after valid registration
#     user = users.query.filter_by(username = 'ZaidJ').first()
#     assert user is not None
#     assert user_repository_singleton.is_logged_in()

# def test_failed_user_registration(test_client):
#     # testing invalid registration : password too short 
#     response = test_client.post('/register', data = {
#         'first-name' : 'Zaid',
#         'last-name' : 'Jebril',
#         'username' : 'ZaidJ',
#         'email' : 'ZaidJ@yahoo.com',
#         'password' : 'Zaid'
#     }, follow_redirects= True )

#     assert response.status_code == 200  #no redirection after failed registration
#     user = users.query.filter_by(username = 'ZaidJ').first()
#     assert user is None
    
# def test_duplicate_user_registration(test_client):
#     # testing duplicate username and email

#     test_client.post('/register', data = {
#         'first-name' : 'Zaid',
#         'last-name' : 'Jebril',
#         'username' : 'ZaidJ',
#         'email' : 'ZaidJ@yahoo.com',
#         'password' : 'Zaid'
#     }, follow_redirects= True )

#     user = users.query.filter_by(username = 'ZaidJ').first()
#     assert user is not None

#     test_client.post('/register', data = {
#         'first-name' : 'John',
#         'last-name' : 'Doe',
#         'username' : 'ZaidJ',
#         'email' : 'John@yahoo.com',
#         'password' : 'John123'
#     }, follow_redirects= True )

#     user = users.query.filter_by(email = 'John@yahoo.com').first()
#     assert user is None

#     test_client.post('/register', data = {
#         'first-name' : 'John',
#         'last-name' : 'Doe',
#         'username' : 'JohnD',
#         'email' : 'ZaidJ@yahoo.com',
#         'password' : 'John123'
#     }, follow_redirects= True )

#     user = users.query.filter_by(username = 'JohnD').first()
#     assert user is None



