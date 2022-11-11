"""Server for movie app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
import os
import requests

from jinja2 import StrictUndefined

# importing hashing passwords
from passlib.hash import argon2

app = Flask(__name__)
app.secret_key = "forsession"
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ['TMDB_KEY']

@app.route("/")
def homepage():
    """Displays homepage"""

    return render_template("homepage.html")

######## Not used currently after implementing REACT
@app.route("/search")
def display_search_bar():
    """Displays search bar for media page before REACT"""

    return render_template("search_media.html")
###################################################

@app.route("/search-friends")
def display_search():
    """Displays search bar to search for friends"""

    if "email" in session: 
        user_email = session["email"]
        user = crud.get_user_by_email(user_email)
        all_users_not_user = crud.get_all_users_not_user(user)
        return render_template("/search_friends.html", user=user, all_users_not_user=all_users_not_user)

    else:
        flash("Sorry, please log in:")
        return redirect("/")

@app.route("/create-user")
def display_create_user():
    """Shows the create user page"""

    return render_template("create_user.html")

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
        # user = crud.create_user(username=username, email=email, password=password)
        # store the hashed password in the database instead
        user = crud.create_user(username=username, email=email, password=password_hashed)
        db.session.add(user)
        db.session.commit()
        flash ("Succesfully created user")
        return redirect ("/")

    return redirect ("/create-user")
   

@app.route("/login", methods=["POST"])
def login_user():
    """Logs in the user"""

    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if user:
        # if password == user.password:
        # do it getting the hashed password: 
        if argon2.verify(password, user.password):
            session["username"] = user.username
            session['email'] = email
            flash("You have successfully logged in")
            return redirect ("/user-profile")
        else:
            flash("Your password was incorrect. Please try again.")

    else:
        flash("Sorry, a user with that email doesn't exist")

    return redirect("/")

@app.route("/logout")
def logout_user():
    """Logs out the user by clearing the session."""
    if "email" in session: 
        session.clear()
        flash("You've been logged out")

    else:
        flash("Sorry, please log in:")
        return redirect("/")
    
    return redirect("/")

@app.route("/user-profile")
def display_user_profile():
    """Displays the user profile page"""

    if "email" in session: 
        user_email = session["email"]
        user = crud.get_user_by_email(user_email)
        return render_template("user_profile.html", user=user)

    else:
        flash("Sorry, please log in:")
        return redirect("/")

@app.route("/user-profile/create-playlist", methods=["POST"])
def creates_playlist_for_user():
    """Adds a playlist for user to store movies in"""
    playlist_name = request.form.get("playlist_name")
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    if playlist_name: 
        playlist = crud.create_playlist(playlist_name, user)
        db.session.add(playlist)
        db.session.commit()
        flash(f"The playlist '{playlist_name}' has successfully been created")

    return redirect("/user-profile")

@app.route("/user-profile/delete-playlist", methods=["POST"])
def deletes_playlist_for_user():
    """Deletes a playlist for user"""
    playlist_id = request.form.get("playlist_id")
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    if playlist_id:
        playlist = crud.get_playlist_by_id(playlist_id, user)
        db.session.delete(playlist)
        db.session.commit()
        flash(f"The playlist '{playlist.name}' has successfully been deleted")

    return redirect("/user-profile")

@app.route("/user-profile/delete-rating", methods=["POST"])
def deletes_rating_for_user():
    """Deletes a rating for user on the user's profile"""
    rating_id = request.form.get("rating_id")
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    if rating_id:
        rating = crud.get_rating_by_id(rating_id, user)
        db.session.delete(rating)
        db.session.commit()
        flash(f"The rating has successfully been deleted")

    return redirect("/user-profile")

