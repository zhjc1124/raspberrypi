import Adafruit_DHT
from db import *
import time


def dht11():
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
    return humidity, temperature


def save_dht11():
    while True:
        try:
            with connections.cursor() as cursor:
                humidity, temperature = dht11()
                if humidity and temperature:
                    cursor.execute('insert into dht11(temperature, humidity) values(%d,%d);', (humidity, temperature))
        except Exception:
            continue
        time.sleep(60)
