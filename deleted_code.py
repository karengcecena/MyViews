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


#### MOVIE AND TV SHOWS SEPARATED BELOW IN DIFFERENT ROUTES BECAUSE OF REPEATED TMDB_ID's ####
# # Before Code Consolidation:    

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



# ##### ADDING MOVIE TO PLAYLIST
# @app.route("/movie/<TMDB_id>/add-to-playlist", methods=["POST"])
# def add_movie_to_playlist(TMDB_id):
#     """Adds movie to selected playlist"""
#     movie = crud.get_media_by_TMDB_id(TMDB_id, "movie")
#     playlist_id = request.form.get("playlist")
#     user_username = session["username"]
#     user = crud.get_user_by_username(user_username)

#     # add movie to database if not in there already
#     if not movie:
#         #get movie information
#         url = f"https://api.themoviedb.org/3/movie/{TMDB_id}"
#         payload = {"api_key": API_KEY} 

#         res = requests.get(url, params=payload)
#         data = res.json()

#         # add movie to db
#         movie = crud.add_movie_to_db(data)
#         db.session.add(movie)
#         db.session.commit()

#         ### ADDING MOVIE GENRE INFORMATION ###
#         # add genres to movie that do not exist:
#         genres = data["genres"]
#         for genre in genres:
#             # check if genre in genres:
#             if crud.check_if_genre_in_db(genre):
#                 # if yes: 
#                 genre = crud.check_if_genre_in_db(genre)
#                 movie.genres.append(genre)
#                 db.session.commit()
#             else:
#                 # if not, add to genre:
#                 genre = crud.add_genre_to_db(genre)
#                 db.session.add(genre)
#                 movie.genres.append(genre)
#                 db.session.commit()

#     # add show to playlist
#     if playlist_id != "no":
#         playlist = crud.get_playlist_by_id(playlist_id, user)
#         movie.playlists.append(playlist)
#         db.session.commit()
#         flash(f"Movie successfully added to {playlist.name}")
#         return redirect (f"/media-info/movie/{TMDB_id}")
#     else:
#         flash("Please log in")


# ##### ADDING SHOW TO PLAYLIST
# @app.route("/tv/<TMDB_id>/add-to-playlist", methods=["POST"])
# def add_show_to_playlist(TMDB_id):
#     """Adds show to selected playlist"""
#     show = crud.get_media_by_TMDB_id(TMDB_id, "tv")
#     playlist_id = request.form.get("playlist")
 
#     user_username = session["username"]
#     user = crud.get_user_by_username(user_username)

#     # add show to database if not in there already
#     if not show:
#         #get show information
#         url = f"https://api.themoviedb.org/3/tv/{TMDB_id}"
#         payload = {"api_key": API_KEY} 

#         res = requests.get(url, params=payload)
#         data = res.json()

#         # add show to db
#         show = crud.add_show_to_db(data)
#         db.session.add(movie)
#         db.session.commit()

#         ### Note CANNOT ADD SHOW GENRE INFORMATION BC DB DOES NOT HAVE###

#     # add to playlist
#     if playlist_id != "no":
#         playlist = crud.get_playlist_by_id(playlist_id, user)
#         show.playlists.append(playlist)
#         db.session.commit()
#         flash(f"Show successfully added to {playlist.name}")
#         return redirect (f"/media-info/tv/{TMDB_id}")
#     else:
#         flash("Please log in")

