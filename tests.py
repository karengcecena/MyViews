from unittest import TestCase
from server import app
from model import connect_to_db, db
from flask import session

class FlaskTestsLoggedOut(TestCase):
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
       
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b'Login', result.data)
        

if __name__ == "__main__":
    # how do I get this page to run tests?
    import unittest

    unittest.main()