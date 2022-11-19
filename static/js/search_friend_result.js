'use-strict';

// following btn AJAX

const followBtn = document.querySelector("#follow-btn")
if (followBtn) {
  followBtn.addEventListener("click", evt => {
    
    const formInputs  = {
          action: followBtn.innerText,
          user2ID: document.querySelector("#user2_id").value,
          };

    fetch("/friend/follow-status.js", {
              method: 'POST',
              body: JSON.stringify(formInputs),
              headers: {
                'Content-Type': 'application/json',
              },
          })

    .then((response) => response.json())
    .then((responseJson) => {
        if (followBtn.innerText == "Unfollow"){
            document.querySelector("#follow-btn").innerText = "Follow";

        } else if (followBtn.innerText == "Follow"){
            document.querySelector("#follow-btn").innerText = "Unfollow";
        }   
      });
  })
}

  // unfollowing btn AJAX

const unfollowBtn = document.querySelector("#unfollow-btn")
if (unfollowBtn) {
  unfollowBtn.addEventListener("click", evt => {
    
    const formInputs  = {
            action: unfollowBtn.innerText,
            user2ID: document.querySelector("#user2_id").value,
            };

    fetch("/friend/follow-status.js", {
                method: 'POST',
                body: JSON.stringify(formInputs),
                headers: {
                'Content-Type': 'application/json',
                },
            })

    .then((response) => response.json())
    .then((responseJson) => {
        if (unfollowBtn.innerText == "Unfollow"){
            document.querySelector("#unfollow-btn").innerText = "Follow";
        } else if (unfollowBtn.innerText == "Follow"){
            document.querySelector("#unfollow-btn").innerText = "Unfollow";
        }   
        });
    })
}