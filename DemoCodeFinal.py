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
DISTANCE_STEP = 0.97 * 40 #cm
TARGET_DIST = 13

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
lastLeft = abs(BP.get_motor_encoder(LEFT_MOTOR))
lastRight = abs(BP.get_motor_encoder(RIGHT_MOTOR))
TURN_AMOUNT = 260#Paper260
TURN_ADJUST = 195

#get initial values
INITIAL_ENCODER = BP.get_motor_encoder(ULTRASONIC_MOTOR)
WHEEL_DIAMETER = 6.3 #cm

#Map initializations
X_SIZE = 100#6
Y_SIZE = 100#7
origX = 50#2
origY = 50#0
mapNum = 0
posX = origX
posY = origY
heading = 1 # 1: N, 2: E, 3: S, 4: W

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
    mapFile.seek(56)
    return()

def leftWallFollow(distance, distanceLast):
    #print(distance)
    lastErr = TARGET_DIST - distanceLast
    err = TARGET_DIST - distance
    dK = ((err - lastErr) / (TIME_STEP / 100.0)) * DK_CONSTANT
    pK = err * PK_CONSTANT
    iK = err * (TIME_STEP / 100.0)
    BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED - pK + dK - iK)
    BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED + pK - dK + iK)

def ultraLeft():
    BP.set_motor_position(ULTRASONIC_MOTOR, INITIAL_ENCODER)
    time.sleep(0.5)
    dist = grovepi.ultrasonicRead(ULTRASONIC)
    time.sleep(0.1)
    #print("ultraLeft:", dist)
    return dist

def ultraForward():
    BP.set_motor_position(ULTRASONIC_MOTOR, INITIAL_ENCODER - 90)
    time.sleep(0.5)
    dist = grovepi.ultrasonicRead(ULTRASONIC)
    time.sleep(0.1)
    #print("ultraForward:", dist)
    return dist

def ultraRight():
    BP.set_motor_position(ULTRASONIC_MOTOR, INITIAL_ENCODER - 180)
    time.sleep(0.5)
    dist = grovepi.ultrasonicRead(ULTRASONIC)
    time.sleep(0.1)
    #print("ultraRight:", dist)
    return dist

def infraRead():
#    [val1, val2] = IR_Read(grovepi)
    return(IR_Read(grovepi))

def magRead():
    mag = mpu9250.readMagnet()
    total = (mag['x'] ** 2 + mag['y'] ** 2 + mag['z'] ** 2) ** 0.5
    return(total)

def checkDist(lastLeft, lastRight):
    lEnc = abs(BP.get_motor_encoder(LEFT_MOTOR))
    rEnc = abs(BP.get_motor_encoder(RIGHT_MOTOR))

    lDeg = lEnc - lastLeft
    rDeg = rEnc - lastRight
    avgDeg = (lDeg + rDeg) / 2.0

    rotations  = avgDeg / 360.0
    circum = m.pi * WHEEL_DIAMETER
    distance = abs(circum * rotations)
    return(distance, lEnc, rEnc)

def turnCW():
    leftEnc = BP.get_motor_encoder(LEFT_MOTOR)
    rightEnc = BP.get_motor_encoder(RIGHT_MOTOR)
    BP.set_motor_position(LEFT_MOTOR, leftEnc - TURN_ADJUST)
    BP.set_motor_position(RIGHT_MOTOR, rightEnc - TURN_ADJUST)
    time.sleep(0.5)
    leftEnc = BP.get_motor_encoder(LEFT_MOTOR)
    rightEnc = BP.get_motor_encoder(RIGHT_MOTOR)
    BP.set_motor_position(LEFT_MOTOR, leftEnc + TURN_AMOUNT)
    BP.set_motor_position(RIGHT_MOTOR, rightEnc - TURN_AMOUNT)
    print("turnCW")
    time.sleep(1.25)

def turnCCW():
    leftEnc = BP.get_motor_encoder(LEFT_MOTOR)
    rightEnc = BP.get_motor_encoder(RIGHT_MOTOR)
    BP.set_motor_position(LEFT_MOTOR, leftEnc - TURN_ADJUST)
    BP.set_motor_position(RIGHT_MOTOR, rightEnc - TURN_ADJUST)
    time.sleep(0.5)
    leftEnc = BP.get_motor_encoder(LEFT_MOTOR)
    rightEnc = BP.get_motor_encoder(RIGHT_MOTOR)
    BP.set_motor_position(LEFT_MOTOR, leftEnc - TURN_AMOUNT)
    BP.set_motor_position(RIGHT_MOTOR, rightEnc + TURN_AMOUNT)
    print("turnCCW")
    time.sleep(1.25)

