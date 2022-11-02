"""CRUD operations."""

from model import db, User, Media, Rating, Playlist, PlaylistMedia, WatchedList, ToBeWatchedList, Genre, MediaGenre, connect_to_db


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
    """Adds movie to DB"""

    TMDB_id = movie_info["id"]
    media_type = "movie"
    title = movie_info["original_title"]
    overview = movie_info["overview"]
    release_date = movie_info["release_date"]
    poster_path = movie_info["poster_path"]

    return Media(TMDB_id=TMDB_id, media_type=media_type, title=title, overview=overview, release_date=release_date, poster_path=poster_path )

def check_if_genre_in_db(genre):
    """Checks if the genre mentioned is in DB"""

    return Genre.query.filter(Genre.TMDB_genre_id == genre["id"]).first()

def add_genre_to_db(genre):
    """Adds genre to DB"""
    TMDB_genre_id = genre["id"]
    genre_name = genre["name"]

    return Genre(TMDB_genre_id=TMDB_genre_id, genre_name=genre_name)
    
def add_rating_to_db(score, user_id, media_id, comment=None):
    """Adds the rating to the DB"""

    rating = Rating(score=score, user_id=user_id, media_id=media_id, review_input=comment)

    return rating


def user_rated(media, user):
    """Checks if user has rated this media previously"""

    return Rating.query.filter(Rating.media_id == media.media_id, Rating.user_id == user.user_id).first()


def user_sorted_Watched(media, user):
    """Checks if user has sorted movie in folder previously"""

    return WatchedList.query.filter(WatchedList.media_id == media.media_id, WatchedList.user_id == user.user_id).first()


def user_sorted_ToBeWatched(media, user):
    """Checks if user has sorted movie in folder previously"""

    return ToBeWatchedList.query.filter(ToBeWatchedList.media_id == media.media_id, ToBeWatchedList.user_id == user.user_id).first()


def add_to_WatchedList(media, user):
    """Adds media to users watched list"""

    movie_folder = WatchedList(user_id=user.user_id, media_id=media.media_id)

    return movie_folder

def add_to_ToBeWatchedList(media, user):
    """Adds media to users to be watched list"""

    movie_folder = ToBeWatchedList(user_id=user.user_id, media_id=media.media_id)

    return movie_folder

def get_user_genres(user):
    """Returns the genres the user has saved in a dictionary"""

    media_genres = {}
    
    user_watched_list = user.watched_list

    for media in user_watched_list:
        for genre in media.genres:
            media_genres[genre] = media_genres.get(genre, 0) + 1

    # to sort the dictionary values so the pie chart goes from smallest to largest, 
    # adapted from https://www.tutorialsteacher.com/articles/sort-dict-by-value-in-python
    media_genres_list = sorted(media_genres.items(), key=lambda x:x[1], reverse=True)
    sort_media_genres_dict = dict(media_genres_list)

    return sort_media_genres_dict

def create_playlist(playlist_name, user):
    """Creates a playlist for user"""

    return Playlist(name=playlist_name, user_id=user.user_id)