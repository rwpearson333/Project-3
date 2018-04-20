import time
import brickpi3
from grovepi import *
import math as m

BP = brickpi3.BrickPi3()

LIGHT_SENSOR = BP.PORT_2
BUTTON = BP.PORT_1
ULTRASONIC = 7

LEFT_MOTOR = #Left motor port
RIGHT_MOTOR = #Right motor port

BP.set_sensor_type(LIGHT_SENSOR, BP.SENSOR_TYPE.NXT_LIGHT_ON)

BP.set_motor_dps(RIGHT_MOTOR, 0)
BP.set_motor_dps(LEFT_MOTOR, 0)

value = 0
count = 0
while not value:
    try:
       value = BP.get_sensor(BUTTON)
    except brickpi3.SensorError:
       value = 0

while value:
    if count == 0:
        BP.set_motor_dps(RIGHT_MOTOR, 50)
        BP.set_motor_dps(LEFT_MOTOR, 50)#need to calibrate
    
    distance = ultrasonicRead(ULTRASONIC)
    
    if distance < 6.5:
        BP.set_motor_dps(RIGHT_MOTOR, 0)
        BP.set_motor_dps(LEFT_MOTOR, 0)
        color = BP.get_sensor(LIGHT_SENSOR)
        if color < 2800 and color > 2450:
            print("ITEM IS BLUE")
            value = 0
        else:
            print("ITEM IS GOLD")
            value = 0
    count = count + 1
    