def reverseT():
    leftEnc = BP.get_motor_encoder(LEFT_MOTOR)
    rightEnc = BP.get_motor_encoder(RIGHT_MOTOR)
    BP.set_motor_position(LEFT_MOTOR, leftEnc - TURN_AMOUNT)
    BP.set_motor_position(RIGHT_MOTOR, rightEnc + TURN_AMOUNT)
    print("turnCCW")
    time.sleep(1.25)
    leftEnc = BP.get_motor_encoder(LEFT_MOTOR)
    rightEnc = BP.get_motor_encoder(RIGHT_MOTOR)
    BP.set_motor_position(LEFT_MOTOR, leftEnc - TURN_AMOUNT)
    BP.set_motor_position(RIGHT_MOTOR, rightEnc + TURN_AMOUNT)
    print("turnCCW")
    time.sleep(1.25)

def chooseTurn(left, right, front, heading):
    leftTurn = False
    rightTurn = False
    reverse = False
    hasReversed = False
    global posY
    global posX

    if (heading == 1):
        posY = posY + 1
    elif (heading == 2):
        posX = posX + 1
    elif (heading == 3):
        posY = posY - 1
    elif (heading == 4):
        posX = posX - 1

    updateMap(posX, posY, 1)

    if (right > 25 and front < 25):
        rightTurn = True
        distanceTravelled = -2
    if (left > 25):
        leftTurn = True
        rightTurn = False
        distanceTravelled = -2
    if (left <= 25 and right <= 25 and front <= 25):
        leftTurn = False
        rightTurn = False
        reverse = True

    if (leftTurn):
        turnCCW()
        if (heading == 1):
            heading = 4
        else:
            heading = heading - 1
    if (rightTurn):
        turnCW()
        if (heading == 4):
            heading = 1
        else:
            heading = heading + 1
    if (reverse):
        ultraForward()
        color = BP.get_sensor(LIGHT_SENSOR)
        if color > 2550:
                #blue
                updateMap(posX, posY, 3)
        elif color < 2500:
            #gold
                updateMap(posX, posY, 2)
        ultraLeft()
        reverseT()
        heading = heading + 2
        hasReversed = True
        if (heading > 4):
            heading = heading - 4
    return heading, hasReversed

temp = False
mri = 0
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
            updateMap(origX, origY, 10)
            timeInitial = time.time()
            count = count + 1
        if (int(time.time() * 100) % TIME_STEP ==  0):
            distanceLast = distance
            distance = grovepi.ultrasonicRead(ULTRASONIC)
            if distance < 25:
                if temp:
                    leftWallFollow(distance, distanceLast)
                temp = True
            else:
                BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED)
                BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED)
                temp = False
            distanceTemp, lastLeft, lastRight = \
                    checkDist(lastLeft, lastRight)
            distanceTravelled = distanceTravelled + distanceTemp
            if(distanceTravelled > DISTANCE_STEP):
                distanceTravelled = 0
                BP.set_motor_dps(RIGHT_MOTOR, 0)
                BP.set_motor_dps(LEFT_MOTOR, 0)
                frontDist = ultraForward()
                rightDist = ultraRight()
                leftDist = ultraLeft()

                heading, reverseBool = chooseTurn(leftDist, rightDist, frontDist, heading)
                irLeft, irRight = infraRead()
                lastMri = mri
                mri = magRead()

                if (mri > 800 or (mri > 120 and lastMri > 120)):
                    updateMap(posX, posY, 5)
                #If both see IR, update ahead, otherwise update appropriate side
                if (irLeft > 100 and irRight > 100):
                    updateMap(posX, posY, 4)
                elif (irLeft > 100):
                    if heading == 1:
                        updateMap(posX - 1, posY, 4)
                    elif heading == 2:
                        updateMap(posX, posY + 1, 4)
                    elif heading == 3:
                        updateMap(posX + 1, posY, 4)
                    else:
                        updateMap(posX, posY - 1)
                elif (irRight > 100):
                    if heading == 1:
                        updateMap(posX + 1, posY, 4)
                    elif heading == 2:
                        updateMap(posX, posY - 1, 4)
                    elif heading == 3:
                        updateMap(posX - 1, posY, 4)
                    else:
                        updateMap(posX, posY + 1)
        if (BP.get_sensor(BUTTON) and time.time() - timeInitial > 5):
            #if the button is pressed while running, stop and rest
            #then break loop and close map file, sleep to restart
            BP.set_motor_dps(LEFT_MOTOR, 0)
            BP.set_motor_dps(RIGHT_MOTOR, 0)
            ultraLeft()
            mapFile.close()
            print("reeeee")
            value = 0
            time.sleep(2)
            break
