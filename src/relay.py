import RPi.GPIO as GPIO

class Relay:
    def __init__(self, gpioPin):
        self.gpioPin = gpioPin
        GPIO.setup(gpioPin, GPIO.OUT)

    def on(self):
        GPIO.output(self.gpioPin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.gpioPin, GPIO.LOW )