@app.route("/media-info/<media_type>/delete-rating", methods=["POST"])
def deletes_rating_for_user_media_page(media_type):
    """Deletes a rating for user on the media page"""
    rating_id = request.form.get("rating_id")
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    if rating_id:
        rating = crud.get_rating_by_id(rating_id, user)
        media = crud.get_media_by_rating(rating)
        db.session.delete(rating)
        db.session.commit()
        flash(f"The rating has successfully been deleted")

    return redirect(f"/media-info/{media_type}/{media.TMDB_id}")


@app.route("/friend-search-results", methods=["POST"])
def show_friend_search_results():
    """Shows friend profile as search result it username exists"""
    
    # if not user2: 
    search_text = request.form.get("friend_username")

    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    user2 = crud.get_user_by_username(search_text)

    if user2: 
        return render_template("/search_friend_result.html", user2=user2, user=user, user2_user_id= user2.user_id)

    else: 
        flash(f"Sorry, no user exists with the username '{search_text}'.")
        return redirect("/search-friends")

@app.route("/friend/<user2_user_id>/follow-status", methods=["POST"])
def follow_or_unfollow_friends(user2_user_id):
    """Allows user to unfollow or follow a friend"""

    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    user2 = crud.get_user_by_id(user2_user_id)

    action = request.form.get("following")

    if action == "follow": 
        user.following.append(user2)
        db.session.commit()

    elif action == "unfollow": 
        ### figure out how to unfollow 
        user.following.remove(user2)
        db.session.commit()

    return render_template("/search_friend_result.html", user2=user2, user=user, user2_user_id= user2.user_id)


@app.route('/display-friend/<friend_username>')
def display_friend_by_username(friend_username):
    """Displays friend profile when user clicks on their name in user profile"""

    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    user2 = crud.get_user_by_username(friend_username)

    # if user2: 
    return render_template("/search_friend_result.html", user2=user2, user=user, user2_user_id= user2.user_id)


#### MOVIE AND TV SHOWS SEPARATED BELOW IN DIFFERENT ROUTES BECAUSE OF REPEATED TMDB_ID's ####   
@app.route("/media-search-results", methods=["POST"])
def show_search_results():
    "Displays results from search bar query"

    search_text = request.form.get("title")
    media_type = request.form.get("media_type")

    #for movies: 
    if media_type == "movie":
        url = "https://api.themoviedb.org/3/search/movie"

    #for tv shows:
    elif media_type == "show":
        url = "https://api.themoviedb.org/3/search/tv"
    payload = {"api_key": API_KEY} 

    # add media title to payload
    if search_text:
        payload["query"]=search_text

    res = requests.get(url, params=payload)
    data = res.json()

    results = data['results']

    return render_template("all_media.html", data=data, search_text=search_text, results=results, res=res, media_type=media_type)

################################################# REACT #################################################
@app.route("/media-search-results-react.json",  methods=["POST"])
def get_search_results_react_json():
    """Return a JSON response with all media from search bar query"""

    # REACT getting version
    search_text = request.get_json().get("search")
    media_type = request.get_json().get("mediaType")
    

    #for movies: 
    if media_type == "movie":
        url = "https://api.themoviedb.org/3/search/movie"

    #for tv shows:
    elif media_type == "show":
        url = "https://api.themoviedb.org/3/search/tv"
    payload = {"api_key": API_KEY} 

    # add media title to payload
    if search_text:
        payload["query"]=search_text

    res = requests.get(url, params=payload)
    data = res.json()

    results = data['results']

    # return render_template("all_media.html", data=data, search_text=search_text, results=results, res=res, media_type=media_type)
    return jsonify({"media": results, "search_text": search_text, "media_type": media_type })

@app.route("/media-search-results-react")
def show_react_search_results():
    """Show all media using REACT"""

    return render_template("all_media_react.html")

################################################# REACT #################################################

