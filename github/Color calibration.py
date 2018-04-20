import time
import brickpi3
from grovepi import *
import math as m

BP = brickpi3.BrickPi3()

LIGHT_SENSOR = BP.PORT_2
BUTTON = BP.PORT_1
ULTRASONIC = 7

BP.set_sensor_type(LIGHT_SENSOR, BP.SENSOR_TYPE.NXT_LIGHT_ON)

value = 0

while not value:
    try:
       value = BP.get_sensor(BUTTON)
    except brickpi3.SensorError:
       value = 0

while value:
    try:
       value = BP.get_sensor(BUTTON)
    except brickpi3.SensorError:
       value = 0
    distance = ultrasonicRead(ULTRASONIC)
    color = BP.get_sensor(LIGHT_SENSOR)
    print("Color:", color)
    print("Distnace:", distance)
    time.sleep(0.2)




