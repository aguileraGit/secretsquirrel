



### Browser
Configure browser to start when `pi` user logins. Chromium runs in *kiosk* mode. This prevents buttons from showing. 

Create file
`touch /home/pi/.config/autostart/chromeAutoStart.desktop`

Add text below to file. `nano /home/pi/.config/autostart/chromeAutoStart.desktop`

```
[Desktop Entry]
Type=Application
Name=StartBrowser
Exec=chromium-browser http://192.168.1.14:5000 --kiosk
```
