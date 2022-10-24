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

@app.route("/login")
def login_user():
    """Logs in the user"""

    redirect("user_profile.html")

@app.route("/register-user")
def register_user():
    """Gets info input in create user page and registers user"""
    pass

    redirect("/login")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)