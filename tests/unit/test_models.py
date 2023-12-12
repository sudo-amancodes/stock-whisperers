from src.models import *

def test_user_model():
    temp_user = users('Zaid', 'Jebril', "Zaid_J", 'Zaid@yahoo.com', 'Zaid123', 'default-profile-pic.jpg')

    assert temp_user.first_name == 'Zaid'
    assert temp_user.last_name == 'Jebril'
    assert temp_user.username == 'Zaid_J'
    assert temp_user.email == 'Zaid@yahoo.com'
    assert temp_user.password == 'Zaid123'
    assert temp_user.profile_picture == 'default-profile-pic.jpg'

    # Checking that changing info works
    temp_user.first_name  = 'John'
    temp_user.last_name  = 'Jack'
    temp_user.username  = 'JohnJ'
    temp_user.email  = 'John@yahoo.com'
    temp_user.password  = 'John123'
    temp_user.profile_picture = 'new-profile-pic.jpg'

    assert temp_user.first_name == 'John'
    assert temp_user.last_name == 'Jack'
    assert temp_user.username == 'JohnJ'
    assert temp_user.email == 'John@yahoo.com'
    assert temp_user.password == 'John123'
    assert temp_user.profile_picture == 'new-profile-pic.jpg'

def test_friendships_model():
    user1 = users('Zaid', 'Jebril', "Zaid_J", 'Zaid@yahoo.com', 'Zaid123', 'default-profile-pic.jpg')
    user2 = users('John', 'Doe', "John_D", 'John@yahoo.com', 'John123', 'default-profile-pic.jpg')

    temp_freindship = friendships(user1.username, user2.username)
    
    assert temp_freindship.user1_username == 'Zaid_J'
    assert temp_freindship.user2_username == 'John_D'