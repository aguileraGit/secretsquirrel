
### Clone repo
```git clone git@github.com:aguileraGit/secretsquirrel.git```

### Running Flask Server as a service
Create service file. `sudo touch /etc/systemd/system/flaskServer.service`

Add the following text to the file. `sudo nano /etc/systemd/system/flaskServer.service`
```
[Unit]
Description=Run Flask Server
After=network.target

[Service]
Type=simple
Restart=always
User=pi
WorkingDirectory=/home/pi/secretsquirrel
ExecStart=/usr/bin/python3 /home/pi/secretsquirrel/app.py

[Install]
WantedBy=multi-user.target
```

Start the service. `sudo systemctl start flaskServer`

Enable the service after reboots. `sudo systemctl enable flaskServer`


### Browser
Configure browser to start when `pi` user logins. Chromium runs in *kiosk* mode. This prevents buttons from showing. 

Create file
`touch /home/pi/.config/autostart/chromeAutoStart.desktop`

Add text below to file. `nano /home/pi/.config/autostart/chromeAutoStart.desktop`

```
[Desktop Entry]
Type=Application
Name=StartBrowser
Exec=chromium-browser http://192.168.1.104:5000 --kiosk
```

### Disable screen from sleeping
Need to disable the screen from going to sleep
Script is already included in repo. `disableScreenSaver.sh`
Make it executable. `chmod +x /home/pi/disableScreenSaver.sh`
Create a file to autostart the script. `/home/pi/.config/autostart`
Add the following
```
[Desktop Entry]
Type=Application
Name=Disable screen screensaver
Exec="/home/pi/disableScreenSaver.sh"
```
