import gpsd    #import module
import time    #import required library
import requests

gpsd.connect()
gpsd.connect()
print("test")
gpsData=gpsd.get_current()
print(gpsData.mode)
print(gpsData.track)