import RPi.GPIO as GPIO
import time

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
GPIO.setmode(GPIO.BOARD)

heatingMat = Relay(settings.HEATING_MAT_RELAY_PIN)
gsheetLogger = Log(settings.GDOCS_SPREADSHEET_NAME)
fan = Fan(settings.FAN_PIN)
sensor_inside = Sensor(settings.INSIDE_SENSOR_PIN)
sensor_outside = Sensor(settings.OUTSIDE_SENSOR_PIN)
goal_temp = 20
goal_humdity = 50

#loop

try:
    while True:
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
            # print("Turning on Heating Mat to increase teperature")

        #Fan
        if (h_inside > goal_humdity & goal_humdity < h_outside):
            fanTargetSpeed=100
            # print("Turning on fan to decrease humidity")

        elif (t_inside > goal_temp & goal_temp > t_outside):
            fanTargetSpeed=100
            # print("Turning on fan to decrease temperature")

        # elif (t_inside < goal_temp & t_outside > t_inside):
        #     fanTargetSpeed=100
        #     #print("Truning on fan to increase temperature")

        #Logging
        gsheetLogger.log(t_inside, h_inside, t_outside, h_outside, fanTargetSpeed, shouldHeat)

        #Actions
        fan.setSpeed(fanTargetSpeed)
        heatingMat.setState(shouldHeat)

        #Repeat every x seconds
        time.sleep(settings.FREQUENCY_SECONDS)


except KeyboardInterrupt:
    pass
    fan.setSpeed(0)
    GPIO.cleanup()

