"""Models for movie app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    # middle tables:
    ratings = db.relationship('Rating', back_populates="user")
    playlists = db.relationship('Playlist', back_populates="user")

    # association tables:
    watched_list = db.relationship('Media', secondary="watched_lists", back_populates="watched_users")
    to_be_watched_list = db.relationship('Media', secondary="to_be_watched_lists", back_populates="to_be_watched_users")


    def __repr__(self):
        """Show info about User"""

        return f"<User user_id = {self.user_id} username = {self.username} email = {self.email}>"

class Media(db.Model):
    """Media information"""

    __tablename__ = "medias"

    media_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TMDB_id = db.Column(db.Integer, unique=True, nullable=False)
    media_type = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String(50))
    seasons = db.Column(db.Integer)
    episodes = db.Column(db.Integer)

    # middle table: 
    ratings = db.relationship('Rating', back_populates="media")

    # association tables:
    watched_users = db.relationship('User', secondary="watched_lists", back_populates="watched_list")
    to_be_watched_users = db.relationship('User', secondary="to_be_watched_lists", back_populates="to_be_watched_list")
    playlists = db.relationship('Playlist', secondary="playlists_media", back_populates="medias")
    genres = db.relationship('Genre', secondary="media_genres", back_populates="medias")


    def __repr__(self):
        """Show info about Media"""
        ### possible add ons: TMDB_id: {self.TMDB_id}, genre: {self.genre}

        return f"<Media media_id: {self.media_id} media_type: {self.media_type} media_title: {self.title}>"

class Rating(db.Model):
    

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer, nullable=False)
    review_input = db.Column(db.Text)
    media_id = db.Column(db.Integer, db.ForeignKey("medias.media_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    # connects back to:
    user = db.relationship('User', back_populates="ratings")
    media = db.relationship('Media', back_populates="ratings")


    def __repr__(self):
        """Show info about Rating"""

        return f"<Rating rating_id: {self.rating_id} movie_title: {self.media.title} score: {self.score} media_id: {self.media_id} user_id: {self.user_id}>"

class Playlist(db.Model):
    
    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    # connects back to:
    user = db.relationship('User', back_populates="playlists")

    #association table: 
    medias = db.relationship('Media', secondary="playlists_media", back_populates="playlists")
 

    def __repr__(self):
        """Show info about Playlist"""

        return f"<Playlist playlist_id: {self.playlist_id} name: {self.name} user_id: {self.user_id}>"

class PlaylistMedia(db.Model):
  
    __tablename__ = "playlists_media"

    playlist_media_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"), nullable=False)
    media_id = db.Column(db.Integer, db.ForeignKey("medias.media_id"), nullable=False)

    # this is an association table, so it doesn't directly connect back to any table

    def __repr__(self):
        """Show info about PlaylistMedia"""

        return f"<PlaylistMedia playlist_media_id: {self.playlist_media_id} playlist_id: {self.playlist_id} media_id: {self.media_id}>"

class WatchedList(db.Model):
    
    __tablename__ = "watched_lists"

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    media_id = db.Column(db.Integer, db.ForeignKey("medias.media_id"), nullable=False)

    # this is an association table, so it doesn't directly connect back to any table

    def __repr__(self):
        """Show info about WatchedList"""
        # so that the movie title can be shown in the repr
        media = Media.query.get(self.media_id)

        return f"<WatchedList item_id: {self.item_id} movie_title: {media.title} user_id: {self.user_id} media_id: {self.media_id}>"

class ToBeWatchedList(db.Model):

    __tablename__ = "to_be_watched_lists"

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    media_id = db.Column(db.Integer, db.ForeignKey("medias.media_id"), nullable=False)

    # this is an association table, so it doesn't directly connect back to any table

    def __repr__(self):
        """Show info about ToBeWatchedList"""
        media = Media.query.get(self.media_id)

        return f"<ToBeWatchedList item_id: {self.item_id} movie_title: {media.title} user_id: {self.user_id} media_id: {self.media_id}>"

class Genre(db.Model):

    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TMDB_genre_id = db.Column(db.Integer, unique=True, nullable=False)
    genre_name = db.Column(db.String(50), unique=True, nullable=False)

    #association table: 
    medias = db.relationship('Media', secondary="media_genres", back_populates="genres")

    def __repr__(self):
        """Show info about Genre"""

        return f"<Genre genre_id: {self.genre_id} genre_name = {self.genre_name}>"

class MediaGenre(db.Model):

    __tablename__ = "media_genres"

    media_genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.genre_id"), nullable=False)
    media_id = db.Column(db.Integer, db.ForeignKey("medias.media_id"), nullable=False)

    # this is an association table, so it doesn't directly connect back to any table

    def __repr__(self):
        """Show info about MediaGenre"""
        media = Media.query.get(self.media_id)

        return f"<MediaGenre media_genre_id: {self.media_genre_id} movie_title: {media.title}>"


def connect_to_db(flask_app, db_uri="postgresql:///project_db", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Successfully connected to DB")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    db.create_all()