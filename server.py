"""Server for movie app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify, url_for)
from model import connect_to_db, db, login_manager, OAuth, User
import crud
import os
import requests
from jinja2 import StrictUndefined

# import for hashing passwords
from passlib.hash import argon2

#### imports to implement github oauth: 
from flask_dance.contrib.github import github, make_github_blueprint
from flask_login import current_user
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound

from datetime import date

app = Flask(__name__)
app.secret_key = "forsession"
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ['TMDB_KEY']

#################################################################################################
# OAuth for Github Implemented Using https://testdriven.io/blog/flask-social-auth/#oauth

github_blueprint = make_github_blueprint(
    client_id = os.environ['GITHUB_ID'],
    client_secret = os.environ['GITHUB_SECRET'],
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
)

app.register_blueprint(github_blueprint, url_prefix="/login")

@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    info = github.get("/user")
    if info.ok:
        account_info = info.json()
        username = account_info["login"]

        query = User.query.filter_by(username=username)
        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        
        session["username"] = username
        return redirect("/user-profile")

@app.route("/github")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    res = github.get("/user")
    username = res.json()["login"]

    session['username'] = username
    return redirect("/user-profile")

##################### End of GitHub OAuth Implementation ###########################################

@app.route("/")
def homepage():
    """Displays homepage"""

    if "username" in session:
        return redirect("/user-profile")

    return render_template("homepage.html")

@app.route("/register-user", methods=["POST"])
def register_user():
    """Gets info input in create user page and registers user"""
    
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    # to hash the password 
    password_hashed = argon2.hash(password)

    if crud.get_user_by_username(username):
        flash("Sorry, that username is already taken.")

    elif crud.get_user_by_email(email):
        flash("Sorry, that email is already taken")

    else:
        user = crud.create_user(username=username, email=email, password=password_hashed)
        db.session.add(user)
        db.session.commit()
        session["username"] = username
        # flash ("Succesfully created user")
        return redirect("/user-profile")

    return redirect ("/")
   

@app.route("/login", methods=["POST"])
def login_user():
    """Logs in the user"""

    username = request.form.get("username")
    password = request.form.get("password")
    user = crud.get_user_by_username(username)

    if user:
       # see if they are a github user
        if not user.password: 
            flash("Sorry, that password was incorrect. Try logging in with GitHub")
        # if not github user, verify hashed password input is equal to one in DB
        elif argon2.verify(password, user.password):
            session["username"] = user.username
            # flash("You have successfully logged in")
            # return redirect ("/user-profile")
            return redirect ("/media-search-results-react")
        
        else:
            flash("Your password was incorrect. Please try again.")

    else:
        flash("Sorry, a user with that email doesn't exist")

    return redirect("/")

@app.route("/logout")
def logout_user():
    """Logs out the user by clearing the session."""
    
    if "username" in session: 
        session.clear()
        # flash("You've been logged out")
    else:
        # flash("Sorry, please log in:")
        return redirect("/")
    
    return redirect("/")

@app.route("/user-profile")
def display_user_profile():
    """Displays the user profile page"""
    
    if "username" in session: 
        user_username= session["username"]
        user = crud.get_user_by_username(user_username)
        return render_template("user_profile.html", user=user)

    else:
        # flash("Sorry, please log in:")
        return redirect("/")

@app.route("/search-friends")
def display_search():
    """Displays search bar to search for friends"""

    if "username" in session: 
        return render_template("/search_friends.html")

    else:
        # flash("Sorry, please log in:")
        return redirect("/")

@app.route("/friend-search-results", methods=["POST"])
def show_friend_search_results():
    """Shows friend profile as search result it username exists"""
    
    search_text = request.form.get("friend_username")
    user_username = session["username"]

    user = crud.get_user_by_username(user_username)
    user2 = crud.get_user_by_username(search_text)

    if user2: 
        return render_template("/search_friend_result.html", user2=user2, user=user, user2_user_id= user2.user_id)

    else: 
        flash(f"Sorry, no user exists with the username '{search_text}'.")
        return redirect("/search-friends")

@app.route("/friend/follow-status.js", methods=["POST"])
def follow_or_unfollow_friends():
    """Allows user to unfollow or follow a friend"""

    user_username = session["username"]
    user = crud.get_user_by_username(user_username)

    user2_user_id = request.json.get("user2ID")
    user2 = crud.get_user_by_id(user2_user_id)

    action = (request.json.get("action")).lower()

    if action == "follow": 
        user.following.append(user2)
        db.session.commit()

    elif action == "unfollow": 
        user.following.remove(user2)
        db.session.commit()

    return jsonify({"success": "user followed/unfollowed"})


@app.route('/display-friend/<friend_username>')
def display_friend_by_username(friend_username):
    """Displays friend profile when user clicks on their name in user profile"""

    user_username = session["username"]
    user = crud.get_user_by_username(user_username)

    user2 = crud.get_user_by_username(friend_username)

    # if user2: 
    return render_template("/search_friend_result.html", user2=user2, user=user, user2_user_id= user2.user_id)

################################################# REACT #################################################
@app.route("/media-search-results-react.json",  methods=["POST"])
def get_search_results_react_json():
    """Return a JSON response with all media from search bar query"""

    # REACT getting version
    search_text = request.get_json().get("search")
    media_type = request.get_json().get("mediaType")
    
    url = f"https://api.themoviedb.org/3/search/{media_type}"
    
    payload = {"api_key": API_KEY} 

    # add media title to payload
    if search_text:
        payload["query"]=search_text

    res = requests.get(url, params=payload)
    data = res.json()

    results = data['results']

    return jsonify({"media": results, "search_text": search_text, "media_type": media_type})

@app.route("/media-search-results-react")
def show_react_search_results():
    """Show all media using REACT"""

    return render_template("all_media_react.html")

##############################################End REACT #################################################

@app.route("/media-info/<media_type>/<TMDB_id>")
def show_media(media_type, TMDB_id):
    """Shows specific media information for selected media"""

    #get media information
    url = f"https://api.themoviedb.org/3/{media_type}/{TMDB_id}"

    payload = {"api_key": API_KEY} 

    res = requests.get(url, params=payload)
    data = res.json()
    
    # filter for that movies ratings in db to display on media page
    if crud.get_media_by_TMDB_id(TMDB_id, media_type):
        media = crud.get_media_by_TMDB_id(TMDB_id, media_type)
        media_id = media.media_id
        all_ratings = crud.get_all_ratings(media_id)

    else: 
        all_ratings = False

    # check if user is logged in in order to display playlists correctly 
    if "username" in session:
        user = crud.get_user_by_username(session["username"])
        return render_template("media_information.html", data=data, TMDB_id=TMDB_id, user=user, media_type=media_type, all_ratings=all_ratings)

    else:
        return render_template("media_information.html", data=data, TMDB_id=TMDB_id, user=False, media_type=media_type, all_ratings=all_ratings)
 
@app.route("/<media_type>/<TMDB_id>/add-to-playlist", methods=["POST"])
def add_media_to_playlist(media_type, TMDB_id):
    """Adds media to selected playlist"""
    media = crud.get_media_by_TMDB_id(TMDB_id, media_type)
    playlist_id = request.form.get("playlist")
    user_username = session["username"]
    user = crud.get_user_by_username(user_username)

    # add media to database if not in there already
    if not media:
        #get media information
        url = f"https://api.themoviedb.org/3/{media_type}/{TMDB_id}"
        payload = {"api_key": API_KEY} 

        res = requests.get(url, params=payload)
        data = res.json()

        # add media to db
        if media_type == "movie":
            media = crud.add_movie_to_db(data)
        
        elif media_type == "tv":
            media = crud.add_show_to_db(data)

        db.session.add(media)
        db.session.commit()

        ### ADDING MEDIA GENRE INFORMATION ###
        # add genres to media that do not exist:
        if data["genres"]: 
            genres = data["genres"]
            for genre in genres:
                # check if genre in genres:
                if crud.check_if_genre_in_db(genre):
                    # if yes: 
                    genre = crud.check_if_genre_in_db(genre)
                    media.genres.append(genre)
                    db.session.commit()
                else:
                    # if not, add to genre:
                    genre = crud.add_genre_to_db(genre)
                    db.session.add(genre)
                    media.genres.append(genre)
                    db.session.commit()

    # add media to playlist
    if playlist_id != "no":
        playlist = crud.get_playlist_by_id(playlist_id, user)
        media.playlists.append(playlist)
        db.session.commit()
        # flash(f"{media.title} successfully added to {playlist.name}")
        return redirect (f"/media-info/{media_type}/{TMDB_id}")
    # else:
    #     flash("Please log in")

@app.route("/media-info/<media_type>/<TMDB_id>/rating", methods=["POST"])
def rate_media(media_type, TMDB_id):
    """Adds rating: Sets score user inputs under ratings"""
    
    score = request.form.get("score")
    comment = request.form.get("comment")
    media = crud.get_media_by_TMDB_id(TMDB_id, media_type)
    time_watched = request.form.get("watch_time")

    # add media to database if not in there already
    if not media:
        #get movie information
        url = f"https://api.themoviedb.org/3/{media_type}/{TMDB_id}"
        payload = {"api_key": API_KEY} 

        res = requests.get(url, params=payload)
        data = res.json()

        # add media to db
        if media_type == "movie":
            media = crud.add_movie_to_db(data)

        elif media_type == "tv":
            media = crud.add_show_to_db(data)

        db.session.add(media)
        db.session.commit()

        ### ADDING MEDIA GENRE INFORMATION ###
        # add genres to media that do not exist:
        if data["genres"]: 
            genres = data["genres"]
            for genre in genres:
                # check if genre in genres:
                if crud.check_if_genre_in_db(genre):
                    # if yes: 
                    genre = crud.check_if_genre_in_db(genre)
                    media.genres.append(genre)
                    db.session.commit()
                else:
                    # if not, add to genre:
                    genre = crud.add_genre_to_db(genre)
                    db.session.add(genre)
                    media.genres.append(genre)
                    db.session.commit()

    # add time watched 
    if time_watched:
        media.time_watched = time_watched
    else:
        # auto set time watched to day when added
        media.time_watched = date.today()
        db.session.commit()

    # get user
    user_username = session["username"]
    user = crud.get_user_by_username(user_username)

    # check if a score was input:
    if score:   

        # check if user has rated this media before:
        if crud.user_rated(media, user):

            # update the score in db
            if comment: 
                media_rating = crud.user_rated(media, user)
                media_rating.score = score
                media_rating.review_input = comment
                db.session.commit()
                # flash(f"Your score has been updated to {score} and your comment was successfully added to {media.title}")
            else:
                media_rating = crud.user_rated(media, user)
                media_rating.score = score
                db.session.commit()
                # flash(f"Your score has been updated to {score} for {media.title}")
        else:
            # add rating to media
            rating = crud.add_rating_to_db(score, user.user_id, media.media_id, comment)
            db.session.add(rating)
            db.session.commit()
            # flash(f"Your rating of {score} out of 5 and comment were successfully added for {media.title}")

            if crud.user_sorted_ToBeWatched(media,user):
                # delete from to_be_watched_list
                media_folder = crud.user_sorted_ToBeWatched(media, user)
                db.session.delete(media_folder)
                db.session.commit()

            # add media to watched list: 
            if not crud.user_sorted_Watched(media, user):
                # add to watched list
                media_folder = crud.add_to_WatchedList(media, user)
                db.session.add(media_folder)
                db.session.commit()
                # flash(f"{media.title} has been added to your watched list")

    return redirect(f"/media-info/{media_type}/{TMDB_id}")

@app.route("/<media_type>/<TMDB_id>/sort-folder", methods=["POST"])
def add_media_to_folder(media_type, TMDB_id):
    """Adds selected movie to watched or to be watched list"""

    folder = request.form.get("list")
    media = crud.get_media_by_TMDB_id(TMDB_id, media_type)
    time_watched = request.form.get("watch_time")

    # add media to database if not in there already
    if not media:
        #get mmdia information
        url = f"https://api.themoviedb.org/3/{media_type}/{TMDB_id}"
        payload = {"api_key": API_KEY} 

        res = requests.get(url, params=payload)
        data = res.json()

        # add media to db
        if media_type == "movie":
            media = crud.add_movie_to_db(data)

        elif media_type == "tv":
            media = crud.add_show_to_db(data)

        db.session.add(media)
        db.session.commit()

        ### ADDING MEDIA GENRE INFORMATION ###
        # add genres to media that do not exist:
        if data["genres"]: 
            genres = data["genres"]
            for genre in genres:
                # check if genre in genres:
                if crud.check_if_genre_in_db(genre):
                    # if yes: 
                    genre = crud.check_if_genre_in_db(genre)
                    media.genres.append(genre)
                    db.session.commit()
                else:
                    # if not, add to genre:
                    genre = crud.add_genre_to_db(genre)
                    db.session.add(genre)
                    media.genres.append(genre)
                    db.session.commit()

    # add time watched 
    if time_watched:
        media.time_watched = time_watched
    else:
        # auto set time watched to day when added
        media.time_watched = date.today()
        db.session.commit()
        
    # check if folder was selected:
    if folder:
        # check is user is logged in:
        if "username" in session:
            user_username = session["username"]
            user = crud.get_user_by_username(user_username)

            # sort into folder depending on value:
            if folder == "watched":
                
                # check if user added to watched_list before:
                # if crud.user_sorted_Watched(media, user):
                #     flash(f"{media.title} is already in your Watched List")

                # check if user added to to_be_watched_list before:
                if crud.user_sorted_ToBeWatched(media, user):
                    # delete from to_be_watched_list
                    media_folder = crud.user_sorted_ToBeWatched(media, user)
                    db.session.delete(media_folder)
                    db.session.commit()

                    # add to watched list
                    media_folder = crud.add_to_WatchedList(media, user)
                    db.session.add(media_folder)
                    db.session.commit()
                    # flash(f"{media.title} has been switched from your To Be Watched List to your Watched List")

                else:
                    # add to watched list:
                    media_folder = crud.add_to_WatchedList(media, user)
                    db.session.add(media_folder)
                    db.session.commit()
                    # flash(f"{media.title} has been added to your Watched List")


            elif folder == "to_be_watched":
                # check if user added to to_be_watched_list before:
                # if crud.user_sorted_ToBeWatched(media, user):
                    # flash(f"{media.title} is already in your To Be Watched List")

                # check if user added to to_be_watched_list before:
                if crud.user_sorted_Watched(media, user):
                    # flash(f"{media.title} is already in your To Be Watched List")
                    # delete from to be watched_list
                    media_folder = crud.user_sorted_Watched(media, user)
                    db.session.delete(media_folder)
                    db.session.commit()

                    # add to to_be_watched list
                    media_folder = crud.add_to_ToBeWatchedList(media, user)
                    db.session.add(media_folder)
                    db.session.commit()
                    # flash(f"{media.title} has been switched from your Watched List to your To Be Watched List")

                else:
                    # add to to_be_watched list:
                    media_folder = crud.add_to_ToBeWatchedList(media, user)
                    db.session.add(media_folder)
                    db.session.commit()
                    # flash(f"{media.title} has been added to your Watched List")

        # else:
        #     flash("Sorry, only logged in users can add movies to folders")

    # else:
    #     flash("Sorry, it seems no folder was selected.")

    return redirect(f"/media-info/{media_type}/{TMDB_id}")

@app.route("/user-profile/genres.json")
def get_users_genres():
    """Gets the users genres in their watched list"""

    # get user object: 
    user_username = session["username"]
    user = crud.get_user_by_username(user_username)

    # get users genres:
    user_genres = crud.get_user_genres(user)
    
    genres = []

    for genre, total in user_genres.items():
        genres.append({'genre': genre.genre_name,'number_of_genre': total})

    return jsonify({"data": genres})

@app.route("/user-profile/watch_history.json")
def get_users_watch_history():
    """Gets the users watch history"""

    # get user object: 
    user_username = session["username"]
    user = crud.get_user_by_username(user_username)

    # get users watch history
    user_movie_watch_history = crud.get_user_movie_watch_history(user)
    user_show_watch_history = crud.get_user_show_watch_history(user)
    
    movie_history = []
    show_history = []

    # for day, total in user_movie_watch_history.items():
        # movie_history.append({'day': day.isoformat(),'number_of_movies': total})
    for month, total in user_movie_watch_history.items():
        movie_history.append({'month': month,'number_of_movies': total})

    # for day, total in user_show_watch_history.items():
        # show_history.append({'day': day.isoformat(),'number_of_shows': total})
    for month, total in user_show_watch_history.items():
        show_history.append({'month': month,'number_of_shows': total})

    return jsonify({"moviedata": movie_history, "showdata": show_history})

@app.route("/recommended")
def display_recommended_media():

    if "username" in session:
        # get user:
        user_username = session["username"]
        user = crud.get_user_by_username(user_username)

        # get last things added to watched list
        last_movie = crud.get_last_movie_added_to_watched_list(user)
        last_show = crud.get_last_show_added_to_watched_list(user)

        #get movie recommended
        if last_movie != False:
            url = f"https://api.themoviedb.org/3/movie/{last_movie.TMDB_id}/recommendations"

            payload = {"api_key": API_KEY} 

            movie_res = requests.get(url, params=payload)
            movie_data = movie_res.json()
            movie_results=movie_data["results"]
        else:
            movie_data = None
            movie_results = None

        #get show recommended
        if last_show != False:
            url = f"https://api.themoviedb.org/3/tv/{last_show.TMDB_id}/recommendations"

            payload = {"api_key": API_KEY} 

            show_res = requests.get(url, params=payload)
            show_data = show_res.json()
            show_results = show_data["results"]

        else:
            show_data = None
            show_results = None

        # get trending movies: 
        url = f"https://api.themoviedb.org/3/trending/movie/day"

        payload = {"api_key": API_KEY} 

        trending_movie_res = requests.get(url, params=payload)
        trending_movie_data = trending_movie_res.json()
        trending_movie_results = trending_movie_data["results"]

        # get trending shows: 
        url = f"https://api.themoviedb.org/3/trending/tv/day"

        payload = {"api_key": API_KEY} 

        trending_show_res = requests.get(url, params=payload)
        trending_show_data = trending_show_res.json()
        trending_show_results = trending_show_data["results"]

        return render_template("/recommended.html", user=user, movie_results=movie_results, show_results=show_results, trending_movie_results=trending_movie_results,trending_show_results=trending_show_results)

    else:
        # get trending movies: 
        url = f"https://api.themoviedb.org/3/trending/movie/day"

        payload = {"api_key": API_KEY} 

        trending_movie_res = requests.get(url, params=payload)
        trending_movie_data = trending_movie_res.json()
        trending_movie_results = trending_movie_data["results"]

        # get trending shows: 
        url = f"https://api.themoviedb.org/3/trending/tv/day"

        payload = {"api_key": API_KEY} 

        trending_show_res = requests.get(url, params=payload)
        trending_show_data = trending_show_res.json()
        trending_show_results = trending_show_data["results"]

        return render_template("/recommended.html", user=None, movie_results=None, show_results=None, trending_movie_results=trending_movie_results,trending_show_results=trending_show_results)
        # flash("Sorry, please log in:")

        # return redirect("/")


@app.route("/create-playlist", methods=["POST"])
def creates_playlist_for_user():
    """Adds a playlist for user to store movies in"""
    playlist_name = request.form.get("playlist_name")
    user_username = session["username"]

    user = crud.get_user_by_username(user_username)

    if playlist_name: 
        playlist = crud.create_playlist(playlist_name, user)
        db.session.add(playlist)
        db.session.commit()
        # flash(f"The playlist '{playlist_name}' has successfully been created")

    return redirect("/user-profile")

#### ALL THE DELETING STUFF #####

@app.route("/delete-rating.json", methods=["POST"])
def deletes_rating_for_user_media_page():
    """Deletes a rating for user"""
    rating_id = request.json.get("ratingID")
    user_username = session["username"]
    user = crud.get_user_by_username(user_username)

    if rating_id:
        rating = crud.get_rating_by_id(rating_id, user)
        db.session.delete(rating)
        db.session.commit()

    return jsonify({"success": "The rating has successfully been deleted"})

@app.route("/user-profile/delete-from-watched-list.json", methods=['POST'])
def remove_media_from_watchedlist():
    """Allows user to remove media from their watched list"""
    user_username = session["username"]
    user = crud.get_user_by_username(user_username)
    media_id = request.json.get("mediaID")

    if media_id:
        media = crud.get_watchlist_media_by_id(media_id, user)
        db.session.delete(media)
        db.session.commit()
        # flash(f"Removed from watched list")

    return jsonify({"success": "Removed from watched list"})

@app.route("/user-profile/delete-from-to-be-watched-list.json", methods=['POST'])
def remove_media_from_tobe_watchedlist():
    """Allows user to remove media from their to be watched list"""
    user_username = session["username"]
    user = crud.get_user_by_username(user_username)
    media_id = request.json.get("mediaID")

    if media_id:
        media = crud.get_tobewatchlist_media_by_id(media_id, user)
        db.session.delete(media)
        db.session.commit()
        # flash(f"Removed from to be watched list")

    return jsonify({"success": "Removed from to be watched list"})

@app.route("/user-profile/edit-playlist/<playlist_id>")
def edit_playlist(playlist_id):

    user_username = session["username"]
    user = crud.get_user_by_username(user_username)
    playlist = crud.get_playlist_by_id(playlist_id, user)
    
    return render_template("/individual_playlist.html", playlist=playlist, user=user)

@app.route("/user-profile/edit-list/<lst>")
def edit_list(lst):

    user_username = session["username"]
    user = crud.get_user_by_username(user_username)

    if lst == "watched":
        watched = user.watched_list
        return render_template("/individual_lists.html", lst=watched, name="Watched List", type="watched", user=user)

    elif lst == "tobewatched":
        to_be_watched = user.to_be_watched_list
        return render_template("/individual_lists.html", lst=to_be_watched, name="To Be Watched List", type="tobewatched", user=user)
    
@app.route("/delete-playlist", methods=["POST"])
def deletes_playlist():
    """Deletes a playlist for user"""
    playlist_id = request.form.get("playlist_id")
    user_username = session["username"]
    user = crud.get_user_by_username(user_username)

    if playlist_id:
        playlist = crud.get_playlist_by_id(playlist_id, user)
        db.session.delete(playlist)
        db.session.commit()
        # flash(f"The playlist '{playlist.name}' has successfully been deleted")

    return redirect("/user-profile")

@app.route("/user-profile/delete-from-playlist.json", methods=['POST'])
def remove_media_from_playlist():
    """Allows user to remove media from their playlist"""
    user_username = session["username"]
    user = crud.get_user_by_username(user_username)
    
    playlist_id = request.json.get("playlistID")
    playlist = crud.get_playlist_by_id(playlist_id, user)
    
    media_id = request.json.get("mediaID")
    
    if media_id:
        media = crud.get_media_by_id(media_id)
        media.playlists.remove(playlist)
        db.session.commit()

    return jsonify({"success": "Removed from to be watched list"})

if __name__ == "__main__":
    connect_to_db(app)  

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", debug=True)