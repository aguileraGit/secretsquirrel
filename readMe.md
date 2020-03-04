Directions are for a Raspberry Pi Zero W

### Setup RPi 

[Install Raspbian Buster Lite](https://www.raspberrypi.org/downloads/raspbian/). Do not install GUI!

[Setup headless - SSH & Wireless](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)

Setup to autologin.
`sudo raspi-config`

### Setup Router for static IP
The server will need a static IP. 

### Install PIP and packages
 - Pip3: install pip - sudo apt install python3-pip
 - Python modules: pip3 install flask flask_apscheduler PyGithub github3.py --user
 
### Setup Display
[HyperPixel](https://github.com/pimoroni/hyperpixel4). Select Weirdly Square - Pi 3B+ or older

### Install X11
`sudo apt-get install xserver-xorg-video-all xserver-xorg-input-all xserver-xorg-core xinit x11-xserver-utils`

### Start X11
Edit `.bash_profile`. Create with `touch .bash_profile` if it doesn't exist.
```
if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then
startx
fi
```
### Install Chromium and unclutter
`sudo apt-get install chromium-browser`

Unclutter removes mouse pointer
`sudo apt-get install unclutter`

###
Edit or add `.xinitrc` with the following text. Be sure to update your IP. 
```
#!/bin/sh
xset -dpms
xset s off
xset s noblank

unclutter &
chromium-browser http://192.168.1.104:5000 --start-fullscreen --kiosk --no-first-run --fast --noerrdialogs --disable-session-crashed-bubble --disable-infobars --window-size=720,720
```

### Make preformance improvement
Do not skip this step. Rpi Zero W will run super slow without them.
Install optimized version of Chromium
`sudo apt install rpi-chromium-mods`

Increase swap size
`sudo nano /etc/dphys-swapfile` update to `CONF_SWAPFILE=256`
 
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