#for movie media_info 
@app.route("/media-info/movie/<TMDB_id>")
def show_movie(TMDB_id):
    """Shows specific movie information for selected movie"""

    #get media information
    # for movie: 
    url = f"https://api.themoviedb.org/3/movie/{TMDB_id}"

    #for tv show: 
    payload = {"api_key": API_KEY} 

    res = requests.get(url, params=payload)
    data = res.json()
    
    # filter for that movies ratings in db to display on media page
    if crud.get_media_by_TMDB_id(TMDB_id, "movie"):
        movie = crud.get_media_by_TMDB_id(TMDB_id, "movie")
        movie_id = movie.media_id
        all_ratings = crud.get_all_ratings(movie_id)

    else: 
        all_ratings = False

    # check if user is logged in in order to display playlists correctly 
    if "email" in session:
        user = crud.get_user_by_email(session["email"])
        return render_template("media_information.html", data=data, TMDB_id=TMDB_id, user=user, media_type="movie", all_ratings=all_ratings)

    else:
        return render_template("media_information.html", data=data, TMDB_id=TMDB_id, user=False, media_type="movie", all_ratings=all_ratings)

#for tv show media_info 
@app.route("/media-info/tvshow/<TMDB_id>")
def show_tv_show(TMDB_id):
    """Shows specific tv show information for selected tv show"""

    #get media information
    # for movie: 
    url = f"https://api.themoviedb.org/3/tv/{TMDB_id}"

    #for tv show: 
    payload = {"api_key": API_KEY} 

    res = requests.get(url, params=payload)
    data = res.json()

    # filter for that tv shows ratings in db to display on media page
    if crud.get_media_by_TMDB_id(TMDB_id, "show"):
        show = crud.get_media_by_TMDB_id(TMDB_id, "show")
        show_id = show.media_id
        all_ratings = crud.get_all_ratings(show_id)

    else: 
        all_ratings = False

    # check if user is logged in in order to display playlists correctly 
    if "email" in session:
        user = crud.get_user_by_email(session["email"])
        return render_template("media_information.html", data=data, TMDB_id=TMDB_id, user=user, media_type="show", all_ratings=all_ratings)

    else:
        return render_template("media_information.html", data=data, TMDB_id=TMDB_id, user=False, media_type="show", all_ratings=all_ratings)

##### ADDING MOVIE TO PLAYLIST
@app.route("/movie/<TMDB_id>/add-to-playlist", methods=["POST"])
def add_movie_to_playlist(TMDB_id):
    """Adds movie to selected playlist"""
    movie = crud.get_media_by_TMDB_id(TMDB_id, "movie")
    playlist_id = request.form.get("playlist")
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    # add movie to database if not in there already
    if not movie:
        #get movie information
        url = f"https://api.themoviedb.org/3/movie/{TMDB_id}"
        payload = {"api_key": API_KEY} 

        res = requests.get(url, params=payload)
        data = res.json()

        # add movie to db
        movie = crud.add_movie_to_db(data)
        db.session.add(movie)
        db.session.commit()

        ### ADDING MOVIE GENRE INFORMATION ###
        # add genres to movie that do not exist:
        genres = data["genres"]
        for genre in genres:
            # check if genre in genres:
            if crud.check_if_genre_in_db(genre):
                # if yes: 
                genre = crud.check_if_genre_in_db(genre)
                movie.genres.append(genre)
                db.session.commit()
            else:
                # if not, add to genre:
                genre = crud.add_genre_to_db(genre)
                db.session.add(genre)
                movie.genres.append(genre)
                db.session.commit()

    # add show to playlist
    if playlist_id != "no":
        playlist = crud.get_playlist_by_id(playlist_id, user)
        movie.playlists.append(playlist)
        db.session.commit()
        flash(f"Movie successfully added to {playlist.name}")
        return redirect (f"/media-info/movie/{TMDB_id}")
    else:
        flash("Please log in")

