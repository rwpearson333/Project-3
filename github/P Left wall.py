import time
import brickpi3
from grovepi import *
import math as m

BP = brickpi3.BrickPi3()

#define PID gain constants
DK_CONSTANT = 0.1
IK_CONSTANT = 1
BASE_SPEED = 180

#define sensors
LIGHT_SENSOR = BP.PORT_2
BUTTON = BP.PORT_1
ULTRASONIC = 7

#define motor ports
LEFT_MOTOR = BP.PORT_C #Left motor port
RIGHT_MOTOR = BP.PORT_D #Right motor port

#initialize sensors
BP.set_sensor_type(LIGHT_SENSOR, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)

#Set initial motor speeds to zero
BP.set_motor_dps(RIGHT_MOTOR, 0)
BP.set_motor_dps(LEFT_MOTOR, 0)

value = 0
count = 0

left = False
right = False
timeInitial = time.time()

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
    if ((time - timeInitial) % 5 ==  0):
        distanceLast  = distance
        distance = ultrasonicRead(ULTRASONIC)
        if left:
            BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED * dK + iK)
            BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED) 
        elif right:
            BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED)
            BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED * dK + iK)

        if not left and not right:         
            if distance <= 7.5:
                d = abs(distanceLast - distance) / 0.05
                iK = distance * IK_CONSTANT
                dK = d * DK_CONSTANT
                BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED)
                BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED * dK + iK)
                left = True
            elif distance >= 8.5:
                d = abs(distanceLast - distance) / 0.05
                iK = distance * IK_CONSTANT
                dK = d * DK_CONSTANT
                BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED * dK + iK)
                BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED)
                right = True
            else:
                BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED)
                BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED)
                
    count = count + 1
    