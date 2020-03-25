from flask import Flask, render_template, jsonify, request
from flask_apscheduler import APScheduler
from enum import Enum
import re
import datetime
import github

# Credential file always has the same format
# Github Token
# Github Gist Name
# Github Gist ID
CREDENTIALS_FILE_V2 = 'appCreds.txt'


app = Flask(__name__)

class gistTypeOptions(Enum):
    text = 1
    image = 2
    video = 3

class appFunctions:
    def __init__(self, credentialFile):
        self.gistOldLine = 'Love ya!'
        self.gistLine = None
        self.gistNewData = True

        self.credentialFile = credentialFile

        self.gh = None

    #Login using token. Returns True or False.
    def githubLogin(self):
        #Look for credentialsFile - returns 0 if OK
        if self.verifyCredentialFile() == False:
            return False

        #Read credentials file and get token
        token = self.readCredentialsToken()

        #Login
        self.gh = None
        self.gh = github.Github(token)

        #Unsure this is the best way to know if a user is actually logged in
        #print('Debug - githubLogin - login:', self.gh)

        #Check if we've logged in
        if self.gh:
            #print('Debug - initGitHub - Logged in')
            return True
        else:
            print('Debug - initGitHub - Error Logging in')
            return False


    def createGist(self, gistName):
        #Define gist name and content
        files = { str(gistName) : github.InputFileContent('Hello Beautiful!') }
        descriptionStr = 'Gist for sending Love Messages'

        #Create gist
        gistReturn = self.gh.get_user().create_gist(False, files, descriptionStr)

        #Get ID
        gistID = gistReturn.id
        return gistID


    def readGist(self):
        #Get gist text
        gistText = self.gh.get_gist( self.readCredentialsGistID() ).files[self.readCredentialsGistName()].content
        return gistText


    def verifyCredentialFile(self):
        try:
            self.readCredentialsToken()
        #Assume Exception is missing file
        except:
            print('Unable to read file')
            return False

        return True

    def readCredentialsToken(self):
        with open(self.credentialFile, 'r') as fd:
            token = fd.readline().strip()
        return token


    def readCredentialsGistName(self):
        with open(self.credentialFile, 'r') as fd:
            token = fd.readline().strip()
            gistName = str(fd.readline().strip() )
        return gistName


    def readCredentialsGistID(self):
        with open(self.credentialFile, 'r') as fd:
            token = fd.readline().strip()
            gistName = str(fd.readline().strip() )
            gistID = str(fd.readline().strip() )
        return gistID


    #Write single line to file
    def writeCredentialsLine(self, token, gistName, gistID=None):
        with open(self.credentialFile, 'w+') as fd:
            fd.write(str(token) + '\n')
            fd.write(str(gistName) + '\n')

            if gistID:
                fd.write(str(gistID) + '\n')


    def addCredentialsGistID(self, gistID):
        token = self.readCredentialsToken()
        gistName = self.readCredentialsGistName()

        self.writeCredentialsLine(token, gistName, gistID)


#Start Love Box Function with credential file
loveBox = appFunctions(CREDENTIALS_FILE_V2)

#Setup Scheduler to check Github for updates
scheduler = APScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True


# Schedule task to check for new data on gist
@scheduler.task('interval', id='tskCheckGist', seconds=(2*60), misfire_grace_time=900)
def checkGistBackgroundTask():
    print('Fn: checkGistBackgroundTask')

    if loveBox.githubLogin() == False:
        print('Debug checkGistBackgroundTask - Unable to login')

    else:
        gistText = loveBox.readGist()
        #print('Debug - checkGistBackgroundTask - gistText: ', gistText)

        print('GitHub: {} - {}'.format(gistText, type(gistText)))
        print('gistOldLine: {} - {}'.format(loveBox.gistOldLine, type(loveBox.gistOldLine)))
        print('loveBox.gistLine: {} - {}'.format(loveBox.gistLine, type(loveBox.gistLine)))

        #Compare against old line. Update if new data
        if gistText != loveBox.gistOldLine:
            loveBox.gistNewData = True
            loveBox.gistLine = gistText
            print('Updating gistLine...')