##### ADDING MOVIE RATING
@app.route("/media-info/movie/<TMDB_id>/rating", methods=["POST"])
def rate_movie(TMDB_id):
    """Sets score user input under ratings"""
    
    score = request.form.get("score")
    comment = request.form.get("comment")
    movie = crud.get_media_by_TMDB_id(TMDB_id, "movie")
    time_watched = request.form.get("watch_time")

    # add movie to database if not in there already
    if not movie:
        #get movie information
        url = f"https://api.themoviedb.org/3/movie/{TMDB_id}"
        payload = {"api_key": API_KEY} 

        res = requests.get(url, params=payload)
        data = res.json()

        # add movie to db
        movie = crud.add_movie_to_db(data)
        db.session.add(movie)
        db.session.commit()

        ### ADDING MOVIE GENRE INFORMATION ###
        # add genres to movie that do not exist:
        genres = data["genres"]
        for genre in genres:
            # check if genre in genres:
            if crud.check_if_genre_in_db(genre):
                # if yes: 
                genre = crud.check_if_genre_in_db(genre)
                movie.genres.append(genre)
                db.session.commit()
            else:
                # if not, add to genre:
                genre = crud.add_genre_to_db(genre)
                db.session.add(genre)
                movie.genres.append(genre)
                db.session.commit()

    # check if a score was input:
    if score:   

        # check if user is logged in: 
        if "email" in session:
            user_email = session["email"]
            user = crud.get_user_by_email(user_email)

            # check if user has rated this media before:
            if crud.user_rated(movie, user):

                # update the score in db
                if comment: 
                    movie_rating = crud.user_rated(movie, user)
                    movie_rating.score = score
                    movie_rating.review_input = comment
                    db.session.commit()
                    # add time watched if exists: 
                    if time_watched:
                        movie.time_watched = time_watched
                        db.session.commit()
                    flash(f"Your score has been updated to {score} and your comment was successfully added")
                else:
                    movie_rating = crud.user_rated(movie, user)
                    movie_rating.score = score
                    db.session.commit()
                    # add time watched if exists: 
                    if time_watched:
                        movie.time_watched = time_watched
                        db.session.commit()
                    flash(f"Your score has been updated to {score}")
            else:
                # add rating to movie 
                rating = crud.add_rating_to_db(score, user.user_id, movie.media_id, comment)
                db.session.add(rating)
                db.session.commit()
                # add time watched if exists: 
                if time_watched:
                    movie.time_watched = time_watched
                    db.session.commit()
                flash(f"Your rating of {score} out of 5 and comment were successfully added for {movie.title}")

                # add movie to watched list: 
                if not crud.user_sorted_Watched(movie, user):
                    # add to watched list
                    movie_folder = crud.add_to_WatchedList(movie, user)
                    db.session.add(movie_folder)
                    db.session.commit()
                    flash(f"Your media has been added to your watched list")

        else:
            flash("Sorry, only logged in users can rate movies")
    else: 
        flash("Sorry, it seems no score was selected.")

    return redirect(f"/media-info/movie/{TMDB_id}")

