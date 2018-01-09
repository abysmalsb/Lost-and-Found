#!/usr/bin/env python

from Hologram.HologramCloud import HologramCloud
from time import sleep
import sys
import time
import serial
import pynmea2

__author__ = "Balazs Simon"
__license__ = "GPL"
__version__ = "1.0.0"
__details__ = "https://www.hackster.io/Abysmal/lost-and-found-082ebb"

RESPOND_WITH = 'e'

def getCoordinates():
    latitude = hologram.network.location.latitude
    longitude = hologram.network.location.longitude
    return latitude, longitude

def gotSMS():
    global RESPOND_WITH
    sms = hologram.popReceivedSMS()
    if sms is not None:
        RESPOND_WITH = sms.message
        print sms
        return True
    else:
        return False

if __name__ == '__main__':
    hologram = HologramCloud(dict(), network='cellular')
    ser = serial.Serial(
        port='/dev/serial0',
        baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
    msg = None
    while True:
        x=ser.readline()
        if(x[:6] == "$GPGGA"):
            msg = x
        if not hologram.network.is_connected():
            result = hologram.network.connect()
            if result == False:
                print 'Failed to connect to cell network'
            else:
                print 'Connected to cell network'
        elif gotSMS():
            if RESPOND_WITH[1] == 'g' and msg is not None:
                position = pynmea2.parse(msg)
                latitude, longitude = position.latitude, position.longitude
                origin = 'GPS'
            else:
                latitude, longitude = getCoordinates()
                origin = 'Cellular'
            if RESPOND_WITH[0] == 's':
                response = origin + ' coordinates of your bike: https://maps.google.com/maps?q=' + str(latitude) + ',' + str(longitude)
                topic = 'sms'
            else:
                response = '{"latitude":"' + str(latitude) + '","longitude":"' + str(longitude) + '","origin":"'+ origin +'"}'
                topic = 'email'
            print 'Response: ' + response
            response_code = hologram.sendMessage(response, topic)
            if 'Message sent successfully' == hologram.getResultString(response_code):
                print 'Message sent successfully'
            else:
                print 'Failed to send message'
