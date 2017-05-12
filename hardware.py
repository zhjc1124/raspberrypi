import RPi.GPIO as GPIO
import time
import serial
import os
import atexit
import signal
atexit.register(GPIO.cleanup)
servopin = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, 0)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, 0)
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
        serialFromArduino.flushInput()
    return num < 200


def sg90():
    print('doing')
    GPIO.output(16, 1)
    time.sleep(1.5)
    GPIO.output(16, 0)
    return 'OK'
