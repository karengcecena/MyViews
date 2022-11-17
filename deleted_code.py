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


# ##### ADDING MOVIE RATING
# @app.route("/media-info/movie/<TMDB_id>/rating", methods=["POST"])
# def rate_movie(TMDB_id):
#     """Sets score user input under ratings"""
    
#     score = request.form.get("score")
#     comment = request.form.get("comment")
#     movie = crud.get_media_by_TMDB_id(TMDB_id, "movie")
#     time_watched = request.form.get("watch_time")

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

#     # check if a score was input:
#     if score:   

#         # check if user is logged in: 
#         if "username" in session:
#             user_username = session["username"]
#             user = crud.get_user_by_username(user_username)

#             # check if user has rated this media before:
#             if crud.user_rated(movie, user):

#                 # update the score in db
#                 if comment: 
#                     movie_rating = crud.user_rated(movie, user)
#                     movie_rating.score = score
#                     movie_rating.review_input = comment
#                     db.session.commit()
#                     # add time watched if exists: 
#                     if time_watched:
#                         movie.time_watched = time_watched
#                         db.session.commit()
#                     flash(f"Your score has been updated to {score} and your comment was successfully added")
#                 else:
#                     movie_rating = crud.user_rated(movie, user)
#                     movie_rating.score = score
#                     db.session.commit()
#                     # add time watched if exists: 
#                     if time_watched:
#                         movie.time_watched = time_watched
#                         db.session.commit()
#                     flash(f"Your score has been updated to {score}")
#             else:
#                 # add rating to movie 
#                 rating = crud.add_rating_to_db(score, user.user_id, movie.media_id, comment)
#                 db.session.add(rating)
#                 db.session.commit()
#                 # add time watched if exists: 
#                 if time_watched:
#                     movie.time_watched = time_watched
#                     db.session.commit()
#                 flash(f"Your rating of {score} out of 5 and comment were successfully added for {movie.title}")

#                 # add movie to watched list: 
#                 if not crud.user_sorted_Watched(movie, user):
#                     # add to watched list
#                     movie_folder = crud.add_to_WatchedList(movie, user)
#                     db.session.add(movie_folder)
#                     db.session.commit()
#                     flash(f"Your media has been added to your watched list")

#         else:
#             flash("Sorry, only logged in users can rate movies")
#     else: 
#         flash("Sorry, it seems no score was selected.")

#     return redirect(f"/media-info/movie/{TMDB_id}")


# ##### ADDING SHOW RATING
# @app.route("/media-info/tv/<TMDB_id>/rating", methods=["POST"])
# def rate_show(TMDB_id):
#     """Sets score user input under ratings"""
    
#     score = request.form.get("score")
#     comment = request.form.get("comment")
#     show = crud.get_media_by_TMDB_id(TMDB_id, "tv")
#     time_watched = request.form.get("watch_time")

#     # add show to database if not in there already
#     if not show:
#         #get show information
#         url = f"https://api.themoviedb.org/3/tv/{TMDB_id}"
#         payload = {"api_key": API_KEY} 

#         res = requests.get(url, params=payload)
#         data = res.json()

#         # add show to db
#         show = crud.add_show_to_db(data)
#         db.session.add(show)
#         db.session.commit()

#         ### Note CANNOT ADD SHOW GENRE INFORMATION BC DB DOES NOT HAVE###

#     # check if a score was input:
#     if score:   

#         # check if user is logged in: 
#         if "username" in session:
#             user_username = session["username"]
#             user = crud.get_user_by_username(user_username)

#             # check if user has rated this media before:
#             if crud.user_rated(show, user):

#                 # update the score in db
#                 if comment: 
#                     show_rating = crud.user_rated(show, user)
#                     show_rating.score = score
#                     show_rating.review_input = comment
#                     db.session.commit()
#                     # add time watched if exists: 
#                     if time_watched:
#                         show.time_watched = time_watched
#                         db.session.commit()
#                     flash(f"Your score has been updated to {score} and your comment was successfully added")
#                 else:
#                     show_rating = crud.user_rated(show, user)
#                     show_rating.score = score
#                     db.session.commit()
#                     # add time watched if exists: 
#                     if time_watched:
#                         show.time_watched = time_watched
#                         db.session.commit()
#                     flash(f"Your score has been updated to {score}")
#             else:
#                 # add rating to show
#                 rating = crud.add_rating_to_db(score, user.user_id, show.media_id, comment)
#                 db.session.add(rating)
#                 db.session.commit()
#                 # add time watched if exists: 
#                 if time_watched:
#                     show.time_watched = time_watched
#                     db.session.commit()
#                 flash(f"Your rating of {score} out of 5 and comment were successfully added for {show.title}")

#                 # add movie to watched list: 
#                 if not crud.user_sorted_Watched(show, user):
#                     # add to watched list
#                     show_folder = crud.add_to_WatchedList(show, user)
#                     db.session.add(show_folder)
#                     db.session.commit()
#                     flash(f"Your show has been added to your watched list")

#         else:
#             flash("Sorry, only logged in users can rate shows")
#     else: 
#         flash("Sorry, it seems no score was selected.")

#     return redirect(f"/media-info/tv/{TMDB_id}")


##############################################################################################
# I am here

# @app.route("/movie/<TMDB_id>/sort-folder", methods=["POST"])
# def add_movie_to_folder(TMDB_id):
#     """Adds selected movie to watched or to be watched list"""

#     folder = request.form.get("list")
#     movie = crud.get_media_by_TMDB_id(TMDB_id, "movie")
#     time_watched = request.form.get("watch_time")

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

#         # add time watched if exists: 
#         if time_watched:
#             movie.time_watched = time_watched
#             db.session.commit()

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

