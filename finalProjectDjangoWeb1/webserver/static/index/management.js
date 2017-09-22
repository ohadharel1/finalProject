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

function update_motor_table(id, name, kv, weight, price)
{
    console.log('showing');
    $("#motor_edit_modal").modal('hide');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/motor_table_update/",
           data: {
               'motor_id' : id,
               'motor_name' : name,
               'motor_kv' : kv,
               'motor_weight' : weight,
               'motor_price' : price,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            motor_table.clear();
            motor_table.rows.add(mydata);
            motor_table.draw();

            $('#loader').hide();
            console.log($('#result_header'));
            if(response.result == true)
            {
                $('#result_header').text('Success');
                setTimeout(function(){
                    $("#modal_pop_up_result").modal('hide');
                }, 5000);
            }
            else
            {
                $('#result_header').text('Failure!');
                $('#result_body').text(response.message);
            }
            $('#modal_pop_up_result').modal('show');
            console.log(response.result);
            console.log('hiding');
    });
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
            var Obj = document.getElementById("updateContainer");
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
    get_motor_table();
    console.log('motor pressed!')
});
$('#tableTabs').on('click', '#batTab', function() {
//    $(this).tab("option", "active", 1);
    get_bat_table();
    console.log('battery pressed!')
});
$('#tableTabs').on('click', '#propTab', function() {
    get_prop_table();
    console.log('battery pressed!')
});

$("#success-alert").fadeTo(2000, 500).slideUp(500, function(){
    $("#success-alert").slideUp(500);
});

//$('#duration').on('input', function(e) {
//    once(sort_results(e, 'duration', $(this).val()));
//});

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
//            console.log(response)
            var str = response; //it can be anything
            var Obj = document.getElementById("updateContainer");
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
       checkForError
}

function checkForError(alert_display, alert)
{
    if(alert_display == 'True')
    {
        console.log("alert_diaplay is true")
        if(alert == 'True')
        {
            console.log("alert is true")
            window.alert("operatrion success!");
        }
        else
        {
            console.log("alert is false")
            window.alert("operatrion failure!");
        }
    }
    else
    {
        console.log("alert_diaplay is false")
    }
}

function motor_add_single_pop_up()
{
    $('#motor_add_single_modal').modal('show');
}

function motor_add_multi_pop_up()
{
    $('#motor_add_multi_modal').modal('show');
}

function add_single_to_motor_table(name, kv, weight, price)
{
    $('#motor_add_single_modal').modal('hide');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/add_single_motor_table/",
           data: {
                'motor_name' : name,
                'motor_kv' : kv,
                'motor_weight' : weight,
                'motor_price' : price,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            motor_table.clear();
            motor_table.rows.add(mydata);
            motor_table.draw();

            $('#loader').hide();

            if(response.result == true)
            {
                $('#result_header').text('Success');
                setTimeout(function(){
                    $("#modal_pop_up_result").modal('hide');
                }, 5000);
            }
            else
            {
                $('#result_header').text('Failure!');
                $('#result_body').text(response.message);
            }
            $('#modal_pop_up_result').modal('show');
    });
}

function add_multi_to_motor_table(file)
{
    $('#motor_add_multi_modal').modal('hide');
    $('#loader').show();
    var read = new FileReader();
    var content = '';
    read.readAsBinaryString(file[0]);

    read.onloadend = function(){
        content = read.result;
        $.ajax({
           type: "POST",
           url: "/management/add_multi_motor_table/",
           data: {
                'content' : content,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(response.summery);
            motor_table.clear();
            motor_table.rows.add(mydata);
            motor_table.draw();

            $('#loader').hide();

            $('#result_header').text('Summery');
            $('#result_body').text(response.summery);
            $('#modal_pop_up_result').modal('show');
    });
    }


}

function get_motor_table()
{
    console.log('get motor table');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/get_motor_table/",
           data: {
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            motor_table.clear();
            motor_table.rows.add(mydata);
            motor_table.draw();

            $('#loader').hide();
    });
}


function delete_motor(id)
{
//    $('#motor_add_single_modal').modal('hide');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/delete_motor_table/",
           data: {
                'motor_id' : id,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            motor_table.clear();
            motor_table.rows.add(mydata);
            motor_table.draw();

            $('#loader').hide();

            if(response.result == true)
            {
                $('#result_header').text('Success');
                setTimeout(function(){
                    $("#modal_pop_up_result").modal('hide');
                }, 5000);
            }
            else
            {
                $('#result_header').text('Failure!');
                $('#result_body').text(response.message);
            }
            $('#modal_pop_up_result').modal('show');
    });
}


