# 🎬 MyViews

## 📖 Summary 

**MyViews** is a web app that allows users and guests to search for movies and tv shows. This app is for those who love organization and sharing their recommended media with friends. Users who log in can rate the media, categorize them into playlists, see their recommended and trending tv shows and movies, as well as add friends to see their profiles as well. The user profile also contains data visualization graphs, allowing users to be more mindful of the type and amount of media they are taking in. 

## 📋 Content
* [Deployment](#deployment)
* [About the Developer](#aboutme)
* [Tech Stack](#technologies)
* [Database Model](#databasemodel)
* [Features](#features)
* [Future Additions](#futureadditions)
* [Installation](#installation)


## 🌐 <a name="deployment"></a>Deployment

Deployed using AWS Lightsail.

Check out MyViews' [Website](http://myviews.link/)

Or check out [MyViews](https://youtu.be/uvLiHigX4Fg) on youtube for a tutorial of its features. 


## 🪐 <a name="aboutme"></a>About the Developer

MyViews was created by Karen G. Cecena. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/karengcecena).


## 💻 <a name="technologies"></a>Technologies

**Tech Stack:**

- Python
- Flask
- PostgreSQL
- JavaScript ES6+ (AJAX, JSON)
- React
- HTML5
- CSS3
- Bootstrap
- Jinja
- TMDB API
- Chart.js
- GitHub OAuth


## 🗂️ <a name="databasemodel"></a>Database Model

![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/MyViewsDataModel.jpeg "MyViews Database Model")


## 🔍 <a name="features"></a>Features

![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/login_screenshot.png "MyViews Login")

A user can log in via creating an account or logging in with GitHub. Creating an account uses password hashing to maintain user security and RegEx to ensure email formatting. Logging in with GitHub uses GitHub OAuth 2.0 to improve security and facilitate user authentication. 


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/user_profile_graphs_screenshot.png "MyViews Profile Page Graphs")

On a user’s profile, I implemented two graphs, a donut and bar graph, using ChartJS. The left one queries the database using SQLAlchemy to display the genre name and amount of times it appears in a user's watch history. The right one queries the database for watch history information in a users watch lists, and categorizes it by month. 


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/user_profile_lists_screenshot.png "MyViews Profile Create Playlists / Watched List & To Be Watch List")

Users have two default playlists to which they can add media to.


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/edit_watched_list_screenshot.png "MyViews Profile Edit Watched List")

Users can edit each individual list, as well as delete media ratings in their watched and to be watched list. Both of these features use AJAX which allows users to delete reviews/ media without reloading the entire page, increasing user experience


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/user_profile_custom_playlists.png "MyViews Profile Playlists")

Users can also create, edit, and delete custom made playlists. 


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/user_profile_friends_watched_lists_screenshot.png "MyViews Profile Friend Watched Lists")

After adding a friend, the user can see that friends' watch lists on their profile as well as their ratings on other medias. 


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/friend_profile_screenshot.png "MyViews Friends Profile'")

To add a new friend, a follow button was implemented under the friends username that also uses AJAX


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/search_page_screenshot.png "MyViews Search Page")

The search feature uses the TMDB API to populate the page with either movies or tv shows results. For a greater learning experience, I re-implemented the search page using REACT. 


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/media_info_screenshot.png "MyViews Media Info")

Media display poster path and overview, as well as the option to rate media or add them to their lists if they are logged in. 


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/add_rating_screenshot.png "MyViews Add Rating")

If a user is logged in, they can rate a movie and leave a comment, as well as input the day they watched it. The movie and rating are then added to the PostgreSQL database. This reduces the API calls for the users profile, increasing web app speed. 


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/media_info_rating_screenshot.png "MyViews Displayed Ratings")

Ratings are displayed underneath media so that users can see if their friends have rated them before. Ratings can also be seen on profiles. 

![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/add_to_lists_screenshot.png "MyViews Add to Lists")

When a user rates a movie or tv show, it is automatically added to the user’s watch list. They can also add a movie or tv show to their watch list without rating it or add media they would like to watch in the future to their to be watched list or custom playlists.


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/add_to_playlist_screenshot.png "MyViews Add to Playlists")

This is how users can add new media to their playlists. 


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/media_recommendations_screenshot.png "MyViews Movie & Show Recommendations")

For users that are logged in, their watch list media is queried using SQLAlchemy to retrieve that last movie and tv show they watched to give the user movie and tv show recommendations. 


![alt text](https://github.com/karengcecena/project-movie-app/blob/main/static/img/trending_media_screenshot.png "MyViews Trending Movies & Shows")

Both users and guests can see the current trending media 


## ⌨️ <a name="futureadditions"></a>Future Additions 

- Add books to media types
- Add individual episodes to show watch history
- Use OAuth and APIs to automatically add user watch history information


## ⚙️ <a name="installation"></a>Installation

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


