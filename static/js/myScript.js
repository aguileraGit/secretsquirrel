//Set interval to check for new data
var myVar = setInterval(checkForNewLine, 3000);

//Track sreensave
var go = true;

function timer() {
  //Paused - bail!
  if(!go)
      return;
  //Enable screensaver
  screenSaverON();
  setTimeout(timer, 5000);
}

function stopTimer(){
    go = false;
}

function startTimer(){
    go = true;
    timer();
}

//Call Flask backend for data
function checkForNewLine() {
  console.log('Checking for data');

  var currentText = document.getElementById("gistLine").innerHTML;
  var flaskUrl = "http://192.168.1.10:5000/checkGist?webFrontEnd=" + currentText;
  //console.log(flaskUrl)

  $.ajax({
    url: flaskUrl,
    success: function(result) {

      if (result["newData"] == "True") {
        console.log("New Data Found")
        //Quick turn off display
        screenSaverON()

        //Get data type
        dataType = result["type"]

        if (dataType == 'text') {
          formatDivText( result["data"] );

        } else if (dataType == 'image') {
          formatDivImage( result["data"] );

        } else if (dataType == 'video') {
          formatDivVideo( result["data"] )
        } else {
          document.getElementById("gistLine").innerHTML = 'Unknown data type'
        }

        //Show notification
        showNotification()
      }

      else if(result["newData"] == 'False'){
        console.log('No new data found')
      }
    }
  });
}

//Format for Text
function formatDivText(gistLine) {
  //Count number of characters
  var gistLineLen = gistLine.length;
  console.log(gistLineLen)

  //Remove formatting
  $("#formatDiv").removeClass();

  //Remove any HTML from div
  if (document.getElementById("gistImage")) {
    document.getElementById("gistImage").innerHTML = "";
  }

  //Ensure gistLine div is visible
  $("#gistLine").show();

  //Format Div: formatDiv depending on the number
  if (gistLineLen < 40){
    document.getElementById('formatDiv').classList.add('display-3');
  } else if(gistLineLen >=40 && gistLineLen < 80){
    document.getElementById('formatDiv').classList.add('display-4');
  } else if(gistLineLen >=80 && gistLineLen < 120){
    document.getElementById('formatDiv').classList.add('h2');
  } else if(gistLineLen >=120 && gistLineLen < 160){
    document.getElementById('formatDiv').classList.add('h4');
  }

  //Update Text
  document.getElementById("gistLine").innerHTML = gistLine;
}

//Format for Image
function formatDivImage(gistLine) {
  //Unsure how to size image!?

  //Copy link from gistLine and embed in div
  var imageLink = "<div id=\"gistImage\"><img src=\"" + gistLine + "\" class=\"img-fluid\"></div>";
  var resetDivGistLine = "<div id=\"gistLine\">" + gistLine + "</div>";

  //Add HTML (image + Div w/ text)
  document.getElementById("formatDiv").innerHTML = imageLink + resetDivGistLine;

  //Hide the gistLine div
  $("#gistLine").hide();
}

//Format for Video
function formatDivVideo(gistLine) {
  //Not implemented - No audio!
  ;
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

  //Stop Timer
  stopTimer();

  //Wait and re-enable
  setTimeout(function() {
    //Restart when done
    startTimer();
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