function bat_add_single_pop_up()
{
    $('#bat_add_single_modal').modal('show');
}

function bat_add_multi_pop_up()
{
    $('#bat_add_multi_modal').modal('show');
}

function add_single_to_bat_table(name, type, volt, capacity, discharge_rate, weight, price)
{
    $('#bat_add_single_modal').modal('hide');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/add_single_bat_table/",
           data: {
                'bat_name' : name,
                'bat_type' : type,
                'bat_volt' : volt,
                'bat_capacity' : capacity,
                'bat_discharge_rate' : discharge_rate,
                'bat_weight' : weight,
                'bat_price' : price,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            bat_table.clear();
            bat_table.rows.add(mydata);
            bat_table.draw();

            $('#loader').hide();

            if(response.result == true)
            {
                $('#result_header').text('Success');
                setTimeout(function(){
                    $("#modal_pop_up_result").modal('hide');
                }, 5000);
            }
            else
            {
                $('#result_header').text('Failure!');
                $('#result_body').text(response.message);
            }
            $('#modal_pop_up_result').modal('show');
    });
}

function add_multi_to_bat_table(file)
{
    $('#bat_add_multi_modal').modal('hide');
    $('#loader').show();
    var read = new FileReader();
    var content = '';
    read.readAsBinaryString(file[0]);

    read.onloadend = function(){
        content = read.result;
        $.ajax({
           type: "POST",
           url: "/management/add_multi_bat_table/",
           data: {
                'content' : content,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(response.summery);
            bat_table.clear();
            bat_table.rows.add(mydata);
            bat_table.draw();

            $('#loader').hide();

            $('#result_header').text('Summery');
            $('#result_body').text(response.summery);
            $('#modal_pop_up_result').modal('show');
    });
    }
}


function get_bat_table()
{
    console.log('get bat table');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/get_bat_table/",
           data: {
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            bat_table.clear();
            bat_table.rows.add(mydata);
            bat_table.draw();

            $('#loader').hide();
    });
    $('#tblbattery tbody').on( 'click', 'button', function (evt) {
//        evt.stopPropagation();
//        evt.preventDefault();
        evt.stopImmediatePropagation();
        if (this.id == "edit")
        {
            var data = bat_table.row( $(this).parents('tr') ).data();
            $(".modal-body #bat_id").val(data.id);
            $(".modal-body #bat_name").val(data.name);
            $(".modal-body #bat_volt").val(data.volt);
            $(".modal-body #bat_type").val(data.type);
            $(".modal-body #bat_discharge_rate").val(data.discharge_rate);
            $(".modal-body #bat_capacity").val(data.capacity);
            $(".modal-body #bat_weight").val(data.weight);
            $(".modal-body #bat_price").val(data.price);
            $("#bat_edit_modal").modal('show');
        }
        else
        {
            console.log('delete bat');
            var data = bat_table.row( $(this).parents('tr') ).data();
            delete_bat(data.id);
        }
    } );
}


function update_bat_table(id, name, volt, type, discharge_rate, capacity, weight, price)
{
    $("#bat_edit_modal").modal('hide');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/bat_table_update/",
           data: {
               'bat_id' : id,
               'bat_name' : name,
               'bat_type' : type,
               'bat_volt' : volt,
               'bat_discharge_rate' : discharge_rate,
               'bat_capacity' : capacity,
               'bat_price' : price,
               'bat_weight' : weight,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            bat_table.clear();
            bat_table.rows.add(mydata);
            bat_table.draw();

            $('#loader').hide();
            console.log($('#result_header'));
            if(response.result == true)
            {
                $('#result_header').text('Success');
                setTimeout(function(){
                    $("#modal_pop_up_result").modal('hide');
                }, 5000);
            }
            else
            {
                $('#result_header').text('Failure!');
                $('#result_body').text(response.message);
            }
            $('#modal_pop_up_result').modal('show');
    });
}

function delete_bat(id)
{
    console.log(id);
//    $('#motor_add_single_modal').modal('hide');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/delete_bat_table/",
           data: {
                'bat_id' : id,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            bat_table.clear();
            bat_table.rows.add(mydata);
            bat_table.draw();

            $('#loader').hide();

            if(response.result == true)
            {
                $('#result_header').text('Success');
                setTimeout(function(){
                    $("#modal_pop_up_result").modal('hide');
                }, 5000);
            }
            else
            {
                $('#result_header').text('Failure!');
                $('#result_body').text(response.message);
            }
            $('#modal_pop_up_result').modal('show');
    });
}


