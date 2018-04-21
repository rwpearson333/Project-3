#Team 36 map updating function file
#import grovepi
#import brickpi3
import time
import math as m

X_SIZE = 6
Y_SIZE = 7

#UpdateMap required initialization statements
mapArray = [[0] * (X_SIZE - 1) for y in range(Y_SIZE - 1)]
mapFile = open('map.csv', 'w')

def updateMap(x, y, type):
    mapArray[(Y_SIZE - 2) - y][x] = type
    for y in range(0, Y_SIZE - 1):
        for x in range(0, X_SIZE - 1):
            mapFile.write(str(mapArray[y][x]))
            if (x != X_SIZE - 2):
                mapFile.write(',')
        mapFile.write('\n')
    mapFile.seek(0)
    return()

updateMap(0, 0, 3)
updateMap(2, 4,-1)
mapFile.close()
print("reeeee")
