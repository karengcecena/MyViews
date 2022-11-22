'use-strict';

// deleting from a playlist

const deleteFromPlaylistBtns = document.querySelectorAll(".deleting-from-playlist-btn")

for (const deleteBtn of deleteFromPlaylistBtns) {

  deleteBtn.addEventListener("click", evt => {
    console.log(deleteBtn)
    const formInputs  = {
          mediaID: deleteBtn.value,
          playlistID: document.querySelector("#playlist_id").value,
          };

    fetch(`/user-profile/delete-from-playlist.json`, {
              method: 'POST',
              body: JSON.stringify(formInputs),
              headers: {
                'Content-Type': 'application/json',
              },
          })

    .then((response) => response.json())
    .then((responseJson) => {
      document.querySelector(`#playlist_media_div_${deleteBtn.value}`).remove();
      });
  })
}

// deleting a rating on edit playlist
const deleteRatingBtns = document.querySelectorAll(".deleting-rating-btn")

for (const deleteBtn of deleteRatingBtns) {

  deleteBtn.addEventListener("click", evt => {
    const formInputs  = {
          ratingID: deleteBtn.value
          };

    fetch("/delete-rating.json", {
              method: 'POST',
              body: JSON.stringify(formInputs),
              headers: {
                'Content-Type': 'application/json',
              },
          })

    .then((response) => response.json())
    .then((responseJson) => {
      document.querySelector(`#rating_div_${deleteBtn.value}`).remove();
      });
  })
}