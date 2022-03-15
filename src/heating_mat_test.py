import RPi.GPIO as GPIO
import time

from relay import Relay
from log import Log
from sensor import Sensor

import settings

heatingMat = Relay(settings.HEATING_MAT_RELAY_PIN)
gsheetLogger = Log("heating-mat-data")
sensor_inside = Sensor(settings.INSIDE_SENSOR_PIN)
sensor_outside = Sensor(settings.OUTSIDE_SENSOR_PIN)

heatingMat.on()

secs_since_start = 0

# Testing the Heating Mat for one Hour

while secs_since_start <= 3600:
    try:
        h_inside, t_inside = sensor_inside.getTemperatureHumidity()
        h_outside, t_outside = sensor_outside.getTemperatureHumidity()
        gsheetLogger.log(t_inside, h_inside, t_outside, h_outside)
        time.sleep(30)
        secs_since_start += 30
    except Exception as e:
        print(e.__str__())
        GPIO.cleanup()
