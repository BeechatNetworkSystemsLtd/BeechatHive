#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import qrcode
from digi.xbee.devices import XBeeDevice
#import xmpp
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import bluetooth, subprocess
import traceback

#TODO: Separate radio class from screen class. This script should nearly only contain access to the radio.

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyACM0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

device = XBeeDevice(PORT, BAUD_RATE)
my_address = ""
BT_MAC_address = ""

#1. first step is to get the radio address, generate a QR code of it, as well as bluetooth data from your device.
try:
    #device.open()
    with open('/home/beechat/hardware_address.txt', 'r') as file:
        my_address = file.read().rstrip()
    # Obtain the remote XBee device from the XBee network:
        #my_address = device.get_64bit_addr()
        #remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        #remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20041EFD43B"))
        #device.send_data_broadcast(str(my_address))

    qr = qrcode.QRCode()
    qr.add_data(str(my_address))
    qr.make()
    img = qr.make_image()
    img.save('../pic/qr.png')
    subprocess.run("convert ../pic/qr.png -resize 75x75! ../pic/qr.bmp", shell=True, check=False)
    print("Generated Radio address QR code")
    
    cmd = "hciconfig"
    device_id = "hci0" 
    process = subprocess.Popen(['hciconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    print(out)
    s = out.decode()
    startMAC = s.find("BD Address: ") + len("BD Address: ")
    endMAC = s.find("  ACL MTU:")
    BT_MAC_address= s[startMAC:endMAC]
    print(BT_MAC_address)

finally:
    #if device is not None and device.is_open():
        #device.close()
    pass
    print()

#logging.basicConfig(level=logging.DEBUG)


##2. Secondly, we initiate the screen and display the information on a loop.
try:
    #logging.info("epd2in13_V2 screen initiating")
    
    epd = epd2in13_V2.EPD()
    #logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
    #logging.info("1.Drawing on the image...")
    while(True):
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)
        
    #    draw.rectangle([(0,0),(50,50)],outline = 0)
    #    draw.rectangle([(55,0),(100,50)],fill = 0)
    #    draw.line([(0,0),(50,50)], fill = 0,width = 1)
    #    draw.line([(0,50),(50,0)], fill = 0,width = 1)
    #    draw.chord((10, 60, 50, 100), 0, 360, fill = 0)
    #    draw.ellipse((55, 60, 95, 100), outline = 0)
    #    draw.pieslice((55, 60, 95, 100), 90, 180, outline = 0)
    #    draw.pieslice((55, 60, 95, 100), 270, 360, fill = 0)
    #    draw.polygon([(110,0),(110,50),(150,25)],outline = 0)
    #    draw.polygon([(190,0),(190,50),(150,25)],fill = 0)




        draw.text((104, 2), "Your address:", font = font24, fill = 0)
        draw.text((104, 32), str(my_address), font = font15, fill = 0)
        bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
        image.paste(bmp, (2,2))
        bmp2 = Image.open(os.path.join(picdir, 'qr.bmp'))
        draw.ellipse((epd.width-20, 110, epd.width-10, 120), fill=0, outline = 0)
        draw.ellipse((epd.width, 110, epd.width+10, 120), fill=255, outline = 0)
        image.paste(bmp2, (epd.height-75,54))
        epd.display(epd.getbuffer(image))
        time.sleep(3)
        

        ##Start display
        #epd.Clear(0xFF)
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)
        ##Cleared
        bmp = Image.open(os.path.join(picdir, 'bt.bmp'))
        image.paste(bmp, (2,2))

        nearby_devices = bluetooth.discover_devices(duration=4,lookup_names=True,
                                                      flush_cache=True, lookup_class=False)


        draw.text((52, 2), "BT MAC addr.:", font = font24, fill = 0)
        draw.text((52, 25), str(BT_MAC_address), font = font15, fill = 0)

        draw.ellipse((epd.width-20, 110, epd.width-10, 120), fill=255, outline = 0)
        draw.ellipse((epd.width, 110, epd.width+10, 120), fill=0, outline = 0)
        epd.display(epd.getbuffer(image))
        time.sleep(3)










    
    # read bmp file 
#    logging.info("2.read bmp file...")
#    image = Image.open(os.path.join(picdir, '100x100.bmp'))
#    epd.display(epd.getbuffer(image))
#    time.sleep(10)
    
    # read bmp file on window
    #logging.info("3.read bmp file on window...")
    # epd.Clear(0xFF)
    #image1 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    #bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    #image1.paste(bmp, (60,2))
    #epd.display(epd.getbuffer(image1))
    
    #Beechat code
    #draw = ImageDraw.Draw(image)
    #draw.text((120, 60), 'e-Paper demo', font = font15, fill = 0)
    
    #time.sleep(2)
    
    # # partial update
    #logging.info("4.show time...")
    #time_image = Image.new('1', (epd.height, epd.width), 255)
    #time_draw = ImageDraw.Draw(time_image)
    
    #epd.init(epd.FULL_UPDATE)
    #epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    #epd.init(epd.PART_UPDATE)
    #num = 0
    #while (True):
    #    time_draw.rectangle((120, 80, 220, 105), fill = 255)
    #    time_draw.text((120, 80), time.strftime('%H:%M:%S'), font = font24, fill = 0)
    #    epd.displayPartial(epd.getbuffer(time_image))
    #    num = num + 1
    #    if(num == 100000000):
    #        break
    # epd.Clear(0xFF)
    #logging.info("Clear...")
    #epd.init(epd.FULL_UPDATE)
    #epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
