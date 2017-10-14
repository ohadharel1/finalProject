
jQuery(document).ready(function($){
    jQuery.noConflict();
//    $('#loader_modal').modal('hide');
    $('#wait_dialog').hide();
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

function submit_setup_form(num_of_drones, body, size, payload, time, range, price)
{
    jQuery(document).ready(function ($) {
        console.log(num_of_drones + ', ' + body + ', ' + size + ', ' + payload + ', ' + time + ', ' + range);
        //start loading animation
        $('#loader_modal').modal();
        $('#wait_dialog').show();
        //create ajax call with args
        $.ajax({
    //           async: false,
               dataType: 'html',
               type: "POST",
               url: "/drone_setup/setup_params/",
               data: {
                   'drone_type' : body,
                   'max_size' : size,
                   'min_payload' : payload,
                   'min_time' : time,
                   'min_range' : range,
                   'max_price' : price,
                   'iterations' : num_of_drones,
                   'csrfmiddlewaretoken' : getCookie('csrftoken')
               },
           })
           .done(function(response) {
                console.log(response);
                setTimeout(function(){
                    window.location = "/drone_setup/setup_result/";
                }, 5000);

        });
        //when done close loading animation and go to new page
       });
}

    //-----------------------------------------------Setup Details Page-----------------------------------------------------------------------






