import time
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

timeInitial = time.time()


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
    global IK_CONSTANT
    global DK_CONSTANT
    global PK_CONSTANT
    global TIME_STEP
    global RIGHT_MOTOR
    global LEFT_MOTOR

    lastErr = TARGET_DIST - distanceLast
    err = TARGET_DIST - distance
    dK = ((err - lastErr) / (TIME_STEP / 100.0)) * DK_CONSTANT
    pK = err * PK_CONSTANT
    iK = err * (TIME_STEP / 100.0)
    BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED - pK + dK - iK)
    BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED + pK - dK + iK)
    return()

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
        if (int(time.time() * 100) % TIME_STEP ==  0):
            distanceLast = distance
            distance = ultrasonicRead(ULTRASONIC)
            leftWallFollow(distance, distanceLast)
            lastErr = err
            err = TARGET_DIST - distance
            dK = ((err - lastErr) / (TIME_STEP / 100.0)) * DK_CONSTANT
            pK = err * PK_CONSTANT
            iK = err * (TIME_STEP / 100.0)
            BP.set_motor_dps(RIGHT_MOTOR, BASE_SPEED - pK + dK - iK)
            BP.set_motor_dps(LEFT_MOTOR, BASE_SPEED + pK - dK + iK)

#Function Calls
updateMap(0, 0, 3)
updateMap(2, 4,-1)
mapFile.close()
print("reeeee")
