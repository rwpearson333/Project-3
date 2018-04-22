import time
import brickpi3
from grovepi import *
import math as m

BP = brickpi3.BrickPi3()

#define PID gain constants
PK_CONSTANT = 8
DK_CONSTANT = 2
IK_CONSTANT = 2
BASE_SPEED = 180
TIME_STEP = 20
TARGET_DIST = 10

#define sensors
LIGHT_SENSOR = BP.PORT_2
BUTTON = BP.PORT_1
ULTRASONIC = 4

#define motor ports
LEFT_MOTOR = BP.PORT_C #Left motor port
RIGHT_MOTOR = BP.PORT_B #Right motor port

#initialize sensors
BP.set_sensor_type(LIGHT_SENSOR, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)

#Set initial motor speeds to zero
BP.set_motor_dps(RIGHT_MOTOR, 0)
BP.set_motor_dps(LEFT_MOTOR, 0)
BP.set_motor_dps(BP.PORT_D, 0)
BP.set_motor_limits(LEFT_MOTOR, 70, 250)
BP.set_motor_limits(RIGHT_MOTOR, 70, 250)

value = 0
count = 0

left = False
right = False
timeInitial = time.time()
err = TARGET_DIST

while not value:
    try:
       value = BP.get_sensor(BUTTON)
    except brickpi3.SensorError:
       value = 0

while value:
    if count == 0:
        BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED)
        BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED) #need to calibrate
        distance = ultrasonicRead(ULTRASONIC)
#    print(time.time())
    if ( int(time.time() * 100) % TIME_STEP ==  0):
        distance = ultrasonicRead(ULTRASONIC)
        lastErr = err
        err = TARGET_DIST - distance
        dK = ((err - lastErr) / (TIME_STEP / 100.0)) * DK_CONSTANT
        pK = err * PK_CONSTANT
        iK = err * (TIME_STEP / 100.0)
        BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED - pK + dK - iK)
        BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED + pK - dK + iK)

    count = count + 1
