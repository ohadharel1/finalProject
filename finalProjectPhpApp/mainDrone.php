
<!DOCTYPE html>
<html >
<head>
  <meta charset="UTF-8">
  <!-- <title>isNet Login Page</title> -->
      <link rel="stylesheet" type="text/css" href="scruples.css">
</head>

<body>
  <div class="form">

    <h4>Please fill out all criteria</h4>


    <form name="frm" method="post" action="scruplesTbl.php"  >

      <p><input type="text" name="weight" placeholder="Weight"><span class = "required" id = "weightError"></span></p>

      <div class= "selectDiv">
        <select id= "mySelect" onChange = "load()">
        <option value=''>--Number of arms--</option>
          <option value= "Quad"> Quad</option>
            <option value= "Hexa"> Hexa</option>
              <option value= "Octa"> Octa</option>
        </select>
      </div>

      <p><input type="text" name="size" placeholder="Maximum size"></p>
      <p><input type="text" name="payload" placeholder=" Payload weight"></p>

      <p><input type="text" name="timeOfWork" placeholder="Time of work"></p>
      <p><input type="text" name="speed" placeholder="Speed"></p>
      <p><input type="text" name="range" placeholder="Flight range"></p>
      <p><input type="text" name="price" placeholder="Maximum price"></p>

      <input type="submit" class="button" value="Submit" onclick="return checkInfo();"  />

        </form>

  </div>

</body>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script src="Scruples.js"></script>

</html>
