import RPi.GPIO as GPIO
import time
import serial
import os
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, 0)
port = "/dev/" + [i for i in os.listdir('/dev') if i.startswith('ttyUSB')][0]
serialFromArduino = serial.Serial(port, 9600)
serialFromArduino.flushInput()

def sr501():
    return GPIO.input(11)


def relay(status):
    GPIO.output(13, status)
    return 'OK'

def mq2():
    num = 0
    if (serialFromArduino.inWaiting() > 0):
        bytes = serialFromArduino.readline()
        print(bytes)
        num = float(bytes)
    return num<200