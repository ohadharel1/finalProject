
$(document).ready(function(){
    jQuery.noConflict();
});


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

function sort_results(key, value)
{
   jQuery.noConflict();
   if (value == 'Drone ID' || value == 'Status' || value == 'Start Time' || value == 'End Time' || value == 'Duration')
       {
            return
       }
   console.log('key: ' + key);
   console.log('value: ' + value);
   $.ajax({
       async: false,
       type: "POST",
       url: "/reviews/update_reviews/",
       data: {
           'key' : key,
           'value' : value,
           'csrfmiddlewaretoken' : getCookie('csrftoken')
       },
   })
   .done(function(response)
   {
        mydata = [];
        for (var key1 in response)
        {
            mydata.push(response[key1]);
        }
//        mytable = $('#drone_review').DataTable()
        table.clear();
        table.rows.add(mydata);
        table.draw();
   });
}
function sort_results2(key, value) {
       if (value == 'Drone ID' || value == 'Status' || value == 'Start Time' || value == 'End Time' || value == 'Duration')
       {
            return
       }
       console.log('keyyy: ' + key);
       console.log('value: ' + value);
       $.ajax({
           async: false,
           type: "POST",
           url: "/reviews/update_reviews/",
           data: {
               'key' : key,
               'value' : value,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response)
            var str = response; //it can be anything
            var Obj = document.getElementById("tblReviews");
            if(Obj.outerHTML) { //if outerHTML is supported
                Obj.outerHTML=str; ///it's simple replacement of whole element with contents of str var
            }
            else { //if outerHTML is not supported, there is a weird but crossbrowsered trick
                var tmpObj=document.createElement("div");
                tmpObj.innerHTML='<!--THIS DATA SHOULD BE REPLACED-->';
                ObjParent=Obj.parentNode; //Okey, element should be parented
                ObjParent.replaceChild(tmpObj,Obj); //here we placing our temporary data instead of our target, so we can find it then and replace it into whatever we want to replace to
                ObjParent.innerHTML=ObjParent.innerHTML.replace('<div><!--THIS DATA SHOULD BE REPLACED--></div>',str);
            }
       return
//        console.log(response);
    })
    do_data_table();

   }

function once(fn, context) {
	var result;

	return function() {
		if(fn) {
			result = fn.apply(context || this, arguments);
			fn = null;
		}

		return result;
	};
}


$('#tblReviews').on('change', '#drone_id', function() {
    once(sort_results('drone_num', $("#drone_id option:selected").text()));
});
$('#tblReviews').on('change', '#drone_states', function() {
    once(sort_results('state', $("#drone_states option:selected").text()));
});
//$('#duration').on('input', function(e) {
//    once(sort_results(e, 'duration', $(this).val()));
//});

function showPopUpForReview(file_path) {
        console.log(file_path)
       $.ajax({
           async: false,
           type: "POST",
           url: "/reviews/pop_up_modal/",
           data: {
               'file_path' : file_path,
               'is_log' : true,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response)
            var str = response; //it can be anything
            var Obj = document.getElementById("modalLogsPopUp");
            if(Obj.outerHTML) { //if outerHTML is supported
                Obj.outerHTML=str; ///it's simple replacement of whole element with contents of str var
            }
            else { //if outerHTML is not supported, there is a weird but crossbrowsered trick
                var tmpObj=document.createElement("div");
                tmpObj.innerHTML='<!--THIS DATA SHOULD BE REPLACED-->';
                ObjParent=Obj.parentNode; //Okey, element should be parented
                ObjParent.replaceChild(tmpObj,Obj); //here we placing our temporary data instead of our target, so we can find it then and replace it into whatever we want to replace to
                ObjParent.innerHTML=ObjParent.innerHTML.replace('<div><!--THIS DATA SHOULD BE REPLACED--></div>',str);
            }
       });

   }

function showReportPopUpForReview(drone_num) {
        console.log(drone_num)
       $.ajax({
           async: false,
           type: "POST",
           url: "/reviews/pop_up_report_modal/",
           data: {
               'drone_num' : drone_num,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            console.log(response)
            var str = response; //it can be anything
            var Obj = document.getElementById("modalLogsPopUp");
            if(Obj.outerHTML) { //if outerHTML is supported
                Obj.outerHTML=str; ///it's simple replacement of whole element with contents of str var
            }
            else { //if outerHTML is not supported, there is a weird but crossbrowsered trick
                var tmpObj=document.createElement("div");
                tmpObj.innerHTML='<!--THIS DATA SHOULD BE REPLACED-->';
                ObjParent=Obj.parentNode; //Okey, element should be parented
                ObjParent.replaceChild(tmpObj,Obj); //here we placing our temporary data instead of our target, so we can find it then and replace it into whatever we want to replace to
                ObjParent.innerHTML=ObjParent.innerHTML.replace('<div><!--THIS DATA SHOULD BE REPLACED--></div>',str);
            }
       });
   }

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
    $('#loader').show();
    $.ajax({
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
            $('#loader').hide();
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
    $('#loader').show();
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
            $('#loader').hide();
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
    $('#loader').show();
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
            $('#loader').hide();
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
    $('#loader').show();
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
            $('#loader').hide();
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
    $('#loader').show();
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
            $('#loader').hide();
            $("#errorsPerMonthPopUp").modal('show');
       });
}

function saveErrorsPerMonthtImage() {
    $("#ErrorsPerMonthChart").get(0).toBlob(function(blob) {
        saveAs(blob, "errorsPerMonth.png");
    });
}

function myFunction() {
console.log('clicked!')
    document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}