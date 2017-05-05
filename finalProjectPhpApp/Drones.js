send_func = null;
quert_numEnum ={
  // QUERY_GET_ACTIVE_DRONES,
  // QUERY_GET_FLIGHT_RECORDS,
  // QUERY_GET_FLIGHT_TIME_FOR_DRONE,
  QUERY_GET_CURRENT_FLIGHT_DETAILS: 4

//  QUERY_SIZE
}

jQuery(function () {

 var timerVar = setInterval(countTimer, 1000);
 var totalSeconds = 0;
 var time = '00:00';
  //time = document.getElementById('time1')
 //var seconds = 0, minutes = 0,t;
 function countTimer() {
     ++totalSeconds;
     var hour = Math.floor(totalSeconds /3600);
     var minute = Math.floor((totalSeconds - hour*3600)/60);
     var seconds = totalSeconds - (hour*3600 + minute*60);
     time = minute + ":" + seconds
  }

//   function add() {
//     seconds++;
//     if (seconds >= 60) {
//         seconds = 0;
//         minutes++;
//         if (minutes >= 60) {
//             minutes = 0;
//         }
//     }
//
//     time.textContent = (minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" + (seconds > 9 ? seconds : "0" + seconds);
//
//     timer();
// }
// function timer() {
//     t = setTimeout(add, 1000);
// }




  function getFlights(data) {

         var tableD= document.getElementById("tbl");
           $(data).each(function (index, v) {
             var flag=false;
             var count = 0;
             var i =0;
             for(i=0 ; row=tableD.rows[i]; i++){
               var cell=row.cells[0].innerHTML;
                if(v.drone_num == cell){
                    row.cells[2].innerHTML=v.cmd;

                      var intervalID=setInterval(function() {
                                $('.flickering').toggleClass('blink');
                                count++;
                                if (count === 4) clearInterval(intervalID);
                                }, 500);
                                  row.cells[2].innerHTML=v.cmd;
                    flag= true;
                }
             }
             if(flag==false){
                //timer();
                 tableD+= '<tr><td>' + v.drone_num + '</td><td>' + v.drone_ip + '</td><td class= "flickering">' + v.cmd + '</td><td>' + time + '</td></tr>';

         }

           });

        $('#tbl').append(tableD);

       }

       $('#tbl').on('click', 'tr', function() {
          var row = $(this).find('td:nth-child(2)').text();
          var msg = {cmd: 'query', query_num: 4, arg1: row};
         send_func(msg)

       });


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
        if(msg.success == false)
        {
          console.log('query did not succeded');
          return;
        }
        else
        {

          switch (msg.query_num)
          {

            case 4:
              mypopup(msg.result);

              break;
            default:

          }
        }


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

    function mypopup(file)
    {
        alert(file);
    }

 });

 function send_btn1(msg){
     var msg = {cmd: 'query', query_num: 3, arg1: 20};
     send_func(msg)
 }

 function move() {
   var elem = document.getElementById("myBar");
   var width = 10;
   var id = setInterval(frame, 100);
   function frame() {
     if (width >= 100) {
       clearInterval(id);
       window.open ('setupDrone.html','_self',false)

     } else {
       width++;
       elem.style.width = width + '%';
       elem.innerHTML = width * 1  + '%';
     }


   }

 }


 //-----------------------------------------------Setup Form Page-----------------------------------------------------------------------


function resetAllSpans() {
document.getElementById("weightError").innerHTML = "";
// document.getElementById("lastNameError").innerHTML = "";
// document.getElementById("userNameError").innerHTML = "";
// document.getElementById("emailError").innerHTML = "";
// document.getElementById("passwordError").innerHTML = "";
// document.getElementById("passwordValError").innerHTML = "";
}

function checkInfo() {

  var size =document.getElementById("SizeField");
  var payload= document.getElementById("PayloadField");
  var timeofwork= document.getElementById("TimeofworkField");
  var range= document.getElementById("RangeField");
  var price= document.getElementById("PriceField");

//resetAllSpans();

var numbers = /^[0-9]+$/;


//validation of the first name
if (size.value == "" || size.value == null) {
     document.getElementById("SizeFieldError").innerHTML = " * Please enter a size";
    size.focus();
    return false;

      }

if (!size.value.match(numbers)) {
      document.getElementById("SizeFieldError").innerHTML = " * Use only number!";
      size.focus();
      return false;
        }

if (payload.value == "" || payload.value == null) {
        document.getElementById("PayloadFieldError").innerHTML = " * Please enter a payload";
        payload.focus();
        return false;

        }

if (!payload.value.match(numbers)) {
        document.getElementById("PayloadFieldError").innerHTML = " * Use only number!";
        payload.focus();
        return false;
        }

if (timeofwork.value == "" || timeofwork.value == null) {
        document.getElementById("TimeofworkFieldError").innerHTML = " * Please enter a payload";
        timeofwork.focus();
        return false;
        }

if (!timeofwork.value.match(numbers)) {
        document.getElementById("TimeofworkFieldError").innerHTML = " * Use only number!";
        timeofwork.focus();
        return false;
        }

if (range.value == "" || range.value == null) {
        document.getElementById("RangeFieldError").innerHTML = " * Please enter a range";
        range.focus();
        return false;
        }

if (!range.value.match(numbers)) {
        document.getElementById("RangeFieldError").innerHTML = " * Use only number!";
        range.focus();
        return false;
        }

if (price.value == "" || price.value == null) {
        document.getElementById("PriceFieldError").innerHTML = " * Please enter a payload";
        price.focus();
        return false;
        }

if (!price.value.match(numbers)) {
        document.getElementById("PriceFieldError").innerHTML = " * Use only number!";
        price.focus();
        return false;
        }




    }
