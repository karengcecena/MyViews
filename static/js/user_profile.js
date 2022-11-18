'use-strict';

// deleting from watched list
const deleteFromWatchedBtns = document.querySelectorAll(".deleting-from-watched-btn")

for (const deleteBtn of deleteFromWatchedBtns) {

  deleteBtn.addEventListener("click", evt => {
    console.log(deleteBtn.value)
    const formInputs  = {
          mediaID: deleteBtn.value
            // mediaID : document.querySelector('#delete-from-watched-list').value,
          };

    fetch("/user-profile/delete-from-watched-list.json", {
              method: 'POST',
              body: JSON.stringify(formInputs),
              headers: {
                'Content-Type': 'application/json',
              },
          })

    .then((response) => response.json())
    .then((responseJson) => {
      document.querySelector(`#watch_list_div_${deleteBtn.value}`).remove();
      });
  })
}

// deleting from to be watched list
const deleteFromToBeWatchedBtns = document.querySelectorAll(".deleting-from-to-be-watched-btn")

for (const deleteBtn of deleteFromToBeWatchedBtns) {

  deleteBtn.addEventListener("click", evt => {
    const formInputs  = {
          mediaID: deleteBtn.value
          };

    fetch("/user-profile/delete-from-to-be-watched-list.json", {
              method: 'POST',
              body: JSON.stringify(formInputs),
              headers: {
                'Content-Type': 'application/json',
              },
          })

    .then((response) => response.json())
    .then((responseJson) => {
      document.querySelector(`#to_be_watch_list_div_${deleteBtn.value}`).remove();
      });
  })
}



// deleting a playlist 
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


// deleting a rating 
const deleteRatingBtns = document.querySelectorAll(".deleting-rating-btn")

for (const deleteBtn of deleteRatingBtns) {

  deleteBtn.addEventListener("click", evt => {
    const formInputs  = {
          ratingID: deleteBtn.value
          };

    fetch("/media-info/delete-rating.json", {
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

// deleting from a playlist

// const deleteFromPlaylistBtns = document.querySelectorAll(".deleting-from-playlist-btn")

// for (const deleteBtn of deleteFromPlaylistBtns) {

//   deleteBtn.addEventListener("click", evt => {
//     const formInputs  = {
//           mediaID: deleteBtn.value
//           // playlistID: document.querySelector("#playlist__div_{{ playlist.playlist_id }}")
//           };

//     fetch(`/user-profile/delete-from/${playlist.playlist_id}.json`, {
//               method: 'POST',
//               body: JSON.stringify(formInputs),
//               headers: {
//                 'Content-Type': 'application/json',
//               },
//           })

//     .then((response) => response.json())
//     .then((responseJson) => {
//       document.querySelector(`#playlist_media_div_${deleteBtn.value}`).remove();
//       });
//   })
// }




// before steve showed me the other stuff

// document.querySelector("#create_playlist_form").addEventListener("submit", evt => {
//     evt.preventDefault();

//     const formInputs  = {
//       playlistName : document.querySelector('#playlist_name_field').value,
//     };
  
//     console.log(playlist_name)

//     fetch("/create-playlist.json", {
//         method: 'POST',
//         body: JSON.stringify(formInputs),
//         headers: {
//           'Content-Type': 'application/json',
//         },
//     })
//         // .then((response) => response.json())
//         // .then((responseJson) => {
//         //     alert(responseJson.success);
//         // });
// })

// const addplaylistbtn = document.querySelector("#playlistadd").addEventListener("submit", evt => {
//   evt.preventDefault();

//   const playlist_name = document.querySelector('#playlist_name_field').value;

//     console.log(playlist_name)

//     fetch("/create-playlist.json", {
//         method: 'POST',
//         body: JSON.stringify(playlist_name),
//         headers: {
//           'Content-Type': 'application/json',
//         },
//     })
// })