import Adafruit_DHT


def dht11():
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')


def sensor():
    pass


def light_on():
    pass

