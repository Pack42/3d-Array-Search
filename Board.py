import random
maxX = 10
maxY = 10
maxZ = 10
numWalls = 500
def getMax():
    return maxX, maxY, maxZ
def board():
    b = [[[0 for k in range(maxX)] for j in range(maxY)] for i in range(maxZ)]
    for i in range(numWalls):
        b[random.randint(0,maxZ-1)][random.randint(0,maxY-1)][random.randint(0,maxX-1)] = 8
    n = [random.randint(0,maxZ-1),random.randint(0,maxY-1),random.randint(0,maxX-1)]
    while b[n[0]][n[1]][n[2]] != 0:
        n = [random.randint(0,maxZ-1),random.randint(0,maxY-1),random.randint(0,maxX-1)]
    path = []
    x,y,z = n[2],n[1],n[0]
    b[z][y][x] = 2
    while True:
        print(len(path))
        if x-1 >= 0 and b[z][y][x-1] ==0:
            path.append([z,y,x])
            x-=1
            b[z][y][x] = 2
        elif x+1 < maxX and b[z][y][x+1] ==0:
            path.append([z,y,x])
            x+=1
            b[z][y][x] = 2
        elif y+1 < maxY and b[z][y+1][x] ==0:
            path.append([z,y,x])
            y+=1
            b[z][y][x] = 2
        elif y-1>= 0 and b[z][y-1][x] ==0:
            path.append([z,y,x])
            y-=1
            b[z][y][x] = 2
        elif z+1 < maxZ and b[z+1][y][x] == 0:
            path.append([z,y,x])
            z+=1
            b[z][y][x] = 2
        elif z-1 >= 0 and b[z-1][y][x] == 0:
            path.append([z,y,x])
            z-=1
            b[z][y][x] = 2
        elif len(path) > 0:
            loc = path.pop()
            z = loc[0]
            y = loc[1]
            x = loc[2]
        else:
            break
    for z in range(maxZ):
        for y in range(maxY):
            for x in range(maxX):
                if b[z][y][x] == 0:
                    b[z][y][x] = 8
                elif b[z][y][x] == 2:
                    b[z][y][x] = 0
                    
    for item in b[0]:
        print(item)
    return b
