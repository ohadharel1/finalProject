send_func = null;

jQuery(function () {

  function getFlights(data) {
    // $('#tblDrone').empty();
    //    $.getJSON("json.json", function (data) {



         var tableD= getElementById("tbl");
           $(data).each(function (index, v) {
             var flag=false;
             for(var i =0, row; row=tableD.row[i], i++){
               var cell=row.cells[0].innerHTML;
               var cellStatus= row.cells[2].innerHTML;
                if(v.drone_num == cell){
                    row.cells[2].innerHTML=v.cmd;
                    flag= true;
                }
             }
             if(flag==false){
           tableD+= '<tr><td>' + v.drone_num + '</td><td>' + v.cmd + '</td></tr>';
         }
           });

        $('#tbl').append(tableD);




    //    });

       }




  // setInterval(getFlights,2500);

  // $(".clickable-row").click(function() {
  //     window.location = $(this).data("href");
  // });




    var socket = io.connect('http://127.0.0.1:5000');
    var client_id = 0
    socket.on('connect', function() {
        console.log('connected');
    });
    socket.on('disconnect', function() {
        socket.send('disconnect');
        console.log('disconnect');
    });
    socket.on('message', function(msg) {
        console.log('Received message:' + msg.result);
        var input = document.getElementById("input1").value;
        input = msg.result;

    });
    socket.on('my_msg', function(msg) {
          getFlights(msg.msg)
          console.log('Received my_msg');
    });
    function send_msg(msg) {
        socket.send(msg);
        console.log('msg sent:' + JSON.stringify(msg));
    };
    send_func = send_msg;

 });

 function send_btn1(msg){
     var msg = {cmd: 'query', query_num: 3, arg1: 20};
     send_func(msg)
 }

function resetAllSpans() {
document.getElementById("weightError").innerHTML = "";
// document.getElementById("lastNameError").innerHTML = "";
// document.getElementById("userNameError").innerHTML = "";
// document.getElementById("emailError").innerHTML = "";
// document.getElementById("passwordError").innerHTML = "";
// document.getElementById("passwordValError").innerHTML = "";
}

function checkInfo() {
resetAllSpans();

var numbers = /^[0-9]+$/;


    //validation of the first name
    if ((frm.weight.value) == "" || (frm.weight.value) == null) {
        //alert("Please Enter The First Name");
        document.getElementById("weightError").innerHTML = " * Enter The First Name";
        frm.weight.focus();
        return false;
    }

    if (!(frm.weight.value).match(numbers)) {
        //alert("The First Name Must Contains Only letters!");
        document.getElementById("weightError").innerHTML = " * Use only number!";
        frm.weight.focus();
        return false;
    }
    //
    // //validation of the last name
    // if ((frm.lastNameField.value) == "" || (frm.lastNameField.value) == null) {
    //     //alert("Please Enter The Last Name");
    //     document.getElementById("lastNameError").innerHTML = "*Enter last name";
    //     frm.lastNameField.focus();
    //     return false;
    // }
    //
    // if (!(frm.lastNameField.value).match(letters)) {
    //     //alert("The Last Name Must Contains Only letters!");
    //     document.getElementById("lastNameError").innerHTML = "*Use only letters!";
    //     frm.lastNameField.focus();
    //     return false;
    // }
    //
    // //validation of the user name
    // if ((frm.username.value) == "" || (frm.username.value) == null) {
    //     //alert("Please Enter The User Name");
    //     document.getElementById("userNameError").innerHTML = "*Enter user name";
    //     frm.username.focus();
    //     return false;
    // }
    //
    // if ((frm.username.value).charAt(0) == "." || (frm.username.value).charAt((frm.username.value).length - 1) == ".") {
    //     //alert("Please Enter A Valid User Name");
    //     document.getElementById("userNameError").innerHTML = "*Invalid user name";
    //     frm.username.focus();
    //     return false;
    // }
    //
    // if (!(frm.username.value).match(validUserNameChar)) {
    //     //alert("Please Enter A Valid User Name");
    //     document.getElementById("userNameError").innerHTML = "*Invalid user name";
    //     frm.username.focus();
    //     return false;
    // }
    //
    // //validation of the email
    // if ((frm.emailField.value) == "" || (frm.emailField.value) == null) {
    //     //alert("Please Enter An Email");
    //     document.getElementById("emailError").innerHTML = "*Enter Email";
    //     frm.emailField.focus();
    //     return false;
    // }
    //
    // if (!regularExpressions.test(frm.emailField.value)) {
    //     //alert("Please Enter A Valid Email");
    //     document.getElementById("emailError").innerHTML = "*Invalid Email";
    //     frm.emailField.focus();
    //     return false;
    // }
    //
    // //validation of the password
    // if ((frm.passwordField.value) == "" || (frm.passwordField.value) == null) {
    //     //alert("Please Enter The Password");
    //     document.getElementById("passwordError").innerHTML = "*Enter password";
    //     frm.passwordField.focus();
    //     return false;
    // }
    //
    // if ((frm.confirmPasswordField.value) == "" || (frm.confirmPasswordField.value) == null) {
    //     //alert("Please Enter The Password Validation");
    //     document.getElementById("passwordValError").innerHTML = "*password validation";
    //     frm.confirmPasswordField.focus();
    //     return false;
    // }
    //
    // if ((frm.passwordField.value) !== (frm.confirmPasswordField.value)) {
    //     //alert("The Passwords Are Not Identical");
    //     document.getElementById("passwordError").innerHTML = "*not identical";
    //     document.getElementById("passwordValError").innerHTML = "*not identical";
    //     frm.passwordField.focus();
    //     return false;
    // }

}