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

    # don't need a tear down?

if __name__ == "__main__":
    # how do I get this page to run tests?
    import unittest

    unittest.main()