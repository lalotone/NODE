
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import time
import os
import sys
import pyqrcode
import qrtools
import subprocess
import weather_python
import rss_news_feeder

cameraPlugged = False
cameraDaemon = True
camera_port = 0

def startCamera():
    camera = cv2.VideoCapture(camera_port)
    return camera

def getWeather():
    print "Retrieving weather info..."
    tmp, weaDescOne, weaDescTwo, humiData, windData = weather_python.takeData()
    weatherStats = "The temperature is about " + str(tmp) + "degrees," + "and the sky is" + str(weaDescOne)
    print weatherStats

def getNews():
    rss_news_feeder.takeNews()
    print "Getting last news..."
    news = open('news.txt')
    for new in news:
	print new
def decodeQR():
    qr = qrtools.QR()
    qr.decode("/home/lalotone/test_image.png")
    qrData = str(qr.data)
    return qrData

def get_image(camera):
    retval, im = camera.read()
    return im

def take_cam_shot(cameraStart):
    print("Taking image...")
    time.sleep(0.1)
    file = "/home/lalotone/test_image.png"
    camera_capture = get_image(cameraStart)
    cv2.imwrite(file, camera_capture)
    decodedQRData = decodeQR()
    if decodedQRData != None:
        return "blank"
    else:
        return decodedQRData

while cameraDaemon == True:

    if cameraPlugged == False:
        camAttach = startCamera()
        cameraPlugged = True

    qrData = take_cam_shot(camAttach)
    if qrData == "blank":
        for i in range(10):
            print "Shot number ", i + 1
            qrData = take_cam_shot(camAttach)
            print qrData
        del(camAttach)
        cameraPlugged = False
        time.sleep(2)
