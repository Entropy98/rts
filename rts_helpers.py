import math
import rts_classes
import rts_map_builder
import pygame,sys
from pygame.locals import *

def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print("]")

def rectanglesOverlap(x1, y1, w1, h1, x2, y2, w2, h2):
    if(((y2<=y1 and y1<=y2+h2) or (y2<=y1+h1 and y1+h1<=y2+h2))and
        ((x1<=x2 and x2<=x1+w1) or (x2<=x1+w1 and x1+w1<=x2+w2))):
        return True
    return False

def getTileCenterCoordinate(data,xCoord,yCoord):
    point0=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
        (xCoord*.25*data.cellWidth+yCoord*.25*data.cellWidth)+data.gameY)

    point1=(((xCoord-1)*.5*data.cellWidth - (yCoord)*.5*data.cellWidth)+data.gameX,\
        ((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

    point2=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
        ((xCoord+1)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

    point3=(((xCoord+1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
        ((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)
    return (point1[0]+point3[0])//2,(point0[1]+point2[1])//2

def moveUnit(x,y,destX,destY,speed,epsilon=6):
    dx=destX-x
    dy=destY-y
    xDir,yDir=1,1
    if(dx<0):
        xDir=-1
    if(dy<0):
        yDir=-1
    if(dy<epsilon and dy>-epsilon and dx<epsilon and dx>-epsilon):
        return (x,y)
    elif(dy<epsilon and dy>-epsilon):
        return (x+speed*xDir,y)
    elif(dx<epsilon and dx>-epsilon):
        return (x,y+speed*yDir)
    else:
        theta=abs(math.atan(dy/dx))
        i=speed*math.cos(theta)*xDir
        j=speed*math.sin(theta)*yDir
        return (x+i,y+j)

def legalPosition(data,unit):
    collided=pygame.sprite.spritecollide(unit,rts_classes.player1.units,False)
    if(len(collided)==0):
        print('sprite collide')
        return False
    if(pointRhombusIntersect(unit.rect.center,*data.mapPos)==False):
        print('map boundary')
        return False
    if(unit.flying==False):
        coords=pos2Coord(data,*unit.rect.center)
        if(data.board[coords[0]][coords[1]]!='field'):
            print('terrain collide')
            return False
    return True

def mapAdjustUnits(dx,dy):
    for unit in rts_classes.player1.units:
        curCoords=unit.rect.center
        unit.rect.center=(curCoords[0]+dx,curCoords[1]+dy)
        unit.desX+=dx
        unit.desY+=dy

def updateMap(data,dx,dy):
    mapAdjustUnits(dx,dy)
    data.trees.update(data)
    data.mapPos=rts_map_builder.generateMapPos(data)


def pointRhombusIntersect(pos,point0,point1,point2,point3):
    m01=(point0[1]-point1[1])/(point0[0]-point1[0])
    m03=(point0[1]-point3[1])/(point0[0]-point3[0])
    m21=(point2[1]-point1[1])/(point2[0]-point1[0])
    m23=(point2[1]-point3[1])/(point2[0]-point3[0])

    # print('TL',pos[1],'>',m21*pos[0]+point2[1]-m21*point2[0])
    # print('TR',pos[1],'>',m23*pos[0]+point2[1]-m23*point2[0])
    # print('BL',pos[1],'<',m01*pos[0]+point0[1]-m01*point0[0])
    # print('BR',pos[1],'<',m03*pos[0]+point0[1]-m03*point0[0])

    if(pos[1]>m21*pos[0]+point2[1]-m21*point2[0]):
        return False
    if(pos[1]>m23*pos[0]+point2[1]-m23*point2[0]):
        return False
    if(pos[1]<m01*pos[0]+point0[1]-m01*point0[0]):
        return False
    if(pos[1]<m03*pos[0]+point0[1]-m03*point0[0]):
        return False
    return True

def pos2Coord(data,xPos,yPos):
    for row in range(data.cells):
        for col in range(data.cells):
            if(pointRhombusIntersect((xPos,yPos),*coord2Pos(data,row,col,'tile'))):
                return(row,col)

#change anchor to 'tile' to receive 4 coordinates of tile instead of 2 of center
def coord2Pos(data,xCoord,yCoord,anchor='center'):
    point0=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
        (xCoord*.25*data.cellWidth+yCoord*.25*data.cellWidth)+data.gameY)

    point1=(((xCoord-1)*.5*data.cellWidth - (yCoord)*.5*data.cellWidth)+data.gameX,\
        ((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

    point2=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
        ((xCoord+1)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

    point3=(((xCoord+1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
        ((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)
    if(anchor=='center'):
        return (((point1[0]+point3[0])//2),((point0[1]+point2[1])//2))
    elif(anchor=='tile'):
        return (point0,point1,point2,point3)