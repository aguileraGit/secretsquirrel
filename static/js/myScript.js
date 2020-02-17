//Set interval to check for new data
var myVar = setInterval(checkForNewLine, 3000);


//Want to keep the screen off as much as possible. Keep turning it off.
var restartScreenSaver = setInterval(screenSaverON, 5000)


//Call Flask backend for data
function checkForNewLine() {
  console.log('Checking for data');

  var currentText = document.getElementById("gistLine").innerHTML;
  var flaskUrl = "http://192.168.1.104:5000/checkGist?webFrontEnd=" + currentText;
  console.log(flaskUrl)
    
  $.ajax({
    url: flaskUrl,
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
  console.log('Enable screensaver')
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

  console.log('Waiting to turn off screensave - 10 seconds')
    
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

  //Init blank sceen
  document.getElementById("overlay").style.display = "block";
  showNotification()

});
