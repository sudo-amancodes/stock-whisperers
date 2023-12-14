from src.models import * 
import unittest
from app import app
from tests.e2e.utils import reset_db


class TestLiveCommentFeature(unittest.TestCase):

    def setUp(self):
      
        app.testing = True
        self.client = app.test_client()

    def test_add_comment(self):
        reset_db()
        response = self.client.post('/add_comment', data={
            'post_id': '123',
            'user_id': 'user1',
            'comment_text': 'Test comment'
        })
        self.assertEqual(response.status_code, 200)  
         
    # testing get comments
    def test_get_comments(self):
        response = self.client.get('/get_comments?post_id=123')
        self.assertIn("Test comment", response.data.decode()) 

    # testing adding an empty comment. 
    def test_add_empty_comment(self):
       
        response = self.client.post('/add_comment', data={
            'post_id': '123',
            'user_id': 'user1',
            'comment_text': ''
        })
        self.assertNotEqual(response.status_code, 200)  

 





