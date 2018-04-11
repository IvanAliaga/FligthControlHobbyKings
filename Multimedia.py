#!/usr/bin/python
'''
Created on 05/06/2014

@author: ivanaliaga
'''
import time
import os
import picamera
import datetime

def getFileNameVideo():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

def getFileNameFoto():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")

def streaming():
    resultado = os.system(" raspivid -o - -t 0 -hf -w 640 -h 320 -fps 24 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8080}' :demux=h264")
    return resultado

def tomarfoto():
    filenamefoto = getFileNameFoto()
    with picamera.PiCamera() as picam:
    	picam.start_preview()
    	time.sleep(5)
    	picam.capture(filenamefoto)
    	picam.stop_preview()
    	picam.close()
    return "<h1>Tomando una foto!</h1>"

def grabarvideo():   
    filenamevideo = getFileNameVideo()
    with picamera.PiCamera() as picam:
	picam.start_recording(filenamevideo)
	picam.wait_recording(20)
    	picam.stop_recording()
    	picam.close()
    return "<h1>Grabando 20 seg!</h1>"
