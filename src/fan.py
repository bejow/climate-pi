import RPi.GPIO as GPIO

PWM_FREQ = 25           # [kHz] 25kHz for Silent Wings PWM control
FAN_LOW = 20
FAN_HIGH = 100

class Fan:
    def __init__(self, gpioPin):
        self.gpioPin = gpioPin
        self.fan = GPIO.PWM(gpioPin,PWM_FREQ)
             

    def setSpeed(self, speed):
        self.fan.start(speed)