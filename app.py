from flask import Flask, render_template, jsonify, request
from flask_apscheduler import APScheduler
from github3 import login
from github3 import authorize
import datetime

from github import Github

gistOldLine = 'Love ya!'
gistLine = None
gistNewData = True
gistError = None

CREDENTIALS_FILE = 'valentinesCreds.txt'

app = Flask(__name__)

#Setup Scheduler to check Github for updates
scheduler = APScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True


# Schedule task to check for new data on gist
@scheduler.task('interval', id='tskCheckGist', seconds=(2*60), misfire_grace_time=900)
def checkGistBackgroundTask():
    print('Checking Gist')
    #Set variables to global
    global gistNewData
    global gistOldLine
    global gistLine
    
    #Make sure a Credential file exists and contains token and id
    try:
        token = id = ''
        with open(CREDENTIALS_FILE, 'r') as fd:
            token = fd.readline().strip()
            id = int( fd.readline().strip() )
            gistID = str(fd.readline().strip() )
            
        #Login            
        gh = login(token=token)

        #Get all gists
        gists = [g for g in gh.gists()]

        #Sort all gists
        for g in gists:
            #Get the right gist
            if g.id == gistID:
                rawLine = str(g.files['valentinesDay'].content()).strip()

        #Compare against old line. Update if new data
        if rawLine != gistOldLine:
            gistNewData = True
            gistLine = rawLine.strip()
            
    except Exception as e:
        
        print('Background Exception: ', e)
        gistLine = e
        gistNewData = True
    #Try and different exception to know when to login
    #401 Bad credentials
    #[Errno 2] No such file or directory: 'valentinesCreds.txt'

#checkGist will recieve the latest text from website    
@app.route('/checkGist', methods=['GET', 'POST'])  
def checkGist():
    #Setup return dict
    toReturn = {'newData': 'False',
                'data': 'None'}

    #Set variables to global
    global gistNewData
    global gistOldLine
    global gistLine
    
    #Get latest gistLine from the website.
    try:
        websiteCurrent = request.args.get('webFrontEnd', 0)
        
        #print('Website: ', websiteCurrent)
        #print('gistLine: ', gistLine)
        #print('gistOldLine: ', gistOldLine)
        
        #See if website (Front/Back end) is out of sync str(bytes_string, 'utf-8')
        if websiteCurrent != gistLine:
            print('Website needs update. Current: ', websiteCurrent)
            
            gistNewData = True

    except Exception as e:
        print('Exception: ',e)
                
    
    if gistNewData:
        toReturn['newData'] = 'True'
        toReturn['data'] = str(gistLine)
        
        #Update globals
        gistOldLine = str(gistLine)
        gistNewData = False

    return jsonify(toReturn)



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def displayWebPage():
    return render_template('index.html')
    
  
#Inital Login to Github
#Setups gist and token
@app.route('/initAuthGitHub', methods=['POST'])
def initAuthGitHub():
    print('Auth Time')
    
    #Get Github login info
    if request.method == 'POST':
        results = request.form.to_dict()

    user = results['githubLogin']
    password = results['githubPassword']

    #Need to do some better error handling
    #while not password:
    #    password = getpass('Password for {0}: '.format(user))

    #Define scopes and note name
    note = 'Valentines Day Gist App'
    scopes = ['user', 'gist']
    
    #Connect to Github
    try:
        auth = authorize(user, password, scopes, note)
        
        #Write token and ID to file to read later.
        with open(CREDENTIALS_FILE, 'w+') as fd:
            fd.write(str(auth.token) + '\n')
            fd.write(str(auth.id) + '\n')

        auth.delete()

    except Exception as e:
        #Github API throws up exception, but still creates the API token
        #Ignoring it for now. Will look at later.
        print(e)
        
    print('Done creating token')

    #Login using token
    try:
        token = id = ''
        with open(CREDENTIALS_FILE, 'r') as fd:
            token = fd.readline().strip()
            id = int( fd.readline().strip() )
        
        print('Token read')
        
        #Login            
        gh = login(token=token)
        print(gh)
        #auth = gh.authorization(id)
        
        print('Logged in with token!')
    
        #DummyText for testing
        dateNowStr = datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
    
        #Create gist
        
        files = {
        'valentinesDay' : {
            'content': dateNowStr
            }
        }

        gist = gh.create_gist('gistName', files, public=False)
        
        print('Created gist')
        
        # gist == <Gist [gist-id]>
        print(gist.html_url)
        
        gistID = gist.html_url.split('/')[-1]
        with open(CREDENTIALS_FILE, 'a') as fd:
            fd.write(str(gistID) + '\n')
        
    except Exception as e:
        print(e)
        
    finally:
        #Reload page
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
    app.run(host='192.168.1.104', debug=True, port=5000)
