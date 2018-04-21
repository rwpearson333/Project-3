import time
import math as m

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

#Function Calls
updateMap(0, 0, 3)
updateMap(2, 4,-1)
mapFile.close()
print("reeeee")
