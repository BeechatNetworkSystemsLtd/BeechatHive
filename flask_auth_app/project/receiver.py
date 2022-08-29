# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from digi.xbee.devices import XBeeDevice
import subprocess
# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyACM0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600




def main():
    print(" +-------------------------+")
    print(" | BEECHAT GATEWAY STARTED |")
    print(" +-------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)
    import subprocess

   
    try:
        device.open()

        ##Read hardware address and write to file for the screen

        print("Radio address:"+str(device.get_64bit_addr()))
        text_file = open("hardware_address.txt", "w")
        n = text_file.write(str(device.get_64bit_addr()))
        text_file.close()

        device.flush_queues()

        print("Waiting for data...\n")

        while True:
            xbee_message = device.read_data()
            if xbee_message is not None:
                print("Received message from %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                         xbee_message.data.decode()))
                s = xbee_message.data.decode()

                # An example received packet may be:
                #s = "<T>user@xmppdomain.org</T><M>Sending from sender script</M>"
                # TODO: replace prefix and suffix for bytes and encode string.
                
                # TODO: 27/07/2022 - check message type, XMPP or radio. If <T> tag is empty it's a radio message
                # TODO: 27/07/2022 - save message into sqlite db


                b='<T>'
                c='</T>'
                l=s.find(b)+len(b)
                sendTO = s[l:s.find(c)]
                print("Forwarding to:" +sendTO)


                b='<M>'
                c='</M>'
                l=s.find(b)+len(b)
                MSG = s[l:s.find(c)]
                print("Forwarding message:" +MSG)


                from datetime import datetime
                now = datetime.now()
                with open('messages.txt', 'a') as f:
                    f.write(now.strftime("%d/%m/%Y %H:%M:%S") +" from "+ str(xbee_message.remote_device.get_64bit_addr())+" | Message: " +MSG +"\n")

                ## add check to see if the received message was empty
                

                #Check for internet connection
                import requests
                def connected_to_internet(url="https://beechat.network/", timeout=5):
                    try:
                        _ = requests.head(url,timeout=timeout)
                        return True
                    except requests.ConnectionError:
                        print("No Internet connection available.")
                    return False
                    
                connected = connected_to_internet()
                if(connected):
                    subprocess.run("python3 xsend.py " + sendTO + " " + MSG , shell=True, check=True)

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
