##Setup script for the project
#This script will edit working paths within the files
#To change:

# ./project/main.py: line 19
# subprocess.Popen(['/bin/python3 /home/beechat/BeechatHive-main/flask_auth_app/project/receiver.py'], shell=True)

# ./project/main.py: line 24
# subprocess.Popen(["sh /home/beechat/BeechatHive-main/flask_auth_app/project/killradio.sh"], shell=True)

# ./project/main.py: line 38
# print("/bin/python3 /home/beechat/BeechatHive-main/flask_auth_app/project/sender.py \"<G>"+gateway+"</G><T>"+ xmppaddress +"</T><M>"+ message+"</M>\"")

# ./project/main.py: line 40
# subprocess.Popen(["/bin/python3 /home/beechat/BeechatHive-main/flask_auth_app/project/sender.py \"<G>"+gateway+"</G><T>"+ xmppaddress +"</T><M>"+ message+"</M>\"" ], shell=True)



# Import the os module
import os

# Get the current working directory
cwd = os.getcwd()

# Print the current working directory
print("Current working directory: {0}".format(cwd))


#input file
fin = open(cwd+"/project/main.py", "rt")
#output file to write the result to
fout = open(cwd+"/project/main.py.out", "wt")
#for each line in the input file
for line in fin:
	#read replace the string and write to output file
	fout.write(line.replace('/home/beechat/BeechatHive-main/flask_auth_app/', cwd+"/"))
#close input and output files
fin.close()
fout.close()

#Delete old file
myfile= cwd+"/project/main.py"

## Try to delete the file ##
try:
    os.remove(myfile)
except OSError as e:  ## if failed, report it back to the user ##
    print ("Error: %s - %s." % (e.filename, e.strerror))
#Rename new file
os.rename(cwd+"/project/main.py.out",cwd+"/project/main.py")

from project import db, create_app, models
db.create_all(app=create_app())

#Setup WiFi Hotspot

#sudo nano /etc/dhcpcd.conf
    #interface wlan0
    #static ip_address=192.168.0.1/24  <-sets the IP of the RPi hotspot
    #nohook wpa_supplicant

#sudo nano /etc/dnsmasq.conf
    #interface=wlan0
    #listen-address=192.168.0.1
    #bind-interfaces 
    #server=8.8.8.8
    #domain-needed
    #bogus-priv
    #dhcp-range=192.168.0.2,192.168.0.30,255.255.255.0,24h <- dictates which IP range is provided to the wlan0 interface, in this case from 192.168.0.2 to ...30
    #no-hosts
    #addn-hosts=/etc/hosts.dnsmasq

#sudo nano /etc/hosts.dnsmasq
    #192.168.0.1 beechatgateway <- set a hostname

#sudo nano /etc/network/interfaces
    #auto wlan0
    #iface wlan0 inet static
    #address 192.168.0.1
    #netmask 255.255.255.0

#sudo nano /etc/hostapd/hostapd.conf <- this file sets up the details for the WiFi Hotspot, such as SSID and password
    #interface=wlan0
    #driver=nl80211
    #hw_mode=g
    #channel=7
    #wmm_enabled=0
    #macaddr_acl=0
    #auth_algs=1
    #ignore_broadcast_ssid=0
    #wpa=2
    #wpa_key_mgmt=WPA-PSK
    #wpa_pairwise=TKIP
    #rsn_pairwise=CCMP
    #ssid=NETWORK
    #wpa_passphrase=PASSWORD

#sudo nano /etc/default/hostapd <- needs to point to previous file
    #DAEMON_CONF="/etc/hostapd/hostapd.conf" <- uncomment


#To disable hotspot and reconnect to WiFi: 
#sudo nano /etc/dhcpcd.conf : comment the lines at the bottom
#sudo systemctl stop hostapd.service
#sudo systemctl restart dhcpcd

#To enable hotspot:
#sudo nano /etc/dhcpcd.conf : uncomment the lines at the bottom
#sudo systemctl start hostapd.service
#sudo systemctl restart dhcpcd
