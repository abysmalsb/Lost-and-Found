#!/usr/bin/env python

from Hologram.HologramCloud import HologramCloud
from time import sleep
import sys

__author__ = "Balazs Simon"
__license__ = "GPL"
__version__ = "1.0.0"
__details__ = "https://www.hackster.io/Abysmal/lost-and-found-082ebb"

WAIT_SECONDS = 30.0
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
    while True:
        if not hologram.network.is_connected():
            result = hologram.network.connect()
            if result == False:
                print 'Failed to connect to cell network'
            else:
                print 'Connected to cell network'
        elif gotSMS():
            latitude, longitude = getCoordinates()
            if RESPOND_WITH == 's':
                response = 'GPS coordinates of your bike: https://maps.google.com/maps?q=' + str(latitude) + ',' + str(longitude)
                topic = 'sms'
            else:
                response = '{"latitude":"' + str(latitude) + '","longitude":"' + str(longitude) + '"}'
                topic = 'email'
            print 'Response: ' + response
            response_code = hologram.sendMessage(response, topic)
            if 'Message sent successfully' == hologram.getResultString(response_code):
                print 'Message sent successfully'
            else:
                print 'Failed to send message'
        sleep(WAIT_SECONDS)