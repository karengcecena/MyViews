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


def get_media_by_TMDB_id(TMDB_id):
    """Checks if media is in the db using TMDB_id"""

    return Media.query.filter(Media.TMDB_id == TMDB_id).first()


def add_movie_to_db(movie_info):
    """Adds movie to db"""

    TMDB_id = movie_info["id"]
    media_type = "movie"
    title = movie_info["original_title"]
    overview = movie_info["overview"]
    release_date = movie_info["release_date"]
    poster_path = movie_info["poster_path"]
     # genre = 

    return Media(TMDB_id=TMDB_id, media_type=media_type, title=title, overview=overview, release_date=release_date, poster_path=poster_path )


def add_rating_to_db(score, user_id, media_id):
    """Adds the rating to the DB"""

    rating = Rating(score=score, user_id=user_id, media_id=media_id)

    return rating


def user_rated(media, user):
    """Checks if user has rated this media previously"""

    return Rating.query.filter(Rating.media_id == media.media_id, Rating.user_id == user.user_id).first()