##### ADDING MOVIE TO FOLDER WATCHED VS NOT
@app.route("/movie/<TMDB_id>/sort-folder", methods=["POST"])
def add_movie_to_folder(TMDB_id):
    """Adds selected movie to watched or to be watched list"""

    folder = request.form.get("list")
    movie = crud.get_media_by_TMDB_id(TMDB_id, "movie")
    time_watched = request.form.get("watch_time")

    # add movie to database if not in there already
    if not movie:
        #get movie information
        url = f"https://api.themoviedb.org/3/movie/{TMDB_id}"
        payload = {"api_key": API_KEY} 

        res = requests.get(url, params=payload)
        data = res.json()

        # add movie to db
        movie = crud.add_movie_to_db(data)
        db.session.add(movie)
        db.session.commit()

        # add time watched if exists: 
        if time_watched:
            movie.time_watched = time_watched
            db.session.commit()

        ### ADDING MOVIE GENRE INFORMATION ###
        # add genres to movie that do not exist:
        genres = data["genres"]
        for genre in genres:
            # check if genre in genres:
            if crud.check_if_genre_in_db(genre):
                # if yes: 
                genre = crud.check_if_genre_in_db(genre)
                movie.genres.append(genre)
                db.session.commit()
            else:
                # if not, add to genre:
                genre = crud.add_genre_to_db(genre)
                db.session.add(genre)
                movie.genres.append(genre)
                db.session.commit()

    # check if folder was selected:
    if folder:
        # check is user is logged in:
        if "email" in session:
            user_email = session["email"]
            user = crud.get_user_by_email(user_email)

            # sort into folder depending on value:
            if folder == "watched":
                
                # check if user added to watched_list before:
                if crud.user_sorted_Watched(movie, user):
                    flash("This movie is already in your Watched List")

                # check if user added to to_be_watched_list before:
                elif crud.user_sorted_ToBeWatched(movie, user):
                    # delete from to_be_watched_list
                    movie_folder = crud.user_sorted_ToBeWatched(movie, user)
                    db.session.delete(movie_folder)
                    db.session.commit()

                    # add to watched list
                    movie_folder = crud.add_to_WatchedList(movie, user)
                    db.session.add(movie_folder)
                    db.session.commit()
                    flash("This movie has been switched from your To Be Watched List to your Watched List")

                else:
                    # add to watched list:
                    movie_folder = crud.add_to_WatchedList(movie, user)
                    db.session.add(movie_folder)
                    db.session.commit()
                    flash("This movie has been added to your Watched List")


            elif folder == "to_be_watched":
                # check if user added to to_be_watched_list before:
                if crud.user_sorted_ToBeWatched(movie, user):
                    flash("This movie is already in your To Be Watched List")

                # check if user added to watched_list before:
                elif crud.user_sorted_Watched(movie, user):
                    flash("This movie is already in your Watched List")
                    # delete from watched_list
                    movie_folder = crud.user_sorted_Watched(movie, user)
                    db.session.delete(movie_folder)
                    db.session.commit()

                    # add to to_be_watched list
                    movie_folder = crud.add_to_ToBeWatchedList(movie, user)
                    db.session.add(movie_folder)
                    db.session.commit()
                    flash("This movie has been switched from your Watched List to your To Be Watched List")

                else:
                    # add to to_be_watched list:
                    movie_folder = crud.add_to_ToBeWatchedList(movie, user)
                    db.session.add(movie_folder)
                    db.session.commit()
                    flash("This movie has been added to your Watched List")

        else:
            flash("Sorry, only logged in users can add movies to folders")

    else:
        flash("Sorry, it seems no folder was selected.")

    return redirect(f"/media-info/movie/{TMDB_id}")

##### ADDING SHOW TO PLAYLIST
@app.route("/tvshow/<TMDB_id>/add-to-playlist", methods=["POST"])
def add_show_to_playlist(TMDB_id):
    """Adds show to selected playlist"""
    show = crud.get_media_by_TMDB_id(TMDB_id, "show")
    playlist_id = request.form.get("playlist")
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    # add show to database if not in there already
    if not show:
        #get show information
        url = f"https://api.themoviedb.org/3/tv/{TMDB_id}"
        payload = {"api_key": API_KEY} 

        res = requests.get(url, params=payload)
        data = res.json()

        # add show to db
        show = crud.add_show_to_db(data)
        db.session.add(movie)
        db.session.commit()

        ### Note CANNOT ADD SHOW GENRE INFORMATION BC DB DOES NOT HAVE###

    # add to playlist
    if playlist_id != "no":
        playlist = crud.get_playlist_by_id(playlist_id, user)
        show.playlists.append(playlist)
        db.session.commit()
        flash(f"Show successfully added to {playlist.name}")
        return redirect (f"/media-info/tvshow/{TMDB_id}")
    else:
        flash("Please log in")

