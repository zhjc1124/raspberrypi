from datetime import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.OUT)


def sr501():
    return GPIO.input(11)


def light_on():
    GPIO.output(13, GPIO.HIGH)


def draw_dht1(date=datetime.now().date().isoformat()):
    pass
