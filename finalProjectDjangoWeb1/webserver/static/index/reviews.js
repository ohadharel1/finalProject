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


function sort_results(e, key, value) {
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
           success: function ajaxSuccess(data, textStatus, jqXHR) {
               $(e.target).parent().html(data);
           },
           dataType: 'html'
       })
       .done(function(response) {
            var str = response; //it can be anything
            var Obj = document.getElementById("drone_review");
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
    });

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


$('#tblReviews').on('change', '#drone_id', function(e) {
    once(sort_results(e, 'drone_num', $("#drone_id option:selected").text()));
});
$('#tblReviews').on('change', '#drone_states', function(e) {
    once(sort_results(e, 'state', $("#drone_states option:selected").text()));
});

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