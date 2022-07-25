# Beechat Hive -  _The Beechat to XMPP bridge_

## Current features
1. Turn the XMPP message forwarder on
2. Display data on screen

## Diagram of operation
[![img](https://raw.githubusercontent.com/BeechatNetworkSystemsLtd/BeechatHive/main/diagram.png)]()

## Hardware requirements
- Any Raspberry Pi
- Beechat Clip radio
- an XMPP account

## Features coming soon:
* Send and receive XMPP or Beechat text messages via the Web UI
    
## Setup: ##


**[RASPBERRY PI SETUP]** 
1. download the Raspbian Imager from here: https://www.raspberrypi.com/software/
2. After executing Raspbian Imager, go to advanced options via the GUI and 
    (1) enable SSH 
    (2) set the user to "beechat" 
    (3) configure a Wi-fi network. That way, on the first boot you can ssh into it with ```ssh beechat@IP_OF_RPI_HERE```. 
3. Once you've booted in, it is very useful to make your Hive reachable from a .local network domain rather than an IP. So, instead of ```ssh beechat@192.168.1.57``` you would use ```ssh beechat@beechathive.local```. If you wish to do this do the following (make sure you use a different host name for every Hive) :
    *  ``` sudo apt-get install avahi-utils ```
    *  ``` sudo nano /etc/avahi/avahi-daemon.conf```
    *  Uncomment the line starting with **host-name=** and add your domain such as "beechathive" (without quotes).
    *  ```sudo  service avahi-daemon restart```
    *  ```service avahi-daemon status``` If the last line says: _"Server startup complete. Host name is"_ then it was successful.


**[NEXT STEPS]**
- Download beechat Hive code and unzip to /home/beechat (or your user):
  - ```wget https://github.com/BeechatNetworkSystemsLtd/BeechatHive/archive/refs/heads/main.zip```
  - ```unzip main.zip```
-   **~/BeechatHive-main/flask_auth_app/project/__ init__.py**: Set your server's database password here
-   **~/BeechatHive-main/flask_auth_app/project/xsend.txt**: set your XMPP credentials here.
-   Provide user with access permissions to the radio device (replace "beechat" for your username):
    - ```sudo usermod -a -G dialout beechat```   

**Install requirements (needed on first run only)**
```
python3 -m pip install flask flask-sqlalchemy flask-login xmpppy digi-xbee
```

**Create database (needed on first run only)**

Go into the folder called /flask_auth_app/, then start python by typing ```python``` into terminal then [ENTER]:

```
from project import db, create_app, models
```
```
db.create_all(app=create_app())
```

Exit with ```exit()```




**Create SSL keys for the web app (needed on first run only):**
Within the ```flask_auth_app``` folder: 
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

**Run app**
Use the included ```start.sh``` script within the ```flask_auth_app folder```:
``` ./start.sh```


**Great thanks to**
https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

## Development

Want to contribute? Great, make a pull request!

## License

GPLv2
