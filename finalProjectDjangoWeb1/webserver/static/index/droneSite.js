
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
                console.log(response.is_error)
                var do_message = response.do_message;
                if (do_message)
                {
                    if (response.is_error)
                    {
                        swal('drone ' + response.drone_id + ' has an error', {
                          icon: "error",
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
                    else if (response.is_takeoff)
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

