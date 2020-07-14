// var x = document.getElementById("demo");
var latlon = "";

$(document).ready(function(){ 
  getLocation()
});
        
function getLocation() {
  if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else {
  x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  latlon = position.coords.latitude + "," + position.coords.longitude;
  $("#latlon").val(latlon);
  console.log(latlon)
  //var img_url = "https://maps.googleapis.com/maps/api/staticmap?center="
  //+latlon+"&zoom=14&size=400x300&key=AIzaSyBu-916DdpKAjTmJNIgngS6HL_kDIKU0aU";
  //document.getElementById("mapholder").innerHTML = "<img src='"+img_url+"'>";

}
//To use this code on your website, get a free API key from Google.
//Read more at: https://www.w3schools.com/graphics/google_maps_basic.asp

function showError(error) {
  switch(error.code) {
  case error.PERMISSION_DENIED:
    x.innerHTML = "User denied the request for Geolocation."
    break;
  case error.POSITION_UNAVAILABLE:
    x.innerHTML = "Location information is unavailable."
    break;
  case error.TIMEOUT:
    x.innerHTML = "The request to get user location timed out."
    break;
  case error.UNKNOWN_ERROR:
    x.innerHTML = "An unknown error occurred."
    break;
  }
}


// $("#parking_map").on("click", function(e) {
//   e.preventDefault();
//   var location = $("#latlon").val();
  
//   if (location != "") {
//     var get_location = { "location": location};
//     $.ajax({
//       url: "parking_map",
//       method: "POST",
//       headers: {
//           "Content-Type":"application/json"
//       },
//       dataType: "json",
//       data: JSON.stringify(get_location), 
//     });
//   }
// });


