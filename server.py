"""Server for movie app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
import os

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "forsession"
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ['TMDB_KEY']

@app.route("/")
def homepage():
    """Displays homepage"""

    return render_template("homepage.html")

@app.route("/media")
def show_media():
    """Shows all media"""

    return render_template("all_media.html")

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
            # could I have both?
            session["username"] = user.username
            # session['email'] = email
            flash("You have successfully logged in")
            return redirect ("/user-profile")
        else:
            flash("Your password was incorrect. Please try again.")

    else:
        flash("Sorry, a user with that email doesn't exist")

    return redirect("/")

@app.route("/user-profile")
def display_user_profile():
    user_email = session["username"]
    user = crud.get_user_by_email(user_email)

    return render_template("user_profile.html", user=user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)