##### ADDING SHOW RATING
@app.route("/media-info/tvshow/<TMDB_id>/rating", methods=["POST"])
def rate_show(TMDB_id):
    """Sets score user input under ratings"""
    
    score = request.form.get("score")
    comment = request.form.get("comment")
    show = crud.get_media_by_TMDB_id(TMDB_id, "show")
    time_watched = request.form.get("watch_time")

    # add show to database if not in there already
    if not show:
        #get show information
        url = f"https://api.themoviedb.org/3/tv/{TMDB_id}"
        payload = {"api_key": API_KEY} 

        res = requests.get(url, params=payload)
        data = res.json()

        # add show to db
        show = crud.add_show_to_db(data)
        db.session.add(show)
        db.session.commit()

        ### Note CANNOT ADD SHOW GENRE INFORMATION BC DB DOES NOT HAVE###

    # check if a score was input:
    if score:   

        # check if user is logged in: 
        if "email" in session:
            user_email = session["email"]
            user = crud.get_user_by_email(user_email)

            # check if user has rated this media before:
            if crud.user_rated(show, user):

                # update the score in db
                if comment: 
                    show_rating = crud.user_rated(show, user)
                    show_rating.score = score
                    show_rating.review_input = comment
                    db.session.commit()
                    # add time watched if exists: 
                    if time_watched:
                        show.time_watched = time_watched
                        db.session.commit()
                    flash(f"Your score has been updated to {score} and your comment was successfully added")
                else:
                    show_rating = crud.user_rated(show, user)
                    show_rating.score = score
                    db.session.commit()
                    # add time watched if exists: 
                    if time_watched:
                        show.time_watched = time_watched
                        db.session.commit()
                    flash(f"Your score has been updated to {score}")
            else:
                # add rating to show
                rating = crud.add_rating_to_db(score, user.user_id, show.media_id, comment)
                db.session.add(rating)
                db.session.commit()
                # add time watched if exists: 
                if time_watched:
                    show.time_watched = time_watched
                    db.session.commit()
                flash(f"Your rating of {score} out of 5 and comment were successfully added for {show.title}")

                # add movie to watched list: 
                if not crud.user_sorted_Watched(show, user):
                    # add to watched list
                    show_folder = crud.add_to_WatchedList(show, user)
                    db.session.add(show_folder)
                    db.session.commit()
                    flash(f"Your show has been added to your watched list")

        else:
            flash("Sorry, only logged in users can rate shows")
    else: 
        flash("Sorry, it seems no score was selected.")

    return redirect(f"/media-info/tvshow/{TMDB_id}")

