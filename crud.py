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

def get_user_by_id(user_id):
    """Gets user by their user_id"""

    return User.query.filter(User.user_id == user_id).first()


def get_media_by_TMDB_id(TMDB_id, media_type):
    """Checks if media is in the db using TMDB_id and media_type"""

    return Media.query.filter(Media.TMDB_id == TMDB_id, Media.media_type == media_type).first()


def add_movie_to_db(movie_info):
    """Adds movie to DB"""

    TMDB_id = movie_info["id"]
    media_type = "movie"
    title = movie_info["original_title"]
    overview = movie_info["overview"]
    release_date = movie_info["release_date"]
    poster_path = movie_info["poster_path"]

    return Media(TMDB_id=TMDB_id, media_type=media_type, title=title, overview=overview, release_date=release_date, poster_path=poster_path )

def add_show_to_db(show_info):
    """Adds show to DB"""

    TMDB_id = show_info["id"]
    media_type = "show"
    title = show_info["name"]
    overview = show_info["overview"]
    release_date = show_info["first_air_date"]
    poster_path = show_info["poster_path"]

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

def get_all_ratings(media_id):
    """Gets all ratings by media_id"""

    return Rating.query.filter(Rating.media_id == media_id).all()

def get_rating_by_id(rating_id, user):
    """Gets users rating by id"""

    return Rating.query.filter(Rating.rating_id == rating_id, Rating.user_id== user.user_id).first()

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

def get_user_movie_watch_history(user):
    """Returns the movie watch history data the user has saved in a dictionary"""
   
    users_movies = []

    for media in user.watched_list:
        if media.media_type == "movie":
            users_movies.append(media)

    movie_watch_history = {}

    for movie in users_movies:
        movie_watch_history[movie.time_watched] = movie_watch_history.get(movie.time_watched, 0) + 1

    return movie_watch_history


def get_user_show_watch_history(user):
    """Returns the show watch history data the user has saved in a dictionary"""

    users_shows = []

    for media in user.watched_list:
        if media.media_type == "show":
            users_shows.append(media)

    show_watch_history = {}

    for show in users_shows:
        show_watch_history[show.time_watched] = show_watch_history.get(show.time_watched, 0) + 1

    return show_watch_history

def get_all_users_not_user(user):
    """gets all users in database that are not the user"""

    return User.query.filter(User.user_id != user.user_id).all()

def create_playlist(playlist_name, user):
    """Creates a playlist for user"""

    return Playlist(name=playlist_name, user_id=user.user_id)

def get_playlist_by_id(playlist_id, user):
    """Gets playlist by that id"""

    return Playlist.query.filter(Playlist.playlist_id == playlist_id, Playlist.user_id== user.user_id).first()

def get_watchlist_media_by_id(media_id, user):
    """Gets a media in watch list and returns it"""

    return WatchedList.query.filter(WatchedList.media_id == media_id, WatchedList.user_id ==user.user_id).first()

def get_tobewatchlist_media_by_id(media_id, user):
    """Gets a media in to be watched list and returns it"""

    return ToBeWatchedList.query.filter(ToBeWatchedList.media_id == media_id, ToBeWatchedList.user_id ==user.user_id).first()

def get_media_by_id(media_id):
    """Returns media where user saved"""

    return Media.query.filter(Media.media_id == media_id).first()