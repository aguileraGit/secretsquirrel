//Set interval to check for new data
var myVar = setInterval(checkForNewLine, 3000);


//Want to keep the screen off as much as possible. Keep turning it off.
var restartScreenSaver = setInterval(screenSaverON, 5000)


//Call Flask backend for data
function checkForNewLine() {
  console.log('Checking for data');

  $.ajax({
    url: "http://192.168.1.102:5000/checkGist",
    success: function(result) {

      if (result["newData"] == "True") {
        //Quick turn off display
        screenSaverON()
        //Update Text
        document.getElementById("gistLine").innerHTML = result["data"];
        //Show notification
        showNotification()
      }
    }
  });
}

//Turn the screen blank - 'Screen Saver'
function screenSaverON() {
  document.getElementById("overlay").style.display = "block";
}

//Turn off the screensaver
function screenSaverOFF() {
  //Turn off screensaver
  document.getElementById("overlay").style.display = "none";

  //Hide notification
  hideNotification()

  //Stop screensaver
  clearInterval(restartScreenSaver);

  //Wait
  setTimeout(function() {
    //Restart when done
    restartScreenSaver = setInterval(screenSaverON, 5000)
  }, 10000);
}

function hideNotification() {
  document.getElementById("notify").style.display = "none";
}

function showNotification() {
  document.getElementById("notify").style.display = "block";
}

//Page load events
window.addEventListener('load', function() {

  screenSaverON()
  showNotification()

});