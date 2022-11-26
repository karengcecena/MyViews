// creates a media card for each media
function MediaCard(props) {
    return (
      <div className="media_card text-center">
        <br></br>
        <div class="media_title"><a className="media_title" href={`/media-info/${props.mediaType}/${props.TMDB_id}`}>{props.title}</a></div>
        <br></br>
        <div class="media_poster_path"><img src={`https://image.tmdb.org/t/p/original${props.posterPath}`} alt="No Poster Path Available"/></div>
      </div>
    );
  }

// creates the search feature so the user can search for a media
function SearchMedia(props) {
    const [search, setSearch] = React.useState("");
    const [mediaType, setmediaType] = React.useState("");
    const [mediaCards, setmediaCards] = React.useState([]);
    const [mediaTypeToSearch, setMediaTypeToSearch] = React.useState("");
    
    function searchMediaInfo() {
      console.log(mediaTypeToSearch)
      console.log(search)
      if (mediaTypeToSearch != "" && search != ""){

        fetch("/media-search-results-react.json", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ "search": search, "mediaType": mediaTypeToSearch })
        })
          // data returned from fetch request
          .then((response) => response.json())
          .then((mediaCardsData) => {
            setmediaCards(mediaCardsData.media)
            setmediaType(mediaCardsData.media_type)
          });

      }   
    };

    const mediaCardsList = [];

    if (mediaType == "movie"){
      for (const currentmediaCard of mediaCards) {
        mediaCardsList.push(
        <MediaCard
            key={currentmediaCard["id"]}
            title={currentmediaCard["original_title"]}
            posterPath={currentmediaCard['poster_path']}
            mediaType={mediaType}
            TMDB_id={currentmediaCard["id"]}
        />,
        );
    }
    } else if (mediaType == "tv"){
      for (const currentmediaCard of mediaCards) {
        mediaCardsList.push(
        <MediaCard
            key={currentmediaCard["id"]}
            title={currentmediaCard["name"]}
            posterPath={currentmediaCard['poster_path']}
            mediaType={mediaType}
            TMDB_id={currentmediaCard["id"]}
        />,
        );
    }
    };

    return (
        <React.Fragment>
            <nav>
              <ul>
                  <li><a href="/">MyViews</a></li>
                  <li><a class="active" href="/media-search-results-react">Search</a></li>
                  <li><a href="/user-profile">Profile</a></li>
                  <li><a href="/search-friends">Friends</a></li>
                  <li><a href="/recommended">Your Recommended</a></li>
                  <li><a href="/logout">Logout</a></li>
                </ul>
            </nav>
            <div class="container-flex">
              <div class="container search_page">
                <div class="row search_page_row">
                  <div class="search_bar text-center">
                    <label htmlFor="searchInput"><h1 id="search_title"> Search by title:</h1></label>
                        <input
                            name="search"
                            onChange={(event) => setSearch(event.target.value)}
                            id="searchInput"
                        ></input>
                    <label htmlFor="movieInput">
                        <input
                          type="radio"
                          value="movie"
                          name="mediaTypeToSearch"
                          onChange={(event) => setMediaTypeToSearch(event.target.value)}
                          id="movieInput"
                        /> movie 
                      </label>
                      <label htmlFor="showInput">
                        <input
                          type="radio"
                          value="tv"
                          name="mediaTypeToSearch"
                          onChange={(event) => setMediaTypeToSearch(event.target.value)}
                          id="showInput"
                          /> tv show 
                      </label>
                      <button onClick={searchMediaInfo}>
                          Search
                      </button>
                  </div>
                  </div>
                  <div className="grid">{mediaCardsList}</div>
                </div>
            </div>
        </React.Fragment>
    );
    };

ReactDOM.render(<SearchMedia/>, document.getElementById('container'));