# Beechat Hive -  _The Beechat to XMPP bridge_

## Current features
1. Turn the XMPP message forwarder on
2. Display data on screen

## Diagram of operation
[![img](https://raw.githubusercontent.com/BeechatNetworkSystemsLtd/BeechatHive/main/diagram.png)]()

## Hardware requirements
- Any Linux computer (such as Raspberry Pi, a desktop/laptop will also work)
- Beechat Clip radio [[LINK]](https://beechat.network/)
- an XMPP account

## Features coming soon:
* Receive and view XMPP or Beechat text messages via the Web UI. (Only sending works right now)
    
## Setup: ##


**[MAIN STEPS]**

**(1) Download the Beechat Hive code and unzip to /home/beechat (or your user):**
  - ```wget https://github.com/BeechatNetworkSystemsLtd/BeechatHive/archive/refs/heads/main.zip```
  - ```unzip main.zip```

**(2) Set your server's database password within the file:**
   ```~/BeechatHive-main/flask_auth_app/project/__ init__.py```

**(3) Set your XMPP credentials:**
   ```~/BeechatHive-main/flask_auth_app/xsend.txt```

**(4) Provide user with access permissions to the radio device (replace "beechat" for your username):**
```
sudo usermod -a -G dialout beechat
```

**(5) Install requirements (needed on first run only)**
```
python3 -m pip install flask flask-sqlalchemy flask-login xmpppy digi-xbee
```
**(6) Run the setup.py script located within ```flask_auth_app``` folder(needed on first run only)**

```
python3 setup.py
```


**(7) Create SSL keys for the web app (needed on first run only):**
Within the ```flask_auth_app``` folder: 
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

**(8) Run app**
Use the included ```start.sh``` script within the ```flask_auth_app``` folder:
``` ./start.sh```


**Great thanks to**
https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

## Development

Want to contribute? Great, make a pull request!

## License

GPLv2
