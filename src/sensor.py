import Adafruit_DHT as dht
class Sensor:
    def __init__(self, gpioPin, sensor=dht.AM2302):
        self.gpioPin = gpioPin
        self.sensor = sensor
        
    def getTemperature(self):
        h, t = dht.read_retry(self.sensor, self.gpioPin)
        return t

    def getHumidity(self):
        h, t = dht.read_retry(self.sensor, self.gpioPin)
        return h

    def getTemperatureHumidity(self):
        return dht.read_retry(self.sensor, self.gpioPin)