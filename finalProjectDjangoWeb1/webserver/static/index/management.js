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


function get_and_sort_results(table, key = null, value = null) {
       if (value == 'Drone ID' || value == 'Status' || value == 'Start Time' || value == 'End Time' || value == 'Duration')
       {
            return
       }
       console.log('table: ' + table);
       console.log('key: ' + key);
       console.log('value: ' + value);
       $.ajax({
           async: false,
           type: "POST",
           url: "/management/get_table/",
           data: {
               'table' : table,
               'key' : key,
               'value' : value,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            var str = response; //it can be anything
            var Obj = document.getElementById("tableContainer");
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


$('#tableTabs').on('click', '#motorTab', function() {
    once(get_and_sort_results('tblmotor'));
//    console.log('motor pressed!')
});
$('#tableTabs').on('click', '#batTab', function() {
    once(get_and_sort_results('tblbattery'));
//    console.log('battery pressed!')
});
$('#tableTabs').on('click', '#propTab', function() {
    once(get_and_sort_results('tblprops'));
//    console.log('battery pressed!')
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

function save_changes(id, old_name, old_kv, old_weight, old_price){
    console.log('id is: ' + id)
    console.log('old name is: ' + old_name)
    console.log('old kv is: ' + old_kv)
    console.log('old weight is: ' + old_weight)
    console.log('old price is: ' + old_price)
    var tr = document.getElementById('tblmotor').rows.namedItem(id)
    name = tr.cells[1].children[0].value
    kv = tr.cells[2].children[0].value
    weight = tr.cells[3].children[0].value
    price = tr.cells[4].children[0].value
    $.ajax({
           async: false,
           type: "POST",
           url: "/management/table_update/",
           data: {
               'table_name' : 'tblmotor',
               'id' : id,
               'name' : name,
               'kv' : kv,
               'weight' : weight,
               'price' : price,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            console.log(response)
       });
}