
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
    var myDropdown = document.getElementById("myDropdown");
      if (myDropdown.classList.contains('show')) {
        myDropdown.classList.remove('show');
      }
  }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){

    jQuery.noConflict();
    setInterval(function() {
        jQuery.ajax({
    //           async: false,
               type: "POST",
               url: "/index/get_flight_status/",
               data: {
                   'csrfmiddlewaretoken' : getCookie('csrftoken')
               },
           })
           .done(function(response) {
                var do_message = response.do_message;
                if (do_message)
                {
                    if (response.is_takeoff)
                    {
                        swal('drone ' + response.drone_id + ' is taking off', {
                          buttons: {
                            cancel: "Close",
                            catch: {
                              text: "Go To Flight Screen",
                              value: "go_to_flight",
                            },
                          },
                        })
                        .then((value) => {
                          switch (value) {

                            case "go_to_flight":
                              window.open("http://127.0.0.1:8000/flight_monitor/","_self")
                              break;

                            default:

                          }
                        });
                    }
                    else
                    {
                        swal('drone ' + response.drone_id + ' has landed', {
                          buttons: {
                            cancel: "Close",
                            catch: {
                              text: "Go To Flight Screen",
                              value: "go_to_flight",
                            },
                          },
                        })
                        .then((value) => {
                          switch (value) {

                            case "go_to_flight":
                              window.open("http://127.0.0.1:8000/flight_monitor/","_self")
                              break;

                            default:

                          }
                        });
                    }
                }
        });
    }, 1000)
});

var backgroundColor = 'white';
Chart.plugins.register({
    beforeDraw: function(c) {
        var ctx1 = c.chart.ctx;
        ctx1.fillStyle = backgroundColor;
        ctx1.fillRect(0, 0, c.chart.width, c.chart.height);
    }
});

function get_flights_per_drone()
{
    jQuery.ajax({
           async: false,
           type: "POST",
           url: "/reviews/get_flights_per_drone/",
           data: {
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            console.log(response)
            var ids = response.ids;
            var counters = response.counters;
            var ctx = document.getElementById("FlightsPerDroneChart").getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: response.ids,
                    datasets: [{
                        label: '# of flights per drone',
                        data: response.counters,
                        backgroundColor: response.background_colors,
                        borderColor: response.border_colors,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            });
            $("#modalFlightsPerDronePopUp").modal('show');
       });
}

function saveFlightsPerDroneImage() {
    $("#FlightsPerDroneChart").get(0).toBlob(function(blob) {
        saveAs(blob, "flightsPerDrone.png");
    });
}

function get_errors_per_drone()
{
    $.ajax({
           async: false,
           type: "POST",
           url: "/reviews/get_errors_per_drone/",
           data: {
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            console.log(response)
            var ids = response.ids;
            var counters = response.counters;
            var ctx = document.getElementById("ErrorsPerDroneChart").getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: response.ids,
                    datasets: [{
                        label: '# of errors per drone',
                        data: response.counters,
                        backgroundColor: response.background_colors,
                        borderColor: response.border_colors,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            });
            $("#modalErrorsPerDronePopUp").modal('show');
       });
}

function saveErrorsPerDroneImage() {
    $("#ErrorsPerDroneChart").get(0).toBlob(function(blob) {
        saveAs(blob, "errorsPerDrone.png");
    });
}


function get_all_errors()
{
    $.ajax({
           async: false,
           type: "POST",
           url: "/reviews/get_all_errors/",
           data: {
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            console.log(response)
            var errors = response.errors;
            var counters = response.counters;
            var ctx = document.getElementById("AllErrorsChart").getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: response.errors,
                    datasets: [{
                        label: 'divergent of errors',
                        data: response.counters,
                        backgroundColor: response.background_colors,
                        borderColor: response.border_colors,
                        borderWidth: 1
                    }]
                },
                options: {
                    tooltips: {
                      callbacks: {
                        label: function(tooltipItem, data) {
                          //get the concerned dataset
                          var dataset = data.datasets[tooltipItem.datasetIndex];
                          //calculate the total of this data set
                          var total = dataset.data.reduce(function(previousValue, currentValue, currentIndex, array) {
                            return previousValue + currentValue;
                          });
                          //get the current items value
                          var currentValue = dataset.data[tooltipItem.index];
                          //calculate the precentage based on the total and current item, also this does a rough rounding to give a whole number
                          var precentage = Math.floor(((currentValue/total) * 100)+0.5);

                          return precentage + "%";
                        }
                      }
                    }
                }
            });
            $("#modalAllErrorsPopUp").modal('show');
       });
}

