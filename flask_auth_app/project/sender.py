#!/usr/bin/python3
import sys,os


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

import xmpp
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyACM0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

#DATA_TO_SEND = "<T>test@test.org</T><M>test</M>"


if len(sys.argv) < 1:
    print("Syntax:<G>0013A20041EFDXXX</G><T>account@xmppaddress.org</T><M>text</M>")
    ##Send message "text" to Gateway "0013A20041EFDXXX", for them to forward to "account@xmppaddress.org"
    sys.exit(0)

s=sys.argv[1]
print(s)



b='<G>'
c='</G>'
l=s.find(b)+len(b)
gateway = s[l:s.find(c)]
print("Send to gateway:" +gateway)



b='<T>'
c='</T>'
l=s.find(b)+len(b)
xmppaddress = s[l:s.find(c)]
print("Gateway will forward to XMPP address:" +xmppaddress)


b='<M>'
c='</M>'
l=s.find(b)+len(b)
MSG = s[l:s.find(c)]
print("Gateway will send the following message:" +MSG)

message_to_send = "<T>"+xmppaddress+"</T>"+"<M>"+MSG+"</M>"

DATA_TO_SEND = ""


def main():
    device = XBeeDevice(PORT, BAUD_RATE)
    if(gateway!=''):
        try:
            device.open()
            # Obtain the remote XBee device from the XBee network.
            #xbee_network = device.get_network()
            #remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
            remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(gateway))


            if remote_device is None:
                print("Could not find the remote device")
                exit(1)
            

            print("Sending data to %s >> %s..." % (remote_device.get_64bit_addr(), message_to_send))

            device.send_data(remote_device, message_to_send)

            print("Success")

        finally:
            if device is not None and device.is_open():
                device.close()
    else:
        print("Broadcasting data...")
        try:
            device.open()

            print("Sending broadcast data: %s..." % message_to_send)

            device.send_data_broadcast(message_to_send)

            print("Success")

        finally:
            if device is not None and device.is_open():
                device.close()


if __name__ == '__main__':
    main()
