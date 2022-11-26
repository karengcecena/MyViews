'use-strict';

// deleting from watched list on user profile
const deleteFromWatchedBtns = document.querySelectorAll(".deleting-from-watched-btn")

for (const deleteBtn of deleteFromWatchedBtns) {

  deleteBtn.addEventListener("click", evt => {
    console.log(deleteBtn.value)
    const formInputs  = {
          mediaID: deleteBtn.value
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

// deleting from to be watched list on user profile
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

// deleting a rating on edit list
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
      // document.querySelector('.deleting-rating-btn').classList.add("filler-btn");
      // document.querySelector('.star').classList.add("blank-star");
      });
  })
}
