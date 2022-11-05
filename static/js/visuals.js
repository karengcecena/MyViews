'use strict';

fetch('/user-profile/genres.json')
.then(response => response.json())
.then(responseJson => {

  const xvalues = [];
  const yvalues = [];
  
  // set colors
  const barColors = [
      "#b91d47",
      "#00aba9",
      "#2b5797",
      "#e8c3b9",
      "#1e7145"
    ];

  const barColorsDynamic = [];
  
  for (const value of responseJson.data){
    xvalues.push(value["genre"]);
    yvalues.push(value["number_of_genre"]);
  }
  
  // dynamically generated colors
  // adapted from user comment on 
  // https://stackoverflow.com/questions/45771849/chartjs-random-colors-for-each-part-of-pie-chart-with-data-dynamically-from-data
  const dynamicColors = () => {

    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);
    return "rgb(" + r + "," + g + "," + b + ")";
  };

  for (let i =0; i<(xvalues.length); i++){
    barColorsDynamic.push(dynamicColors());
  }

  console.log(barColors)

  new Chart(document.querySelector('#test-chart'), {
    type: 'doughnut',

    data: {
      labels: xvalues,
      datasets: [{
        // backgroundColor: barColors,
        backgroundColor: barColorsDynamic,
        data: yvalues
      }]
    },

    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Your Movie Watched List Genres:'
        }
      }
    },
  });

});


// ################## CODE BELOW I AM UNSURE OF ###########################################################################
// friend profile genres (not sure yet): 

// fetch('/friend/genres.json')
// .then(response => response.json())
// .then(responseJson => {

//   const xvalues = [];
//   const yvalues = [];
  
//   // set colors
//   const barColors = [
//       "#b91d47",
//       "#00aba9",
//       "#2b5797",
//       "#e8c3b9",
//       "#1e7145"
//     ];

//   const barColorsDynamic = [];
  
//   for (const value of responseJson.data){
//     xvalues.push(value["genre"]);
//     yvalues.push(value["number_of_genre"]);
//   }
  
//   // dynamically generated colors
//   // adapted from user comment on 
//   // https://stackoverflow.com/questions/45771849/chartjs-random-colors-for-each-part-of-pie-chart-with-data-dynamically-from-data
//   const dynamicColors = () => {

//     const r = Math.floor(Math.random() * 255);
//     const g = Math.floor(Math.random() * 255);
//     const b = Math.floor(Math.random() * 255);
//     return "rgb(" + r + "," + g + "," + b + ")";
//   };

//   for (let i =0; i<(xvalues.length); i++){
//     barColorsDynamic.push(dynamicColors());
//   }

//   console.log(barColors)

//   new Chart(document.querySelector('#friend-chart'), {
//     type: 'doughnut',

//     data: {
//       labels: xvalues,
//       datasets: [{
//         // backgroundColor: barColors,
//         backgroundColor: barColorsDynamic,
//         data: yvalues
//       }]
//     },

//     options: {
//       responsive: true,
//       plugins: {
//         legend: {
//           position: 'top',
//         },
//         title: {
//           display: true,
//           text: 'Users Watched List Genres:'
//         }
//       }
//     },
//   });

// });