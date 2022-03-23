# purpose of this script is to obtain data from various states of the system

import RPi.GPIO as GPIO
import time
import random
from progress_bar import progressBar

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

GPIO.setmode(GPIO.BCM)

heatingMat = Relay(settings.HEATING_MAT_RELAY_PIN)
gsheetLogger = Log(settings.GDOCS_SPREADSHEET_NAME)
fan = Fan(settings.FAN_PIN)
sensor_inside = Sensor(settings.INSIDE_SENSOR_PIN)
sensor_outside = Sensor(settings.OUTSIDE_SENSOR_PIN)

# from 0-30 the fan is not moving
fan_settings = [i for i in range(30,100)]
fan_settings += 0 # still add an "off" mode

#loop   
prev_h_inside, prev_t_inside = sensor_inside.getTemperatureHumidity()
prev_h_outside, prev_t_outside = sensor_outside.getTemperatureHumidity()

# try:
while True:
    # Randomly choose settings
    fanTargetSpeed = random.choice(fan_settings) 
    shouldHeat = bool(random.getrandbits(1))

    print("Fan Target Speed set to:", fanTargetSpeed)
    print("Heating Mat should heat set to:", shouldHeat)

    # Apply Settings
    fan.setSpeed(fanTargetSpeed)
    heatingMat.setState(shouldHeat)

    # Wait for result (slowly changing)
    for item in progressBar(range(settings.TEST_TIME), "Testing Settings:", "Complete", 2, 40, printEnd=""):
        time.sleep(1)

    # Obtaining result
    h_inside, t_inside = sensor_inside.getTemperatureHumidity()
    h_outside, t_outside = sensor_outside.getTemperatureHumidity()

    # Logging
    gsheetLogger.log2(t_inside, h_inside, t_outside, h_outside, prev_t_inside, prev_h_inside, prev_t_outside, prev_h_outside, fanTargetSpeed, shouldHeat)

    # Memorize Environment Data for the next loop (to evaluate the impact of the random settings)
    prev_t_inside, prev_h_inside, prev_t_outside, prev_h_outside = t_inside, h_inside, t_outside, h_outside

# except KeyboardInterrupt:
#     pass
#     fan.setSpeed(0)
#     GPIO.cleanup()

# except Exception as e:
#     print(e.__str__())
 
#     GPIO.cleanup()

