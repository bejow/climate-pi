import random
FAN_STEPS = 10
class ClimateRegulation:

    def __init__(self, goalTemperature = 18, goalHumidity=60, currentFanState=None, currentHeatMatState=None, temperatureInside=None, humidityInside=None, temperatureOutside=None, humidityOutside=None):
        self.fanStates = range(0, 100, FAN_STEPS) #10 states for the fan
        self.heatMatStates = [True, False]
        self.currentFanState = currentFanState
        self.currentHeatMatState = currentHeatMatState
        self.temperatureInside = temperatureInside
        self.humidityInside = humidityInside
        self.temperatureOutside = temperatureOutside
        self.humidityOutside = humidityOutside
        self.goalHumidity = goalHumidity
        self.goalTemperature = goalTemperature

    def getRandomState(self):
        return random.choice(self.fanStates), random.choice(self.heatMatStates) 

    def getNeighborStates(self, state):
        neighborStates = []
        #fan
        fanStateIndex = self.fanStates.index(state[0])
        if (fanStateIndex > 0):
            #lower fan speed
            neighborFanStateIndex = fanStateIndex -1
            neighborFanState = self.fanStates[neighborFanStateIndex]
            # with both Heating Mat on/off
            neighborStates.append((neighborFanState, True))
            neighborStates.append((neighborFanState, False))
        if (fanStateIndex < FAN_STEPS-1):
            #higher fan speed
            neighborFanStateIndex = fanStateIndex +1
            neighborFanState = self.fanStates[neighborFanStateIndex]
            # with both Heating Mat on/off
            neighborStates.append((neighborFanState, True))
            neighborStates.append((neighborFanState, False))
        return neighborStates

    def setState(self, state):
        self.currentFanState = state[0]
        self.currentHeatMatState = state[1]

    def getState(self):
        return (self.currentFanState, self.currentHeatMatState)

    def getScore(self, newTemperature, newHumidity):
        #delta t/h towards goal t/h - the lower the better
        return (abs(self.goalTemperature - newTemperature) + abs(self.goalHumidity - newHumidity))