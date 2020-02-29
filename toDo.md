## Still to do...

General
- [ ] ~~Try to get fades to work~~ I don't think this is actually possible.
- [x] Call some kind of default message
- [x] Switch to GitHub tokens
- [x] Move to google fonts
- [x] Publish to Github
- [x] Ignore password file
- [ ] Move away from multiple Github libraries if possible.

OS
- [x] Setup rPi - https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
- [x] Load OS
- [x] Wifi
- [x] Setup display https://github.com/pimoroni/hyperpixel4 - Weirdly Square - Pi 3B+ or older
- [x] Load browser without buttons (--kiosk)
- [x] Autoload browser on boot
- [ ] Control backlight using Python
- [ ] Look @ /etc/rc.local -> I believe I have extra stuff to remove
- [ ] Stop Desktop from loading. It takes up too many resources.
 - *Newer* https://www.raspberrypi.org/forums/viewtopic.php?t=255635
 - https://www.raspberrypi.org/forums/viewtopic.php?t=42888
 - https://www.raspberrypi.org/forums/viewtopic.php?t=73585
 - Google: raspberry pi start single gui without desktop

3D Print case
- [x] Holes need to be updated
- [ ] I believe the *Display* model is off from edge to stand offs
- [ ] Needs to be made into one piece (Mari made a comment today that makes me think I really need to do this)

ReadMe/Documentation
- [ ] Set up rPi wifi/ssh/raspbian OS
- [ ] Add link for setup display https://github.com/pimoroni/hyperpixel4 - Weirdly Square - Pi 3B+ or older
- [ ] Update ReadMe to include general statement about the interaction with Github
- [ ] Link for Github ssh setup - https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
- [ ] Removal instructions
- [ ] Move readMe scripts to new folder. -> Make it copy/permissions
- [ ] Update documentation if moving away from Startx (Desktop)

Features
- [ ] Add images/movies. Use regex to capture jpg/jpeg/gif/svg or link to youtube and embed.
 - https://regex101.com/r/XblFpm/1
 - https://regex101.com/r/OY96XI/5
- [ ] Turn off display at night
