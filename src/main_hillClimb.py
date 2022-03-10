import RPi.GPIO as GPIO
import time

from relay import Relay
from fan import Fan
from sensor import Sensor
from log import Log
from problem import ClimateRegulation

import settings

# Hill Climb: 
# Minimize the time to achieve the goal state

#setup

GPIO.setmode(GPIO.BCM)

heatingMat = Relay(settings.HEATING_MAT_RELAY_PIN)
gsheetLogger = Log(settings.GDOCS_SPREADSHEET_NAME)
fan = Fan(settings.FAN_PIN)
sensor_inside = Sensor(settings.INSIDE_SENSOR_PIN)
sensor_outside = Sensor(settings.OUTSIDE_SENSOR_PIN)
goal_temp = 18
goal_humdity = 60

climateRegulation = ClimateRegulation(goal_temp, goal_humdity)




#loop   

# try:
# initialize values
currentState = climateRegulation.getRandomState()
climateRegulation.setState(currentState)

h_inside, t_inside = sensor_inside.getTemperatureHumidity()
h_outside, t_outside = sensor_outside.getTemperatureHumidity()

while True:
    neighborStates = climateRegulation.getNeighborStates(climateRegulation.getState())
    bestNeighborState = currentState
    bestNeighborScore = climateRegulation.getScore(t_inside, h_inside)

    # Testing neighbor states
    for neighborState in neighborStates:
        print("Testing new Neighbor:", neighborState)

        # Test with new params
        fan.setSpeed(neighborState[0])
        heatingMat.setState(neighborState[1])

        # Wait until measurement makes sense (thermodynamic)
        time.sleep(settings.TEST_TIME)
        h_inside, t_inside = sensor_inside.getTemperatureHumidity()
        h_outside, t_outside = sensor_outside.getTemperatureHumidity()

        # Evalueate Neighbor
        neighborScore = climateRegulation.getScore(t_inside, h_inside)

        #Logging Results
        gsheetLogger.log(t_inside, h_inside, t_outside, h_outside, neighborState[0], neighborState[1], neighborScore)

        if (neighborScore > bestNeighborScore):
            bestNeighborScore = neighborScore
            bestNeighborState = neighborState
    
    # Make decision / Pick best state
    currentState = bestNeighborState
    climateRegulation.setState(currentState)



# except KeyboardInterrupt:
#     pass
#     fan.setSpeed(0)
#     GPIO.cleanup()

# except Exception as e:
#     print(e.__str__())
#     GPIO.cleanup()

