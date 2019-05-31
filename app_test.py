
import app
import unittest 

class FlaskBookshelfTests(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def tearDown(self):
        pass 

    def test_books_get(self):
        result = self.app.get('/books')
        self.assertEqual(result.status_code, 200) 

    def test_books_post(self):
        result = self.app.post('/books')
        self.assertEqual(result.status_code, 200) 

    def test_book_get(self):
        result = self.app.get('/book')
        self.assertEqual(result.status_code, 200) 
