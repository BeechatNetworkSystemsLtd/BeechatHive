#Try to connect to WiFi
#To disable hotspot and reconnect to WiFi: 

#sudo nano /etc/dhcpcd.conf : comment the lines at the bottom
#sudo systemctl stop hostapd.service
#sudo systemctl restart dhcpcd


#Detect if connected to the Internet:
#curl -I https://beechat.network/


#If yes, start flask app
#cd /home/beechat/BeechatHive-main/flask_auth_app
#./start.sh

#If no, set up hotspot, and then start flask app
#sudo nano /etc/dhcpcd.conf : uncomment the lines at the bottom
#sudo systemctl start hostapd.service
#sudo systemctl restart dhcpcd

#cd /home/beechat/BeechatHive-main/flask_auth_app
#./start.sh


import os
import sys
from time import sleep, time
import requests
import subprocess

#Detect if hotspot is disabled
#If it is disabled, check if we have an internet connection
#If we don't have an internet connection, enable hotspot

source_file="/etc/dhcpcd.conf"

f = open(source_file, "r")
contents = f.read()

string_hotspot_disabled= "#interface wlan0"
string_hotspot_disabled2= "#static ip_address=192.168.0.1/24"
string_hotspot_disabled3= "#nohook wpa_supplicant"

string_hotspot_enabled = "interface wlan0"
string_hotspot_enabled2 = "static ip_address=192.168.0.1/24"
string_hotspot_enabled3 = "nohook wpa_supplicant"


hotspot_status = True #True means hotspot is enabled


if string_hotspot_disabled in contents:
    if string_hotspot_disabled2 in contents:
        if string_hotspot_disabled3 in contents:
            print("Hotspot is disabled")
            hotspot_status = False
        else:
            hotspot_status = True
    else:
        hotspot_status = True
else:
    hotspot_status = True

if(hotspot_status):
    print("Hotspot is enabled")
    subprocess.Popen(["sudo mv /etc/dhcpcd.conf.bak /etc/dhcpcd.conf" ], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process6 finished\n")
    f.close()
    subprocess.Popen(["sudo systemctl disable hostapd.service" ], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process7 finished\n")
    f.close()
    subprocess.Popen(["sudo systemctl stop hostapd.service" ], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process8 finished\n")
    f.close()
    subprocess.Popen(["sudo systemctl restart dhcpcd"], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process9 finished\n")
    f.close()
    #Let's disable it
    

#Check for internet connection
def connected_to_internet(url="https://beechat.network/", timeout=5):
    try:
        _ = requests.head(url,timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No Internet connection available.")
    return False
    
connected = connected_to_internet()

if(connected):
    print("No problems detected, start app normally")
    process1 = subprocess.Popen(["/bin/bash /home/beechat/BeechatHive-main/flask-auth-app/start.sh" ], shell=True).wait()    

else:
    print("Internet not detected, starting hotspot")
    contents2 = contents #backup original data

    #Enable hotspot
    contents2 = contents2.replace(string_hotspot_disabled,string_hotspot_enabled)
    contents2 = contents2.replace(string_hotspot_disabled2,string_hotspot_enabled2)
    contents2 = contents2.replace(string_hotspot_disabled3,string_hotspot_enabled3)

    #print(contents2)
    print("Hotspot enabled")
    hotspot_status = True
    
    

    #write contents2 to file
    f = open("new_dhcpcd.conf", "w")
    f.write(contents2)
    f.close()

    #move old conf to backup file
    process1 = subprocess.Popen(["sudo mv /etc/dhcpcd.conf /etc/dhcpcd.conf.bak" ], shell=True).wait()
    
    
    f = open("/home/beechat/debug.log", "w")
    f.write("process1 finished\n")
    f.close()

    #move file to proper location
    subprocess.Popen(["sudo mv /home/beechat/new_dhcpcd.conf /etc/dhcpcd.conf" ], shell=True).wait()

    f = open("/home/beechat/debug.log", "a")
    f.write("process2 finished\n")
    f.close()

    

    #sudo systemctl start hostapd.service
    subprocess.Popen(["sudo systemctl enable hostapd.service" ], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process3 finished\n")
    f.close()

    subprocess.Popen(["sudo systemctl start hostapd.service" ], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process4 finished\n")
    f.close()
    
    subprocess.Popen(["sudo systemctl restart dhcpcd"], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process5 finished\n")
    f.close()

    


sleep(480)
f = open("/home/beechat/debug.log", "a")
f.write("slept for 480s\n")
f.close()

#Now we will disable the hotspot 
if(hotspot_status):
    #move old conf to backup file
    subprocess.Popen(["sudo mv /etc/dhcpcd.conf.bak /etc/dhcpcd.conf" ], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process6 finished\n")
    f.close()
    subprocess.Popen(["sudo systemctl disable hostapd.service" ], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process7 finished\n")
    f.close()
    subprocess.Popen(["sudo systemctl stop hostapd.service" ], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process8 finished\n")
    f.close()
    subprocess.Popen(["sudo systemctl restart dhcpcd"], shell=True).wait()
    f = open("/home/beechat/debug.log", "a")
    f.write("process9 finished\n")
    f.close()