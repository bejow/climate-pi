import time
import RPi.GPIO as GPIO

# Configuration
FAN_PIN = 18            # BCM pin used to drive PWM fan
WAIT_TIME = 10           # [s] Time to wait between each refresh
PWM_FREQ = 25           # [kHz] 25kHz for Noctua PWM control

# Configurable temperature and fan speed
MIN_TEMP = 40
MAX_TEMP = 70
FAN_LOW = 20
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100

TACH = 24       # Fan's tachometer output pin
PULSE = 2       # Noctua fans puts out two pluses per revolution
WAIT_TIME = 1   # [s] Time to wait between each refresh

GPIO.setmode(GPIO.BCM)


def setFanSpeed(speed):
    fan.start(speed)
    return()

def fell(n):
    global t
    global rpm

    dt = time.time() - t
    if dt < 0.005: return # Reject spuriously short pulses

    freq = 1 / dt
    rpm = (freq / PULSE) * 60
    t = time.time()

try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TACH, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull up to 3.3V
    GPIO.add_event_detect(TACH, GPIO.FALLING, fell)
    # Setup variables
    t = time.time()
    rpm = 0
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN,PWM_FREQ)
    setFanSpeed(FAN_OFF)
    # Handle fan speed every WAIT_TIME sec
    while True:
	setFanSpeed(100)
	print "%.f RPM" % rpm
	rpm = 0
        time.sleep(10)   # Detect every second
        print("100")
        setFanSpeed(0)
	print "%.f RPM" % rpm
        time.sleep(10)
	print("0")
	setFanSpeed(0)
        
except KeyboardInterrupt:
    pass
    fan.stop()
    GPIO.cleanup()
