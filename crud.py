"""CRUD operations."""

from model import db, User, Media, Rating, Playlist, PlaylistMedia, WatchedList, ToBeWatchedList, connect_to_db


def create_user(username, email, password):
    """Creates a user"""
    
    user = User(username=username, email=email, password=password)

    return user

def get_user_by_email(email):
    """Gets user by their email"""

    return User.query.filter(User.email == email).first()

def get_user_by_username(username):
    """Gets user by their username"""

    return User.query.filter(User.username == username).first()
