import RPi.GPIO as GPIO
import time
import serial
import os
import atexit
import signal
atexit.register(GPIO.cleanup)
servopin = 6
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(13, GPIO.OUT, initial=False)
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


def sg90():
    p = GPIO.PWM(servopin, 50)
    p.start(0)
    for i in range(0, 181, 10):
        p.ChangeDutyCycle(2.5 + 10 * i / 180)  # 设置转动角度
        time.sleep(0.02)  # 等该20ms周期结束
        p.ChangeDutyCycle(0)  # 归零信号
        time.sleep(0.2)
    time.sleep(3)
    for i in range(181, 0, -10):
        p.ChangeDutyCycle(2.5 + 10 * i / 180)
        time.sleep(0.02)
        p.ChangeDutyCycle(0)
        time.sleep(0.2)
    return 'finished'
