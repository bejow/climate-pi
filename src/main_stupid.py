import RPi.GPIO as GPIO

from relay import Relay
from fan import Fan
from sensor import Sensor
from log import Log

import settings

#Stupid: 
# Heating if: inside temp < target temperature
# Fan if: inside humidity > goal humidity < outside_humidity || inside temp > goal temp > outside temp
# Binary Fan
# No parameter threshold

#setup
heatingMat = Relay(settings.HEATING_MAT_RELAY_PIN)
gsheetLogger = Log("test_main_stupid_data")
fan = Fan(settings.FAN_PIN)
sensor_inside = Sensor(settings.INSIDE_SENSOR_PIN)
sensor_outside = Sensor(settings.OUTSIDE_SENSOR_PIN)
goal_temp = 20
goal_humdity = 50

#loop

while True:
    try:
        #resetting action params
        fanTargetSpeed = 0
        shouldHeat = False

        #obtaining values
        h_inside, t_inside = sensor_inside.getTemperatureHumidity()
        h_outside, t_outside = sensor_outside.getTemperatureHumidity()

        #Logic

        #Heating
        if (t_inside < goal_temp):
            shouldHeat=True
        
        #Fan
        if (h_inside > goal_humdity & goal_humdity < h_outside):
            fanTargetSpeed=100
        elif (t_inside > goal_temp & goal_temp > t_outside):
            fanTargetSpeed=100
    except KeyboardInterrupt:
        pass
        fan.setSpeed(0)
        GPIO.cleanup()
    except Exception as e:
        print(e)
