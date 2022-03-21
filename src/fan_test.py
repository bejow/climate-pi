import RPi.GPIO as GPIO
import time

from fan import Fan
from sensor import Sensor
from log import Log

import settings

#setup

GPIO.setmode(GPIO.BCM)


gsheetLogger = Log(settings.GDOCS_SPREADSHEET_NAME)
fan = Fan(settings.FAN_PIN)
sensor_inside = Sensor(settings.INSIDE_SENSOR_PIN)
sensor_outside = Sensor(settings.OUTSIDE_SENSOR_PIN)

fan.setSpeed(100)

secs_since_start = 0

# Testing the Heating Mat for one Hour

while secs_since_start <= 3600:
    try:
        h_inside, t_inside = sensor_inside.getTemperatureHumidity()
        h_outside, t_outside = sensor_outside.getTemperatureHumidity()
        gsheetLogger.log(t_inside, h_inside, t_outside, h_outside, 100, False)
        time.sleep(30)
        secs_since_start += 30
    except Exception as e:
        print(e.__str__())
        GPIO.cleanup()

