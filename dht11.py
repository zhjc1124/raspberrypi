try:
    import Adafruit_DHT
except ImportError:
    pass

from db import *


def dht11():
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
    print(humidity, temperature)
    return humidity, temperature

if __name__ == '__main__':
    try:
        with connections.cursor() as cursor:
            humidity, temperature = dht11()
            if humidity and temperature:
                cursor.execute('insert into dht11(humidity, temperature) values(%s,%s);', (humidity, temperature))
    except Exception as e:
        print(e)
