// creates a media card for each media
function MediaCard(props) {
    return (
      <div className="mediaCard">
        <a href={`/media-info/${props.mediaType}/${props.TMDB_id}`}>{props.title}</a>
        <br></br>
        <img src={`https://image.tmdb.org/t/p/original${props.posterPath}`} alt="" />
      </div>
    );
  }

// creates the search feature so the user can search for a media
function SearchMedia(props) {
    const [search, setSearch] = React.useState("");
    let [mediaType, setmediaType] = React.useState("");
    const [mediaCards, setmediaCards] = React.useState([]);
    
    function searchMediaInfo() {
      if (mediaType != "" && search != ""){
        
        fetch("/media-search-results-react.json", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ search, mediaType })
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
            mediaType={`${mediaType}`}
            TMDB_id={currentmediaCard["id"]}
        />,
        );
    }
    };

    return (
        <React.Fragment>
            <nav>
              <ul>
                  <li class="medialogo">MyViews</li>
                  {/* <li><a href="/">Home</a></li> */}
                  <li><a class="active" href="/media-search-results-react">Search</a></li>
                  <li><a href="/user-profile">Profile</a></li>
                  <li><a href="/search-friends">Friends</a></li>
                  <li><a href="/logout">Logout</a></li>
                </ul>
            </nav>
            <div>
              <h1> Search a movie or tv show by title using the search bar below: using REACT!!! </h1>
              <label htmlFor="searchInput"></label>
                  <input
                      name="search"
                      onChange={(event) => setSearch(event.target.value)}
                      id="searchInput"
                  ></input>
              <label htmlFor="movieInput">
                  <input
                    type="radio"
                    value="movie"
                    name="mediaType"
                    onChange={(event) => mediaType = event.target.value}
                    id="movieInput"
                  /> movie 
                </label>
                <label htmlFor="showInput">
                  <input
                    type="radio"
                    value="tv"
                    name="mediaType"
                    onChange={(event) => mediaType = event.target.value}
                    id="showInput"
                    /> tv show 
                </label>
                <button onClick={searchMediaInfo}>
                    Search
                </button>
            </div>
            <div className="grid">{mediaCardsList}</div>
        </React.Fragment>
    );
    };

ReactDOM.render(<SearchMedia/>, document.getElementById('container'));