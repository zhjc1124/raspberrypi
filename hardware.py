from datetime import datetime
import RPi.GPIO as GPIO
import time
import serial
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(13, GPIO.OUT)


def sr501():
    return GPIO.input(11)


def mq2():
    return GPIO.input(15)


def relay():
    GPIO.output(13, GPIO.HIGH)
    return '已开启'


def lm35():
    # 选定串口
    port = "/dev/ttyACM0"
    # 设置波特率
    serialFromArduino = serial.Serial(port, 9600)
    serialFromArduino.flushInput()
    while True:
        if (serialFromArduino.inWaiting() > 0):
            input = serialFromArduino.readline()
            inputAsInterger = int(input)
            print("inputAsInterger = " + str(inputAsInterger))
            print("Temperature: " + str(inputAsInterger * 5 / 10.24))
        time.sleep(1)


def draw_dht1(date=datetime.now().date().isoformat()):
    pass