#checkGist will recieve the latest text from website
@app.route('/checkGist', methods=['GET', 'POST'])
def checkGist():
    #Setup return dict
    toReturn = {'newData': 'False',
                'data': 'None',
                'type': 'None'}

    #Get latest gistLine from the website.
    websiteCurrent = request.args.get('webFrontEnd', 0)

    print('WebsiteCurrent: {} - {}'.format(websiteCurrent, type(websiteCurrent)))
    print('gistOldLine: {} - {}'.format(loveBox.gistOldLine, type(loveBox.gistOldLine)))
    print('loveBox.gistLine: {} - {}'.format(loveBox.gistLine, type(loveBox.gistLine)))

    #See if website (Front/Back end) is out of sync str(bytes_string, 'utf-8')
    if loveBox.gistLine not in websiteCurrent:
        print('Website needs update. Current: ', websiteCurrent)
        loveBox.gistNewData = True

    #Updated content
    if loveBox.gistNewData:
        #Determine the type (text, picture, video)
        gistType = determineGistType( str(loveBox.gistLine) )

        toReturn['newData'] = 'True'
        toReturn['data'] = str(loveBox.gistLine)
        toReturn['type'] = str(gistType.name)

        #Update
        loveBox.gistOldLine = loveBox.gistLine
        loveBox.gistNewData = False
    else:
        toReturn['newData'] = 'False'

    return jsonify(toReturn)


#Gist can be line of text, image, or youtube video
#Return type and line
def determineGistType(gistLineInQuestion):
    regexImage = r"(?:https?:\/\/)?(?:(\w+)\.){1,}\w+(?:\/.*){1,}\.(?:jpg|gif|png)"
    regexVideo = r"(?:https?:)?(?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/\S*?[^\w\s-])((?!videoseries)[\w-]{11})(?=[^\w-]|$)(?![?=&+%\w.-]*(?:['\"][^<>]*>|<\/a>))[?=&+%\w.-]*"

    #Default to type being text
    gistType = gistTypeOptions.text
    gistText = str(gistLineInQuestion)

    #Search for image
    match = re.search(regexImage, gistLineInQuestion, re.IGNORECASE | re.MULTILINE)
    if match:
        gistType = gistTypeOptions.image
        gistText = str(match.group(0))

    #Search for video
    match = re.search(regexVideo, gistLineInQuestion, re.IGNORECASE | re.MULTILINE)
    if match:
        gistType = gistTypeOptions.video
        gistText = str(match.group(0))

    return gistType


#Github is dropping user/pass support in library. New methold will require
# user to sign into Github and create New Personal Token. And copy the Token
# into the app. Token will override old token
@app.route('/initGitHub', methods=['POST'])
def initGitHub():
    print('Debug - initGitHub')
    #Get form Token and gist name
    if request.method == 'POST':
        results = request.form.to_dict()

    #Get token and gist name - Need to update page to force user to enter both
    newToken = str(results['gitHubToken'])
    newGistName = str(results['gistName'])

    print('Debug - initGitHub - newToken: ', newToken)
    print('Debug - initGitHub - newGistName: ', newGistName)

    #Write token and gist name
    loveBox.writeCredentialsLine(newToken, newGistName)

    #Check to see if we can login
    if loveBox.githubLogin() == False:
        print('Unable to login')
        #Maybe update the page with error?
        return render_template('index.html')

    #Create gist
    gistID = loveBox.createGist(newGistName)
    loveBox.addCredentialsGistID(gistID)

    #Left off here
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def displayWebPage():
    return render_template('index.html')


#Update text before starting app
checkGistBackgroundTask()

#Start Flask App
if __name__ == '__main__':

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    #Call config
    app.config.from_object(Config())

    #Start scheduler
    scheduler.init_app(app)
    scheduler.start()

    #Run the damn thing
    app.run(host='0.0.0.0', debug=True, port=5000)