#     # check if folder was selected:
#     if folder:
#         # check is user is logged in:
#         if "username" in session:
#             user_username = session["username"]
#             user = crud.get_user_by_username(user_username)

#             # sort into folder depending on value:
#             if folder == "watched":
                
#                 # check if user added to watched_list before:
#                 if crud.user_sorted_Watched(movie, user):
#                     flash("This movie is already in your Watched List")

#                 # check if user added to to_be_watched_list before:
#                 elif crud.user_sorted_ToBeWatched(movie, user):
#                     # delete from to_be_watched_list
#                     movie_folder = crud.user_sorted_ToBeWatched(movie, user)
#                     db.session.delete(movie_folder)
#                     db.session.commit()

#                     # add to watched list
#                     movie_folder = crud.add_to_WatchedList(movie, user)
#                     db.session.add(movie_folder)
#                     db.session.commit()
#                     flash("This movie has been switched from your To Be Watched List to your Watched List")

#                 else:
#                     # add to watched list:
#                     movie_folder = crud.add_to_WatchedList(movie, user)
#                     db.session.add(movie_folder)
#                     db.session.commit()
#                     flash("This movie has been added to your Watched List")


#             elif folder == "to_be_watched":
#                 # check if user added to to_be_watched_list before:
#                 if crud.user_sorted_ToBeWatched(movie, user):
#                     flash("This movie is already in your To Be Watched List")

#                 # check if user added to watched_list before:
#                 elif crud.user_sorted_Watched(movie, user):
#                     flash("This movie is already in your Watched List")
#                     # delete from watched_list
#                     movie_folder = crud.user_sorted_Watched(movie, user)
#                     db.session.delete(movie_folder)
#                     db.session.commit()

#                     # add to to_be_watched list
#                     movie_folder = crud.add_to_ToBeWatchedList(movie, user)
#                     db.session.add(movie_folder)
#                     db.session.commit()
#                     flash("This movie has been switched from your Watched List to your To Be Watched List")

#                 else:
#                     # add to to_be_watched list:
#                     movie_folder = crud.add_to_ToBeWatchedList(movie, user)
#                     db.session.add(movie_folder)
#                     db.session.commit()
#                     flash("This movie has been added to your Watched List")

#         else:
#             flash("Sorry, only logged in users can add movies to folders")

#     else:
#         flash("Sorry, it seems no folder was selected.")

#     return redirect(f"/media-info/movie/{TMDB_id}")



# ##### ADDING SHOW TO FOLDER WATCHED VS NOT
# @app.route("/tv/<TMDB_id>/sort-folder", methods=["POST"])
# def add_show_to_folder(TMDB_id):
#     """Adds selected show to watched or to be watched list"""

#     folder = request.form.get("list")
#     show= crud.get_media_by_TMDB_id(TMDB_id, "tv")
#     time_watched = request.form.get("watch_time")

#     # add show to database if not in there already
#     if not show:
#         #get show information
#         url = f"https://api.themoviedb.org/3/tv/{TMDB_id}"
#         payload = {"api_key": API_KEY} 

#         res = requests.get(url, params=payload)
#         data = res.json()

#         # add show to db
#         show = crud.add_show_to_db(data)
#         db.session.add(show)
#         db.session.commit()

#         # add time watched if exists: 
#         if time_watched:
#             show.time_watched = time_watched
#             db.session.commit()

#         ### Note CANNOT ADD SHOW GENRE INFORMATION BC DB DOES NOT HAVE###

#     # check if folder was selected:
#     if folder:
#         # check is user is logged in:
#         if "username" in session:
#             user_username = session["username"]
#             user = crud.get_user_by_username(user_username)

#             # sort into folder depending on value:
#             if folder == "watched":
                
#                 # check if user added to watched_list before:
#                 if crud.user_sorted_Watched(show, user):
#                     flash("This show is already in your Watched List")

#                 # check if user added to to_be_watched_list before:
#                 elif crud.user_sorted_ToBeWatched(show, user):
#                     # delete from to_be_watched_list
#                     show_folder = crud.user_sorted_ToBeWatched(show, user)
#                     db.session.delete(show_folder)
#                     db.session.commit()

#                     # add to watched list
#                     show_folder = crud.add_to_WatchedList(show, user)
#                     db.session.add(show_folder)
#                     db.session.commit()
#                     flash("This show has been switched from your To Be Watched List to your Watched List")

#                 else:
#                     # add to watched list:
#                     show_folder = crud.add_to_WatchedList(show, user)
#                     db.session.add(show_folder)
#                     db.session.commit()
#                     flash("This show has been added to your Watched List")


#             elif folder == "to_be_watched":
#                 # check if user added to to_be_watched_list before:
#                 if crud.user_sorted_ToBeWatched(show, user):
#                     flash("This show is already in your To Be Watched List")

#                 # check if user added to to be watched_list before:
#                 elif crud.user_sorted_Watched(show, user):
#                     # flash("This show is already in your Watched List")
#                     # delete from watched_list
#                     show_folder = crud.user_sorted_Watched(show, user)
#                     db.session.delete(show_folder)
#                     db.session.commit()

#                     # add to to_be_watched list
#                     show_folder = crud.add_to_ToBeWatchedList(show, user)
#                     db.session.add(show_folder)
#                     db.session.commit()
#                     flash("This show has been switched from your Watched List to your To Be Watched List")

#                 else:
#                     # add to to_be_watched list:
#                     show_folder = crud.add_to_ToBeWatchedList(show, user)
#                     db.session.add(show_folder)
#                     db.session.commit()
#                     flash("This show has been added to your To Be Watched List")

#         else:
#             flash("Sorry, only logged in users can add shows to folders")

#     else:
#         flash("Sorry, it seems no folder was selected.")

#     return redirect(f"/media-info/tv/{TMDB_id}")