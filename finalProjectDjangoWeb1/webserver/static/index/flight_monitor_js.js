
var append_increment = 0;
setInterval(function() {
    $.ajax({
        type: "GET",
        url: location.href='../../flight_monitor/get_current_flights',  // URL to your view that serves new info
    })
    .done(function(response) {
        $('#flight_tb').append(response.data);
    });
}, 3000)
