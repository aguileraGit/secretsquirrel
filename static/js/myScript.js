//Bottom of page has page load init stuff

//Clock variable
var clock;

//Set interval to check for new data
var myVar = setInterval(checkForNewLine, 20000);

var newData = false;

//Timer function runs continously if go is true. It must be restarted is stopped.
//To restart, call startTimer function
function timer() {
  //Paused - bail!
  if(!go)
      return;

  //Force screensaver on every second
  screenSaverON();

  //If no new data (screen has been clicked), show clock
  //No need to show notifcation. Already has been set.
  if(!newData){
    showClock();
  }
  //Wait and run timer again
  setTimeout(timer, 1000);
}

function stopTimer(){
  console.log('Stop Timer')
  go = false;
}

function startTimer(){
  console.log('Start Timer')
  go = true;
  timer();
}

//Checks Flask backend for data. This is an governed by an interval.
// If data is found, one of the functions is called to process the data:
//  formatDivText
//  formatDivImage
//  formatDivVideo - not implemented
function checkForNewLine() {
  console.log('Checking for data');

  var currentText = document.getElementById("gistLine").innerHTML;
  var flaskUrl = "http://192.168.1.104:5000/checkGist?webFrontEnd=" + currentText;
  //console.log(flaskUrl)

  $.ajax({
    url: flaskUrl,
    success: function(result) {

      if (result["newData"] == "True") {
        console.log("New Data Found")

        //Quickly turn off display
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
        hideClock()

        //Fresh data. New data.
        newData = true;
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

//Turn the screen black. I refer to this as the 'Screen Saver'
function screenSaverON() {
  document.getElementById("overlay").style.display = "block";
}

//Turn off the screensaver
function screenSaverOFF() {
  //Turn off screensaver
  document.getElementById("overlay").style.display = "none";

  //Screen has been clicked. Data isn't new anymore.
  newData = false;

  //Hide notification
  hideNotification()

  //Hide Clock
  hideClock()

  //Stop Timer
  stopTimer();

  //Wait and re-enable
  setTimeout(startTimer, 10000);
}

function hideNotification() {
  document.getElementById("notify").style.display = "none";
}

function showNotification() {
  document.getElementById("notify").style.display = "block";
}

function hideClock() {
  document.getElementById("clock").style.display = "none";
}

function showClock() {
  document.getElementById("clock").style.display = "block";
}

//Page load events
window.addEventListener('load', function() {
  //Init blank sceen
  document.getElementById("overlay").style.display = "block";

  //Start clock
  clock = $('.clock').FlipClock({
    clockFace: 'TwentyFourHourClock',
    showSeconds: false
  });

  //No new data yet...
  newData = false;

});