##### ADDING SHOW TO FOLDER WATCHED VS NOT
@app.route("/tvshow/<TMDB_id>/sort-folder", methods=["POST"])
def add_show_to_folder(TMDB_id):
    """Adds selected show to watched or to be watched list"""

    folder = request.form.get("list")
    show= crud.get_media_by_TMDB_id(TMDB_id, "show")
    time_watched = request.form.get("watch_time")

    # add show to database if not in there already
    if not show:
        #get show information
        url = f"https://api.themoviedb.org/3/tv/{TMDB_id}"
        payload = {"api_key": API_KEY} 

        res = requests.get(url, params=payload)
        data = res.json()

        # add show to db
        show = crud.add_show_to_db(data)
        db.session.add(show)
        db.session.commit()

        # add time watched if exists: 
        if time_watched:
            show.time_watched = time_watched
            db.session.commit()

        ### Note CANNOT ADD SHOW GENRE INFORMATION BC DB DOES NOT HAVE###

    # check if folder was selected:
    if folder:
        # check is user is logged in:
        if "email" in session:
            user_email = session["email"]
            user = crud.get_user_by_email(user_email)

            # sort into folder depending on value:
            if folder == "watched":
                
                # check if user added to watched_list before:
                if crud.user_sorted_Watched(show, user):
                    flash("This show is already in your Watched List")

                # check if user added to to_be_watched_list before:
                elif crud.user_sorted_ToBeWatched(show, user):
                    # delete from to_be_watched_list
                    show_folder = crud.user_sorted_ToBeWatched(show, user)
                    db.session.delete(show_folder)
                    db.session.commit()

                    # add to watched list
                    show_folder = crud.add_to_WatchedList(show, user)
                    db.session.add(show_folder)
                    db.session.commit()
                    flash("This show has been switched from your To Be Watched List to your Watched List")

                else:
                    # add to watched list:
                    show_folder = crud.add_to_WatchedList(show, user)
                    db.session.add(show_folder)
                    db.session.commit()
                    flash("This show has been added to your Watched List")


            elif folder == "to_be_watched":
                # check if user added to to_be_watched_list before:
                if crud.user_sorted_ToBeWatched(show, user):
                    flash("This show is already in your To Be Watched List")

                # check if user added to watched_list before:
                elif crud.user_sorted_Watched(show, user):
                    flash("This show is already in your Watched List")
                    # delete from watched_list
                    show_folder = crud.user_sorted_Watched(show, user)
                    db.session.delete(show_folder)
                    db.session.commit()

                    # add to to_be_watched list
                    show_folder = crud.add_to_ToBeWatchedList(show, user)
                    db.session.add(show_folder)
                    db.session.commit()
                    flash("This show has been switched from your Watched List to your To Be Watched List")

                else:
                    # add to to_be_watched list:
                    show_folder = crud.add_to_ToBeWatchedList(show, user)
                    db.session.add(show_folder)
                    db.session.commit()
                    flash("This show has been added to your Watched List")

        else:
            flash("Sorry, only logged in users can add shows to folders")

    else:
        flash("Sorry, it seems no folder was selected.")

    return redirect(f"/media-info/tvshow/{TMDB_id}")

@app.route("/user-profile/genres.json")
def get_users_genres():
    """Gets the users genres in their watched list"""

    # get user object: 
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

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
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    # get users watch history
    user_movie_watch_history = crud.get_user_movie_watch_history(user)
    user_show_watch_history = crud.get_user_show_watch_history(user)
    
    movie_history = []
    show_history = []

    for day, total in user_movie_watch_history.items():
        movie_history.append({'day': day.isoformat(),'number_of_movies': total})

    for day, total in user_show_watch_history.items():
        show_history.append({'day': day.isoformat(),'number_of_shows': total})

    return jsonify({"moviedata": movie_history, "showdata": show_history})

@app.route("/user-profile/delete-from-watched-list", methods=['POST'])
def remove_media_from_watchedlist():
    """Allows user to remove media from their watched list"""
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)
    media_id = request.form.get("media_id")

    if media_id:
        media = crud.get_watchlist_media_by_id(media_id, user)
        db.session.delete(media)
        db.session.commit()
        flash(f"Removed from watched list")

    return redirect("/user-profile")

@app.route("/user-profile/delete-from-to-be-watched-list", methods=['POST'])
def remove_media_from_tobe_watchedlist():
    """Allows user to remove media from their to be watched list"""
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)
    media_id = request.form.get("media_id")

    if media_id:
        media = crud.get_tobewatchlist_media_by_id(media_id, user)
        db.session.delete(media)
        db.session.commit()
        flash(f"Removed from to be watched list")

    return redirect("/user-profile")

@app.route("/user-profile/delete-from/<playlist_id>", methods=['POST'])
def remove_media_from_playlist(playlist_id):
    """Allows user to remove media from their playlist"""
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)
    playlist = crud.get_playlist_by_id(playlist_id, user)
    media_id = request.form.get("media_id")
    
    if media_id:
        media = crud.get_media_by_id(media_id)
        media.playlists.remove(playlist)
        db.session.commit()
        flash(f"Removed from playlist")

    return redirect("/user-profile")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)