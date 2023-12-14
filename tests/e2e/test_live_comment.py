# Import necessary libraries and modules
import unittest
from app import app
from tests.e2e.utils import reset_db
from src.models import * 


class LiveCommentE2ETest(unittest.TestCase):

    def setUp(self): 
        app.testing = True
        self.client = app.test_client()

    def test_comment(self):
        self.client.post('/add_comment', data={
            'post_id': '123',
            'user_id': 'user1',
            'comment_text': 'E2E test comment'
        })
        # check if new comments exists
        response = self.client.get('/get_comments?post_id=123')
        self.assertIn("Test comment", response.data.decode())


