'use-strict';

// deleting a rating 
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