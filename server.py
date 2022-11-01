"""Server for movie app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
import os
import requests

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "forsession"
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ['TMDB_KEY']

@app.route("/")
def homepage():
    """Displays homepage"""

    return render_template("homepage.html")

@app.route("/search")
def display_search_bar():
    """Displays search bar for media page"""

    return render_template("search_media.html")


@app.route("/media-search-results", methods=["POST"])
def show_search_results():
    "Displays results from search bar query"

    search_text = request.form.get("title")

    url = "https://api.themoviedb.org/3/search/movie"
    payload = {"api_key": API_KEY} 

    # add movie title to payload
    if search_text:
        payload["query"]=search_text

    res = requests.get(url, params=payload)
    data = res.json()

    results = data['results']

    return render_template("all_media.html", data=data, search_text=search_text, results=results, res=res)

@app.route("/media-info/<TMDB_id>")
def show_media(TMDB_id):
    """Shows specific media information for selected media"""

     #get media information
    url = f"https://api.themoviedb.org/3/movie/{TMDB_id}"
    payload = {"api_key": API_KEY} 

    res = requests.get(url, params=payload)
    data = res.json()

    return render_template("media_information.html", data=data, TMDB_id=TMDB_id)

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

    if crud.get_user_by_username(username):
        flash("Sorry, that username is already taken.")

    elif crud.get_user_by_email(email):
        flash("Sorry, that email is already taken")

    else:
        user = crud.create_user(username=username, email=email, password=password)
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
        if password == user.password:
            session["username"] = user.username
            session['email'] = email
            flash("You have successfully logged in")
            return redirect ("/user-profile")
        else:
            flash("Your password was incorrect. Please try again.")

    else:
        flash("Sorry, a user with that email doesn't exist")

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

@app.route("/media-info/<TMDB_id>/rating", methods=["POST"])
def rate_movie(TMDB_id):
    """Sets score user input in under ratings"""
    
    score = request.form.get("score")
    comment = request.form.get("comment")
    movie = crud.get_media_by_TMDB_id(TMDB_id)

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
                    flash(f"Your score has been updated to {score} and your comment was successfully added")
                else:
                    movie_rating = crud.user_rated(movie, user)
                    movie_rating.score = score
                    db.session.commit()
                    flash(f"Your score has been updated to {score}")
            else:
                # add rating to movie 
                rating = crud.add_rating_to_db(score, user.user_id, movie.media_id, comment)
                db.session.add(rating)
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

    return redirect(f"/media-info/{TMDB_id}")

@app.route("/<TMDB_id>/sort-folder", methods=["POST"])
def add_movie_to_folder(TMDB_id):
    """Adds selected movie to watched or to be watched list"""

    folder = request.form.get("list")
    movie = crud.get_media_by_TMDB_id(TMDB_id)

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

    return redirect(f"/media-info/{TMDB_id}")

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

########################################################################################################################

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)