function saveAllErrorsImage() {
    $("#AllErrorsChart").get(0).toBlob(function(blob) {
        saveAs(blob, "allErrors.png");
    });
}

function get_flights_per_month()
{
    $.ajax({
           async: false,
           type: "POST",
           url: "/reviews/get_flights_per_month/",
           data: {
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            var ctx = document.getElementById("FlightsPerMonthChart").getContext('2d');
            myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                    datasets: [{
                        label: '# of flights per month',
                        data: response.counters,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                             'rgba(54, 162, 235, 0.2)',
                             'rgba(255, 206, 86, 0.2)',
                             'rgba(75, 192, 192, 0.2)',
                             'rgba(153, 102, 255, 0.2)',
                             'rgba(255, 159, 64, 0.2)',
                             'rgba(255, 99, 132, 0.2)',
                             'rgba(54, 162, 235, 0.2)',
                             'rgba(255, 206, 86, 0.2)',
                             'rgba(75, 192, 192, 0.2)',
                             'rgba(153, 102, 255, 0.2)',
                             'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                             'rgba(54, 162, 235, 1)',
                             'rgba(255, 206, 86, 1)',
                             'rgba(75, 192, 192, 1)',
                             'rgba(153, 102, 255, 1)',
                             'rgba(255, 159, 64, 1)',
                             'rgba(255, 99, 132, 1)',
                             'rgba(54, 162, 235, 1)',
                             'rgba(255, 206, 86, 1)',
                             'rgba(75, 192, 192, 1)',
                             'rgba(153, 102, 255, 1)',
                             'rgba(255, 159, 64, 1)',
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            });
            $("#flightsPerMonthPopUp").modal('show');
       });
}

function saveFlightsPerMonthImage() {
    $("#FlightsPerMonthChart").get(0).toBlob(function(blob) {
        saveAs(blob, "flightsPerMonth.png");
    });
}

function get_errors_per_month()
{
    $.ajax({
           async: false,
           type: "POST",
           url: "/reviews/get_errors_per_month/",
           data: {
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            ctx = document.getElementById("ErrorsPerMonthChart").getContext('2d');
            myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                    datasets: [{
                        label: '# of errors per month',
                        data: response.counters,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                             'rgba(54, 162, 235, 0.2)',
                             'rgba(255, 206, 86, 0.2)',
                             'rgba(75, 192, 192, 0.2)',
                             'rgba(153, 102, 255, 0.2)',
                             'rgba(255, 159, 64, 0.2)',
                             'rgba(255, 99, 132, 0.2)',
                             'rgba(54, 162, 235, 0.2)',
                             'rgba(255, 206, 86, 0.2)',
                             'rgba(75, 192, 192, 0.2)',
                             'rgba(153, 102, 255, 0.2)',
                             'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                             'rgba(54, 162, 235, 1)',
                             'rgba(255, 206, 86, 1)',
                             'rgba(75, 192, 192, 1)',
                             'rgba(153, 102, 255, 1)',
                             'rgba(255, 159, 64, 1)',
                             'rgba(255, 99, 132, 1)',
                             'rgba(54, 162, 235, 1)',
                             'rgba(255, 206, 86, 1)',
                             'rgba(75, 192, 192, 1)',
                             'rgba(153, 102, 255, 1)',
                             'rgba(255, 159, 64, 1)',
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            });
            $("#errorsPerMonthPopUp").modal('show');
       });
}

function saveErrorsPerMonthtImage() {
    $("#ErrorsPerMonthChart").get(0).toBlob(function(blob) {
        saveAs(blob, "errorsPerMonth.png");
    });
}


