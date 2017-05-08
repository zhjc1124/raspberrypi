import Adafruit_DHT
from db import *


def dht11():
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
    return humidity, temperature


try:
    with connections.cursor() as cursor:
        humidity, temperature = dht11()
        if humidity and temperature:
            cursor.execute('insert into dht11(temperature, humidity) values(%d,%d);', (humidity, temperature))
except Exception as e:
    print(e)
