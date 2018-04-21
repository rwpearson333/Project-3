import time
import brickpi3
from grovepi import *
import math as m
#555: 12in
BP = brickpi3.BrickPi3()
rightMotor = BP.PORT_B
leftMotor = BP.PORT_C
ultMotor = BP.PORT_D
turnAmount = 300
forwardAmount = 260#230
error = 1
leftControl = 1
rightControl = 1
initialEncoder = BP.get_motor_encoder(ultMotor)
BP.set_motor_limits(leftMotor, 70, 250)
BP.set_motor_limits(rightMotor, 70, 250)

def ultraLeft():
    BP.set_motor_position(ultMotor, initialEncoder)
    time.sleep(0.5)
    dist = ultrasonicRead(7)
    time.sleep(0.1)
    print("ultraLeft:", dist)
    return dist

def ultraForward():
    BP.set_motor_position(ultMotor, initialEncoder + 90)
    time.sleep(0.5)
    dist = ultrasonicRead(7)
    time.sleep(0.1)
    print("ultraForward:", dist)
    return dist

def ultraRight():
    BP.set_motor_position(ultMotor, initialEncoder + 180)
    time.sleep(0.5)
    dist = ultrasonicRead(7)
    time.sleep(0.1)
    print("ultraRight:", dist)
    return dist

def turnCW():
    leftEnc = BP.get_motor_encoder(leftMotor)
    rightEnc = BP.get_motor_encoder(rightMotor)
    BP.set_motor_position(leftMotor, leftEnc + turnAmount)
    BP.set_motor_position(rightMotor, rightEnc - turnAmount)
    time.sleep(1.25)
    print("CW")

def turnCCW():
    leftEnc = BP.get_motor_encoder(leftMotor)
    rightEnc = BP.get_motor_encoder(rightMotor)
    BP.set_motor_position(leftMotor, leftEnc - turnAmount)
    BP.set_motor_position(rightMotor, rightEnc + turnAmount)
    time.sleep(1.25)
    print("CCW")

def forward():
    leftEnc = BP.get_motor_encoder(leftMotor)
    rightEnc = BP.get_motor_encoder(rightMotor)
    BP.set_motor_position(leftMotor, leftEnc + forwardAmount * leftControl)
    BP.set_motor_position(rightMotor, rightEnc + forwardAmount * rightControl)
    time.sleep(1)
    print("forward")

    
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)

distLeft = 0
distForward = 0
distRight = 0


print("Press button to begin")

touchStart = 0
firstRun = 1

# wait to start until touch sensor pressed
while not touchStart:
    try:
       touchStart = BP.get_sensor(BP.PORT_1)
    except brickpi3.SensorError:
       touchStart = 0

while(touchStart):
    if (firstRun):
        time.sleep(1)
        firstRun = 0
    # stop if touch sensor pressed
    if (BP.get_sensor(BP.PORT_1)):
        touchStart = 0
    
    distLeft = ultraLeft()
    distForward = ultraForward()
    distRight = ultraRight()
    
    error = distLeft - distRight
    if (error > 0):
        leftControl = 1
        rightControl = 1.1
        print("error > 0")
    elif (error < 0):
        leftControl = 1.1
        rightControl = 1
        print("error < 0")
    else:
        leftControl = 1
        rightControl = 1
        print("error = 0")

    if (distForward <= 13):
        if (distLeft >= distRight):
            turnCCW()
            forward()
            print("turnCCW")
        elif (distLeft < distRight):
            turnCW()
            forward()
            print("turnCW")
    elif (distForward > 13):
        forward()

        
        


    

