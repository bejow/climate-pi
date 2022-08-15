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

def chooseBestState(climateRegulationObject, t_outside, h_outside, prev_t_inside, prev_h_inside, prev_t_outside, prev_h_outside):
    states = climateRegulationObject.getAllStates()
    predictions = [model.predict([[t_outside, h_outside, prev_t_inside, prev_h_inside, prev_t_outside, prev_h_outside, currentState[0], currentState[1]]]) for currentState in states]
    scores = [climateRegulationObject.getScore(currentPrediction[0][0], currentPrediction[0][1]) for currentPrediction in predictions]
    max_value = max(scores)
    max_index = scores.index(max_value)
    print(states)
    print(predictions)
    print(scores)
    print(max_value)
    print(max_index)
    return (states[max_index], predictions[max_index], scores[max_index])

# load trained model
with open(settings.TRAINED_MODEL_PATH, 'rb') as file:
    model = pickle.load(file)
    

# Bruteforce: 
# Minimize the time to achieve the goal state

#setup

GPIO.setmode(GPIO.BCM)

heatingMat = Relay(settings.HEATING_MAT_RELAY_PIN)
gsheetLogger = Log(settings.GDOCS_SPREADSHEET_NAME)
fan = Fan(settings.FAN_PIN)
sensor_inside = Sensor(settings.INSIDE_SENSOR_PIN)
sensor_outside = Sensor(settings.OUTSIDE_SENSOR_PIN)
goal_temp = settings.TARGET_TEMPERATURE
goal_humdity = settings.TARGET_HUMIDITY

climateRegulation = ClimateRegulation(goal_temp, goal_humdity)




#loop   

# try:

# initialize values



h_inside, t_inside = sensor_inside.getTemperatureHumidity()
h_outside, t_outside = sensor_outside.getTemperatureHumidity()

# Copy current values, because there are no previous values
prev_h_inside, prev_t_inside = h_inside, t_inside
prev_h_outside, prev_t_outside = h_outside, t_outside


while True:
    
    currentState, prediction, score = chooseBestState(climateRegulation, t_outside, h_outside, prev_t_inside, prev_h_inside, prev_t_outside, prev_h_outside)
    climateRegulation.setState(currentState)

    # Print current environment values
    print("Humidity:\ninside:{0}\noutside:{1}".format(h_inside, h_outside))
    print("Temperature:\ninside:{0}\noutside:{1}".format(t_inside, t_outside))

    # Print the current action
    print("Setting Fan to: ", currentState[1])
    fan.setSpeed(currentState[1])

    print("Heating: ", currentState[0])
    heatingMat.setState(currentState[0])

    print("Estimated state after action: {0}% Humdity, {1}C Temperature".format(prediction[0][1], prediction[0][0]))

    print("Estimates Score after action: {0}".format(score))

    # Wait until change take place
    for item in progressBar(range(settings.TEST_TIME), "Testing Settings:", "Complete", 2, 40, printEnd=""):
        time.sleep(1)

    h_inside, t_inside = sensor_inside.getTemperatureHumidity()
    h_outside, t_outside = sensor_outside.getTemperatureHumidity() 

    realBestNeighborScore = climateRegulation.getScore(t_inside, h_inside)

    print("Measured Score after action: {0}".format(realBestNeighborScore))


    gsheetLogger.log3(t_inside, h_inside, t_outside, h_outside, prev_t_inside, prev_h_inside, prev_t_outside, prev_h_outside, currentState[0], currentState[1], score, realBestNeighborScore)
    
    prev_h_inside, prev_t_inside = h_inside, t_inside
    prev_h_outside, prev_t_outside = h_outside, t_outside



# except KeyboardInterrupt:
#     pass
#     fan.setSpeed(0)
#     GPIO.cleanup()

# except Exception as e:
#     print(e.__str__())
#     GPIO.cleanup()

