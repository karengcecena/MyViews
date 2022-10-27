"""Server for movie app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
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

######### this needs work 10/26 ############################
@app.route("/user-profile")
def display_user_profile():
    """Displays the user profile page"""
    user_email = session["email"]
    user = crud.get_user_by_email(user_email)

    return render_template("user_profile.html", user=user)
############################################################


@app.route("/media-info/<TMDB_id>/rating", methods=["POST"])
def rate_movie(TMDB_id):
    """Sets score user input in under ratings"""
    
    score = request.form.get("score")
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
    
    # check if a score was input:
    if score:   

        # check if user is logged in: 
        if "email" in session:
            user_email = session["email"]
            user = crud.get_user_by_email(user_email)

            # check if user has rated this media before:
            if crud.user_rated(movie, user):

                # update the score in db
                movie_rating = crud.user_rated(movie, user)
                movie_rating.score = score
                db.session.commit()

                flash(f"Your score has been updated to {score}")

            else:
                # add rating to movie 
                rating = crud.add_rating_to_db(score, user.user_id, movie.media_id)
                db.session.add(rating)
                db.session.commit()
                flash(f"You rated {data['original_title']} a {score} out of 5")

        else:
            flash("Sorry, only logged in users can rate movies")
    else: 
        flash("Sorry, it seems no score was selected.")

    return redirect(f"/media-info/{TMDB_id}")

######### this needs work 10/26 ############################
@app.route("media-info/{{ TMDB_id }}/sort-folder", methods=["POST"])
def add_movie_to_folder():
    pass
############################################################

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)