'use strict';

// for genres

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

  // console.log(barColors)

  new Chart(document.querySelector('#genre-chart'), {
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
          labels: {
            color: 'white',
            font: {family: 'Lucida Console', size: 15 }
          }
        },
        title: {
          display: true,
          text: 'Your Movie Watched List Genres:',
          color: 'white',
          font: {
            family: 'Lucida Console', 
            size: 20 
          }
        }
      }
    },
  });

});

// for watch history

fetch('/user-profile/watch_history.json')
  .then(response => response.json())
  .then(responseJson => {

    let movievalues = [];
    let showvalues = [];
  
  
    for (const movie_value of responseJson.moviedata){
        movievalues.push({
          // x: movie_value["day"],
          x: movie_value["month"],
          y: movie_value["number_of_movies"]
        })
       
    };

    for (const show_value of responseJson.showdata){
      showvalues.push({
        // x: show_value["day"],
        x: show_value["month"],
        y: show_value["number_of_shows"]
      })
    };

    console.log(movievalues)
    console.log(showvalues)

    new Chart(document.querySelector('#watch-history-chart'), {
      type: 'bar',
      data: {
        datasets: [{
          label: "Movies",
          data: movievalues,
          fill: false,
          backgroundColor: 'rgb(186, 85, 211)',
          // borderColor: 'rgb(186, 85, 211)',
          // tension: 0.1
        },
        {
            label: "TV Shows",
            data: showvalues,
            fill: false,
            backgroundColor: 'rgb(75, 192, 75)',
            // borderColor: 'rgb(75, 192, 75)',
            // tension: 0.1
          },
        ],
      },

      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              min:0,
              stepSize: 1,
              color: 'white',
            },
            grid: {
              color: 'white',
              borderColor: 'white',
              tickColor: 'white'
            },
          },
          x: {
            type: 'time',
            time: {
              tooltipFormat: 'LLLL dd', // Luxon format string
              unit: 'month',
            },
            grid: {
              color: 'white',
              borderColor: 'white',
              tickColor: 'white',
            },
            ticks: {
              color: 'white',
            },
          },
        },
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: 'white',
              font: {family: 'Lucida Console', size: 15 }
            }
          },
          title: {
            display: true,
            text: 'Your Watched List History:',
            color: 'white',
            font: {family: 'Lucida Console', size: 20 }
          }
        }
      }
  });
});