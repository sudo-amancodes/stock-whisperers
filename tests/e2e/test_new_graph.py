import unittest
from app import app
from tests.e2e.utils import reset_db
from src.models import * 

class LiveCommentE2ETest(unittest.TestCase):

    def setUp(self): 
        app.testing = True
        self.client = app.test_client()

    def test_graph(self):
        self.client.post('/data', data={
            'Stock' : 'AAPL'
        }) 

        response = self.client.get('/data')
        assert response 