import RPi.GPIO as GPIO
import time
import pickle
from progress_bar import progressBar

from relay import Relay
from fan import Fan
from sensor import Sensor
from log import Log
from problem import ClimateRegulation

import settings

# load trained model
with open("model_lin_reg_xl.pkl", 'rb') as file:
    model = pickle.load(file)
    

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

# Copy current values, because there are no previous values
prev_h_inside, prev_t_inside = h_inside, t_inside
prev_h_outside, prev_t_outside = h_outside, t_outside

while True:
    neighborStates = climateRegulation.getNeighborStates(climateRegulation.getState())
    bestNeighborState = currentState
    bestNeighborScore = climateRegulation.getScore(t_inside, h_inside)

    # Testing neighbor states
    for neighborState in neighborStates:
        print("Testing new Neighbor:", neighborState)

        prediction = model.predict([[t_outside, h_outside, prev_t_inside, prev_h_inside, prev_t_outside, prev_h_outside, neighborState[0], neighborState[1]]])
        predicted_t_inside = prediction[0][0]
        predicted_h_inside = prediction[0][1]
        
        # Evalueate Neighbor
        neighborScore = climateRegulation.getScore(predicted_t_inside, predicted_h_inside)

        # Logging Results


        # Compare States (small = better)
        if (neighborScore < bestNeighborScore):
            bestNeighborScore = neighborScore
            bestNeighborState = neighborState
    
    # Make decision / Pick best state
    currentState = bestNeighborState
    climateRegulation.setState(currentState)

    # Print current environment values
    print("Humidity:\ninside:{0}\noutside:{1}".format(h_inside, h_outside))
    print("Temperature:\ninside:{0}\noutside:{1}".format(t_inside, t_outside))

    # Print the current action
    print("Setting Fan to: ", currentState[0])
    fan.setSpeed(currentState[0])

    print("Heating: ", currentState[1])
    heatingMat.setState(currentState[1])

    print("Estimated state after action: {0}% Humdity, {1}C Temperature".format(predicted_h_inside, predicted_t_inside))

    # Wait until change take place
    for item in progressBar(range(settings.TEST_TIME), "Testing Settings:", "Complete", 2, 40, printEnd=""):
        time.sleep(1)

    h_inside, t_inside = sensor_inside.getTemperatureHumidity()
    h_outside, t_outside = sensor_outside.getTemperatureHumidity() 

    # measure real score of neighbor (to compare prediction against reality later)
    realBestNeighborScore = climateRegulation.getScore(t_inside, h_inside)

    gsheetLogger.log3(t_inside, h_inside, t_outside, h_outside, prev_t_inside, prev_h_inside, prev_t_outside, prev_h_outside, currentState[0], currentState[1], bestNeighborScore, realBestNeighborScore)
    
    prev_h_inside, prev_t_inside = h_inside, t_inside
    prev_h_outside, prev_t_outside = h_outside, t_outside



# except KeyboardInterrupt:
#     pass
#     fan.setSpeed(0)
#     GPIO.cleanup()

# except Exception as e:
#     print(e.__str__())
#     GPIO.cleanup()

