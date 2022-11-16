# Before Create User Pop-Up
# @app.route("/create-user")
# def display_create_user():
#     """Shows the create user page"""

#     return render_template("create_user.html")


# Code for search page before React
# @app.route("/media-search-results", methods=["POST"])
# def show_search_results():
#     "Displays results from search bar query"

#     search_text = request.form.get("title")
#     media_type = request.form.get("media_type")

#     #for movies: 
#     if media_type == "movie":
#         url = "https://api.themoviedb.org/3/search/movie"

#     #for tv shows:
#     elif media_type == "show":
#         url = "https://api.themoviedb.org/3/search/tv"
#     payload = {"api_key": API_KEY} 

#     # add media title to payload
#     if search_text:
#         payload["query"]=search_text

#     res = requests.get(url, params=payload)
#     data = res.json()

#     results = data['results']

#     return render_template("all_media.html", data=data, search_text=search_text, results=results, res=res, media_type=media_type)


# Before Code Consolidation: 

# #for movie media_info 
# @app.route("/media-info/movie/<TMDB_id>")
# def show_movie(TMDB_id):
#     """Shows specific movie information for selected movie"""

#     #get media information
#     # for movie: 
#     url = f"https://api.themoviedb.org/3/movie/{TMDB_id}"

#     #for tv show: 
#     payload = {"api_key": API_KEY} 

#     res = requests.get(url, params=payload)
#     data = res.json()
    
#     # filter for that movies ratings in db to display on media page
#     if crud.get_media_by_TMDB_id(TMDB_id, "movie"):
#         movie = crud.get_media_by_TMDB_id(TMDB_id, "movie")
#         movie_id = movie.media_id
#         all_ratings = crud.get_all_ratings(movie_id)

#     else: 
#         all_ratings = False

#     # check if user is logged in in order to display playlists correctly 
#     if "username" in session:
#         user = crud.get_user_by_username(session["username"])
#         return render_template("media_information.html", data=data, TMDB_id=TMDB_id, user=user, media_type="movie", all_ratings=all_ratings)

#     else:
#         return render_template("media_information.html", data=data, TMDB_id=TMDB_id, user=False, media_type="movie", all_ratings=all_ratings)

# #for tv show media_info 
# @app.route("/media-info/tvshow/<TMDB_id>")
# def show_tv_show(TMDB_id):
#     """Shows specific tv show information for selected tv show"""

#     #get media information
#     # for movie: 
#     url = f"https://api.themoviedb.org/3/tv/{TMDB_id}"

#     #for tv show: 
#     payload = {"api_key": API_KEY} 

#     res = requests.get(url, params=payload)
#     data = res.json()

#     # filter for that tv shows ratings in db to display on media page
#     if crud.get_media_by_TMDB_id(TMDB_id, "show"):
#         show = crud.get_media_by_TMDB_id(TMDB_id, "show")
#         show_id = show.media_id
#         all_ratings = crud.get_all_ratings(show_id)

#     else: 
#         all_ratings = False

#     # check if user is logged in in order to display playlists correctly 
#     if "username" in session:
#         user = crud.get_user_by_username(session["username"])
#         return render_template("media_information.html", data=data, TMDB_id=TMDB_id, user=user, media_type="show", all_ratings=all_ratings)

#     else:
#         return render_template("media_information.html", data=data, TMDB_id=TMDB_id, user=False, media_type="show", all_ratings=all_ratings)