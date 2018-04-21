#Team 36 map updating function file
import grovepi
import brickpi3
import time
import math as m

BUTTON = BP.PORT_1
ULTRASONIC = 7

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

#UpdateMap required initialization statements
map = [[0 for x in range(5)] 0 for y in range(6)]
mapFile = open('map.csv', 'w')
updateMap(0, 0, 0)
mapFile.close()

def updateMap(x, y, type):
    map[x][y] = type
    mapFile.write(map)
    return()
