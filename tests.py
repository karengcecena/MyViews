from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
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
        """Tests guests / people not logged in can see the login/homepage"""

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

class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # Start each test with a user ID stored in the session.
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = "test_profile"

    def test_friends_search(self):
        """Tests user can see friends search bar"""
        
        result = self.client.get("/search-friends")
        self.assertIn(b'Search for a friend', result.data)

    def test_log_out(self):
        """Tests user can log out"""
       
        result = self.client.get("/logout", follow_redirects=True)
        
        self.assertIn(b'Login', result.data)
        # self.assertNotIn(b'username', session)

    def test_homepage(self):
        """Tests user cannot see the homepage, redirected to profile"""

        result = self.client.get("/")
        self.assertNotIn(b"Login", result.data)
        
class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"username": "test1", "password": "test1"},
                                  follow_redirects=True)
        self.assertIn(b"test1's profile", result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()