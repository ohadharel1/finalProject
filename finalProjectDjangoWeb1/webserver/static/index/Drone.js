 function move() {
   var elem = document.getElementById("myBar");
   var width = 10;
   var id = setInterval(frame, 100);
   function frame() {
     if (width >= 100) {
       clearInterval(id);
       location.href='../../drone_setup/setup_result';

     } else {
       width++;
       elem.style.width = width + '%';
       elem.innerHTML = width * 1  + '%';
     }


   }

 }

    //-----------------------------------------------Setup Details Page-----------------------------------------------------------------------

    var slideIndex = 1;
    showDivs(slideIndex);

    function plusDivs(n) {
      showDivs(slideIndex += n);
    }

    function showDivs(n) {
      var i;
      var x = document.getElementsByClassName("mySlides");
      if (n > x.length) {slideIndex = 1}
      if (n < 1) {slideIndex = x.length}
      for (i = 0; i < x.length; i++) {
         x[i].style.display = "none";
      }
      x[slideIndex-1].style.display = "block";
    }