function prop_add_single_pop_up()
{
    $('#prop_add_single_modal').modal('show');
}

function prop_add_multi_pop_up()
{
    $('#prop_add_multi_modal').modal('show');
}

function add_single_to_prop_table(name, diameter, speed, weight, price)
{
    $('#prop_add_single_modal').modal('hide');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/add_single_prop_table/",
           data: {
                'prop_name' : name,
                'prop_diameter' : diameter,
                'prop_speed' : speed,
                'prop_weight' : weight,
                'prop_price' : price,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            prop_table.clear();
            prop_table.rows.add(mydata);
            prop_table.draw();

            $('#loader').hide();

            if(response.result == true)
            {
                $('#result_header').text('Success');
                setTimeout(function(){
                    $("#modal_pop_up_result").modal('hide');
                }, 5000);
            }
            else
            {
                $('#result_header').text('Failure!');
                $('#result_body').text(response.message);
            }
            $('#modal_pop_up_result').modal('show');
    });
}

function add_multi_to_prop_table(file)
{
    $('#prop_add_multi_modal').modal('hide');
    $('#loader').show();
    var read = new FileReader();
    var content = '';
    read.readAsBinaryString(file[0]);

    read.onloadend = function(){
        content = read.result;
        $.ajax({
           type: "POST",
           url: "/management/add_multi_prop_table/",
           data: {
                'content' : content,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(response.summery);
            prop_table.clear();
            prop_table.rows.add(mydata);
            prop_table.draw();

            $('#loader').hide();

            $('#result_header').text('Summery');
            $('#result_body').text(response.summery);
            $('#modal_pop_up_result').modal('show');
    });
    }
}


function get_prop_table()
{
    console.log('get prop table');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/get_prop_table/",
           data: {
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            prop_table.clear();
            prop_table.rows.add(mydata);
            prop_table.draw();

            $('#loader').hide();
    });
    $('#tblprop tbody').on( 'click', 'button', function (evt) {
        evt.stopImmediatePropagation();
        if (this.id == "edit")
        {
            var data = prop_table.row( $(this).parents('tr') ).data();
            $(".modal-body #prop_id").val(data.id);
            $(".modal-body #prop_name").val(data.name);
            $(".modal-body #prop_diameter").val(data.diameter);
            $(".modal-body #prop_speed").val(data.speed);
            $(".modal-body #prop_weight").val(data.weight);
            $(".modal-body #prop_price").val(data.price);
            $("#prop_edit_modal").modal('show');
        }
        else
        {
            console.log('delete prop');
            var data = prop_table.row( $(this).parents('tr') ).data();
            delete_prop(data.id);
        }
    } );
}


function update_prop_table(id, name, diameter, speed, weight, price)
{
    $("#prop_edit_modal").modal('hide');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/prop_table_update/",
           data: {
               'prop_id' : id,
               'prop_name' : name,
               'prop_diameter' : diameter,
               'prop_speed' : speed,
               'prop_price' : price,
               'prop_weight' : weight,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            prop_table.clear();
            prop_table.rows.add(mydata);
            prop_table.draw();

            $('#loader').hide();
            console.log($('#result_header'));
            if(response.result == true)
            {
                $('#result_header').text('Success');
                setTimeout(function(){
                    $("#modal_pop_up_result").modal('hide');
                }, 5000);
            }
            else
            {
                $('#result_header').text('Failure!');
                $('#result_body').text(response.message);
            }
            $('#modal_pop_up_result').modal('show');
    });
}

function delete_prop(id)
{
//    console.log(id);
//    $('#motor_add_single_modal').modal('hide');
    $('#loader').show();
    $.ajax({
//           async: false,
           type: "POST",
           url: "/management/delete_prop_table/",
           data: {
                'prop_id' : id,
               'csrfmiddlewaretoken' : getCookie('csrftoken')
           },
       })
       .done(function(response) {
//            console.log(response);
            mydata = [];
            for (var key in response.values)
            {
                mydata.push(response.values[key]);
            }
//            console.log(mydata);
            prop_table.clear();
            prop_table.rows.add(mydata);
            prop_table.draw();

            $('#loader').hide();

            if(response.result == true)
            {
                $('#result_header').text('Success');
                setTimeout(function(){
                    $("#modal_pop_up_result").modal('hide');
                }, 5000);
            }
            else
            {
                $('#result_header').text('Failure!');
                $('#result_body').text(response.message);
            }
            $('#modal_pop_up_result').modal('show');
    });
}