import Adafruit_DHT as dht
from time import sleep

SENSOR_PIN = 2

while True:
	
	h, t = dht.read_retry(dht.AM2302, SENSOR_PIN)
	
	print ("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(t,h))
	sleep(5)
