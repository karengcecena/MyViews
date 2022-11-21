'use-strict';

// deleting a playlist on user profile
const deletePlaylistBtns = document.querySelectorAll(".deleting-playlist-btn")

for (const deleteBtn of deletePlaylistBtns) {

  deleteBtn.addEventListener("click", evt => {
    const formInputs  = {
          playlistID: deleteBtn.value
          };

    fetch("/delete-playlist.json", {
              method: 'POST',
              body: JSON.stringify(formInputs),
              headers: {
                'Content-Type': 'application/json',
              },
          })

    .then((response) => response.json())
    .then((responseJson) => {
      document.querySelector(`#playlist_div_${deleteBtn.value}`).remove();
      });
  })
}

// deleting a rating on user profile
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