import RPi.GPIO as GPIO

class Relay:
    def __init__(self, gpioPin):
        self.gpioPin = gpioPin

        GPIO.setup(gpioPin, GPIO.OUT)
        GPIO.output(gpioPin, GPIO.HIGH) 


    def on(self):
        GPIO.output(self.gpioPin, GPIO.LOW)

    def off(self):
        GPIO.output(self.gpioPin, GPIO.HIGH )

    def setState (self, state):
        goalState = GPIO.HIGH
        if (state):
            goalState = GPIO.LOW
        GPIO.output(self.gpioPin, goalState)