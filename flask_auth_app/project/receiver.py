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
    print(" +-------------------------------------------------+")
    print(" |            BEECHAT GATEWAY STARTING             |")
    print(" +-------------------------------------------------+\n")

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

        print("Waiting for XMPP data...\n")

        while True:
            xbee_message = device.read_data()
            if xbee_message is not None:
                print("Received message from %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                         xbee_message.data.decode()))
                s = xbee_message.data.decode()

                # An example received packet may be:
                #s = "<T>user@xmppdomain.org</T><M>Sending from sender script</M>"
                # TODO: replace prefix and suffix for bytes and encode string.
                
                startTO = s.find("<T>") + len("<T>")
                endTO = s.find("</T>")
                sendTO= s[startTO:endTO]
                print("Forward XMPP to:" +sendTO)

                startMSG = s.find("<M>") + len("<M>")
                endMSG = s.find("</M>")
                MSG = s[startMSG:endMSG]
                print("Message:" +MSG)
                subprocess.run("python3 xsend.py " + sendTO + " " + MSG , shell=True, check=True)

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
