import Adafruit_DHT as dht
class Sensor:
    def __init__(self, gpioPin, sensor=dht.AM2302):
        self.gpioPin = gpioPin
        self.sensor = sensor
        
    def getTemperature(self):
        h, t = dht.read_retry(dht.AM2302, self.gpioPin)
        return t

    def getHumidity(self):
        h, t = dht.read_retry(dht.AM2302, self.gpioPin)
        return h