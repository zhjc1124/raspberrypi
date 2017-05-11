import RPi.GPIO as GPIO
import time
import serial
import os
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, 0)


def sr501():
    return GPIO.input(11)


def relay(status):
    GPIO.output(13, status)
    return 'OK'


def mq2():
    port = "/dev/" + [i for i in os.listdir('/dev') if i.startswith('ttyUSB')][0]
    serialFromArduino = serial.Serial(port, 9600)
    serialFromArduino.flushInput()
    num = 0
    if (serialFromArduino.inWaiting() > 0):
        bytes = serialFromArduino.readline()
        num = float(input)
        print(num)
    return num < 200