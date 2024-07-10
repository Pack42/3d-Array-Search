# TITLE: 3d board creator with no impossible to reach squares
# AUTHOR: Pack
# DATE: 7/7/2024
# LAST UPDATE: 7/9/2024
# SUMMARY: Import to file to be used and run board() to generate 3d array representation of the board
#           To change parameters update the variables maxX, maxY, MaxZ, or numWalls

import random
# Define parameters of board fully costumizable, but will break if num walls is too high
maxX = 10
maxY = 10
maxZ = 10
numWalls = 500
# Function to create 3d-board
def board():
    # Create board with all 0's
    b = [[[0 for k in range(maxX)] for j in range(maxY)] for i in range(maxZ)]
    # Add walls randomly
    for i in range(numWalls):
        b[random.randint(0,maxZ-1)][random.randint(0,maxY-1)][random.randint(0,maxX-1)] = 8
    # Choose starting point for checking which spaces are inaccessible
    n = [random.randint(0,maxZ-1),random.randint(0,maxY-1),random.randint(0,maxX-1)]
    while b[n[0]][n[1]][n[2]] != 0:
        n = [random.randint(0,maxZ-1),random.randint(0,maxY-1),random.randint(0,maxX-1)]
    # Setup algorithm variables and starting square
    path = []
    x,y,z = n[2],n[1],n[0]
    b[z][y][x] = 2
    while True:
        # Check each square next to current square has been visited if not go to square, and add current to end of path
        # If all surronding squares have been visited than pop path list to go back a square
        # If path list is empty and all surronding squares have been visited than every possible square has been reached
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
            z,y,x = loc[0], loc[1], loc[2]
        else:
            break
    # Create maxScore variable
        maxScore = 0
    # Loop that switches all impossible squares to secondary type of wall, switches visited to unvisited, and updates maxScore 
    for z in range(maxZ):
        for y in range(maxY):
            for x in range(maxX):
                if b[z][y][x] == 0:
                    b[z][y][x] = 9
                elif b[z][y][x] == 2:
                    maxScore+=1
                    b[z][y][x] = 0              
    # Returns a tuple with the board and maxScore (-1 to remove starting square)
    return b, maxScore-1
