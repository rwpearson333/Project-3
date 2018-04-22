import time
import math as m
import brickpi3
import grovepi
from IR_Functions import *
from MPU9250 import MPU9250

BP = brickpi3.BrickPi3()

#define PID gain constants
DK_CONSTANT = 2
IK_CONSTANT = 2
PK_CONSTANT = 8
BASE_SPEED = -180
TIME_STEP = 20 #ms
DISTANCE_STEP = 17.5 #cm
TARGET_DIST = 15

#define sensors
LIGHT_SENSOR = BP.PORT_1
BUTTON = BP.PORT_3
ULTRASONIC = 4
IR_setup(grovepi)
mpu9250 = MPU9250()

#define motor ports
LEFT_MOTOR = BP.PORT_B #Left motor port
RIGHT_MOTOR = BP.PORT_C #Right motor port
ULTRASONIC_MOTOR =  BP.PORT_A

#initialize sensors
BP.set_sensor_type(LIGHT_SENSOR, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(BUTTON, BP.SENSOR_TYPE.TOUCH)

#Set initial motor speeds to zero
BP.set_motor_dps(RIGHT_MOTOR, 0)
BP.set_motor_dps(LEFT_MOTOR, 0)

value = 0
count = 0
distanceTravelled = 0
lastLeft = BP.get_motor_encoder(LEFT_MOTOR)
lastRight = BP.get_motor_encoder(RIGHT_MOTOR)

#get initial values
timeInitial = time.time()
INITIAL_ENCODER = BP.get_motor_encoder(ULTRASONIC_MOTOR)
WHEEL_DIAMETER = 6.3 #cm

#Map initializations
X_SIZE = 6
Y_SIZE = 7
origX = 2
origY = 0
mapNum = 0

#UpdateMap required initialization statements
mapArray = [[0] * (X_SIZE - 1) for y in range(Y_SIZE - 1)]
mapFile = open('map.csv', 'w')

#Basic team info
mapFile.write('Team: 36\nMap: {}\nUnit Length: 35\nOrigin: ({},{})'\
    .format(mapNum, origX, origY))
mapFile.write('\nNotes: No\n')

#Function Defenitions
def updateMap(x, y, type):
    mapArray[(Y_SIZE - 2) - y][x] = type
    for y in range(0, Y_SIZE - 1):
        for x in range(0, X_SIZE - 1):
            mapFile.write(str(mapArray[y][x]))
            if (x != X_SIZE - 2):
                mapFile.write(',')
        mapFile.write('\n')
    mapFile.seek(61)
    return()

def leftWallFollow(distance, distanceLast):

    lastErr = TARGET_DIST - distanceLast
    err = TARGET_DIST - distance
    dK = ((err - lastErr) / (TIME_STEP / 100.0)) * DK_CONSTANT
    pK = err * PK_CONSTANT
    iK = err * (TIME_STEP / 100.0)
    BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED - pK + dK - iK)
    BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED + pK - dK + iK)
    print('ELijaaaaaaah')
    return()

def ultraLeft():
    BP.set_motor_position(ULTRASONIC_MOTOR, INITIAL_ENCODER)
    time.sleep(0.5)
    dist = grovepi.ultrasonicRead(ULTRASONIC)
    time.sleep(0.1)
    print("ultraLeft:", dist)
    return dist

def ultraForward():
    BP.set_motor_position(ULTRASONIC_MOTOR, INITIAL_ENCODER - 90)
    time.sleep(0.5)
    dist = grovepi.ultrasonicRead(ULTRASONIC)
    time.sleep(0.1)
    print("ultraForward:", dist)
    return dist

def ultraRight():
    BP.set_motor_position(ULTRASONIC_MOTOR, INITIAL_ENCODER - 180)
    time.sleep(0.5)
    dist = grovepi.ultrasonicRead(ULTRASONIC)
    time.sleep(0.1)
    print("ultraRight:", dist)

def infraRead():
    [val1, val2] = IR_Read(grovepi)
    return((val1 + val2) / 2)

def magRead():
    mag = mpu9250.readMagnet()
    total = (mag['x'] ** 2 + mag['y'] ** 2 + mag['z'] ** 2) ** 0.5
    return(total)

def checkDist(lastLeft, lastRight):
    lEnc = BP.get_motor_encoder(LEFT_MOTOR)
    rEnc = BP.get_motor_encoder(RIGHT_MOTOR)

    lDeg = lEnc - lastLeft
    rDeg = rEnc - lastRight
    avgDeg = (lDeg + rDeg) / 2

    rotations  = avgDeg = 360
    circum = m.pi * WHEEL_DIAMETER
    distance = abs(circum * rotations)
    return(distance, lEnc, rEnc)

#Function Calls
while not value:
    try:
       value = BP.get_sensor(BUTTON)
    except brickpi3.SensorError:
       value = 0

while value:
        if count == 0:
            BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED)
            BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED)
            distance = grovepi.ultrasonicRead(ULTRASONIC)
        if (int(time.time() * 100) % TIME_STEP ==  0):
            distanceLast = distance
            distance = grovepi.ultrasonicRead(ULTRASONIC)
            print(distance)
            if distance < 20:
                leftWallFollow(distance, distanceLast)
            else:
                BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED)
                BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED)
            distanceTemp, lastLeft, lastRight = \
                    checkDist(lastLeft, lastRight)
            distanceTravelled = distanceTravelled + distanceTemp
#            if(distanceTravelled > DISTANCE_STEP):
#                distanceTravelled = 0
#                BP.set_motor_dps(RIGHT_MOTOR, 0)
#                BP.set_motor_dps(LEFT_MOTOR, 0)
#                frontDist = ultraForward()
#                rightDist = ultraRight()
#                leftDist = ultraLeft()
#                ir = infraRead()
#                mri = magRead()

            #update map appropriately
            #do the things
            #cry
            #Scan for objects
            #release biohazard
            #destroy human kind
            #robots rule world
            #I am king
            #kek



mapFile.close()
print("reeeee")
