var drone_id_for_comment = null;

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


setInterval(function() {
    $.ajax({
        type: "GET",
        url: "{% url 'flight_monitor:get_current_flights' %}" , // URL to your view that serves new info
    })
    .done(function(response) {
        var str = response; //it can be anything
var Obj = document.getElementById("tblDrone");
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
//        console.log(response);
    });
}, 1000)

setInterval(function() {
    $.ajax({
        type: "GET",
        url: "{% url 'flight_monitor:pop_up_modal_header'%}" , // URL to your view that serves new info
    })
    .done(function(response) {
        var str = response; //it can be anything
var Obj = document.getElementById("modalTitle");
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
//        console.log(response);
    });
}, 1000)


setInterval(function() {
    $.ajax({
        type: "GET",
        url: "{% url 'flight_monitor:pop_up_modal_body' %}" , // URL to your view that serves new info
    })
    .done(function(response) {
        var str = response; //it can be anything
var Obj = document.getElementById("modalBody");
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
//        console.log(response);
    });
}, 1000)

function showPopUpForDrone(drone_num) {
       $.ajax({
           type: "POST",
           url: "{% url 'flight_monitor:pop_up_modal' %}",
           data: {
               'drone_num' : drone_num,
               'csrfmiddlewaretoken' : $("{% csrf_token %}").val()
           },
           success: function ajaxSuccess(data, textStatus, jqXHR) {
               $(e.target).parent().html(data);
           },
           dataType: 'html'
       });

   }


function closeModal()
{
    $.ajax({
           type: "GET",
           url: "{% url 'flight_monitor:pop_up_modal_close' %}",
//           success: function ajaxSuccess(data, textStatus, jqXHR) {
//               $(e.target).parent().html(data);
//           },
           dataType: 'html'
       });
}

//$('#btn_Add_Comment').click(function ($) {
//    console.log('clicked!');
//
//    $.ajax({
//       type: "POST",
//       url: "/flight_monitor/save_comment/",
//       data: {
//            'drone_id' : drone_id_for_comment,
//           'csrfmiddlewaretoken' : getCookie('csrftoken')
//       },
//   })
//   .done(function(response) {
//        drone_id_for_comment = null;
//        alert('saved');
//    } );
// });

function saveFlightComent(comment)
{
    console.log('clicked!');

    $.ajax({
       type: "POST",
       url: "/flight_monitor/save_comment/",
       data: {
            'drone_id' : drone_id_for_comment,
            'comment': comment,
           'csrfmiddlewaretoken' : getCookie('csrftoken')
       },
   })
   .done(function(response) {
        drone_id_for_comment = null;
        /*alert('saved');*/
         $('#success_title').text('Success');
                setTimeout(function(){
                    $("#modal_pop_up_result").modal('hide');
                }, 2000);
                $('#modal_pop_up_result').modal('show');
    } );
}

function showCommentPopUp(id)
{
    $("#addCommentPopUp").modal('show');
    drone_id_for_comment = id;
}
