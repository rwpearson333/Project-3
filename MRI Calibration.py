import time
import math as m
import brickpi3
import grovepi
from MPU9250 import MPU9250

BP = brickpi3.BrickPi3()

mpu9250 = MPU9250()

BUTTON = BP.PORT_3
BP.set_sensor_type(BUTTON, BP.SENSOR_TYPE.TOUCH)

def magRead():
    mag = mpu9250.readMagnet()
    total = (mag['x'] ** 2 + mag['y'] ** 2 + mag['z'] ** 2) ** 0.5
    return(total)

magArray = []

for i in range(0, 10):
    magArray.stack(magRead)
    time.sleep(0.1)

magBias = average(magArray)
print("\nMag Bias:", magBias, "\n")

value = 0
while True:
    while not value:
        try:
           value = BP.get_sensor(BUTTON)
        except brickpi3.SensorError:
           value = 0

    while value:
        print("\n", magRead() - magBias)
        time.sleep(1)
        value = 0
