from unittest import TestCase
from server import app
from model import connect_to_db, db
from flask import session

class FlaskTestsBasic(TestCase):
    """Flask Tests"""

    def setUp(self):
        """Stuff to do before every test."""
        
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests 
        app.config['TESTING'] = True

    def test_homepage(self):
        """Tests guests can see the homepage"""

        result = self.client.get("/")
        self.assertIn(b"Login", result.data)

    def test_friends_search(self):
        """Tests guests cannot see friends search bar"""
        
        result = self.client.get("/search-friends")
        self.assertIn(b'redirected automatically to the target URL: <a href="/">/</a>', result.data)

    def test_your_recommended(self):
        """Tests guests cannot see recommended media page"""
        
        result = self.client.get("/recommended")
        self.assertIn(b'redirected automatically to the target URL: <a href="/">/</a>', result.data)

    def test_user_profile(self):
        """Test guests cannot see a profile page"""
        
        result = self.client.get("/user-profile")
        self.assertIn(b'redirected automatically to the target URL: <a href="/">/</a>', result.data)

    def test_log_out(self):
        """Tests guests cannot log out if not logged in"""
       
        result = self.client.get("/logout")
        self.assertIn(b'redirected automatically to the target URL: <a href="/">/</a>', result.data)

    def test_search(self):
        """Test guests can use the search bar for media"""
        # can I test search if uses react????
        # result = self.client.get("/media-search-results-react")
        # self.assertIn(b"Search a movie or tv show", result.data)
    
    def test_media_info(self):
        """Tests guests can see media info for media search"""

        # result = self.client.get("/media-info/movie/361743")
        # self.assertIn(b"Top Gun: Maverick", result.data)

    def test_media_info_rating(self):
        """Tests guests cannot see rating in media info for media search"""
        
        # result = self.client.get("/media-info/movie/361743")
        # self.assertNotIn(b"Rating", result.data)

if __name__ == "__main__":
    # how do I get this page to run tests?
    import unittest

    unittest.main()