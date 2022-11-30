# MyViews

## Summary 

**MyViews** is a web app that allows users and guests to search for movies and tv shows. This app is for those who love organization and sharing their recommended media with friends. Users who log in can rate the media, categorize them into playlists, see their recommended and trending tv shows and movies, as well as add friends to see their profiles as well. The user profile also contains data visualization graphs, allowing users to be more mindful of the type and amount of media they are taking in. 

## Features

Check out [MyViews](https://youtu.be/uvLiHigX4Fg) on youtube for a tutorial of its features. 



## About the Developer

MyViews was created by Karen G. Cecena. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/karengcecena).

## Technologies

**Tech Stack:**

- Python
- HTML
- Javascript
- AJAX
- JSON
- CSS
- Bootstrap
- Flask
- Jinja
- ReactJS
- Chart.JS
- PostgreSQL
- GitHub OAuth
- TMDB API


## Installation

To run MyViews:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/karengcecena/project-movie-app.git
```

Create and activate a virtual environment inside your MyViews directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Sign up to use the [TMDB API](https://developer.uber.com/docs/rides/getting-started), and the [GitHub OAuth](https://github.com/settings/applications/new). 
For more information on OAuth Implementation, check out this [article](https://testdriven.io/blog/flask-social-auth/#oauth). 

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export TMDB_KEY="YOUR_KEY_HERE"
export GITHUB_ID="YOUR_ID_HERE"
export GITHUB_SECRET="YOUR_SECRET_HERE"
export OAUTHLIB_INSECURE_TRANSPORT=1
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up the database:

```
createdb project_db
python model.py
```

Run the app:

```
python server.py
```

You can now navigate to 'localhost:5000/' to access MyViews.

## Future Additions: 

- Add books to media types
- Add individual episodes to show watch history
- Use OAuth and APIs to automatically add user watch history information