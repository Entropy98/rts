import math
import rts_classes
import rts_map_builder
import rts_images
import pygame,sys
from pygame.locals import *
import os

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
    if(len(collided)>1):
        return False
    if(pointRhombusIntersect(unit.rect.center,*data.mapPos)==False):
        return False
    if(unit.flying==False):
        coords=pos2Coord(data,*unit.rect.center)
        if(data.board[coords[0]][coords[1]]!='field'):
            return False
    return True

def mapAdjustUnits(dx,dy):
    for unit in rts_classes.player1.units:
        curCoords=unit.rect.center
        unit.rect.center=(curCoords[0]+dx,curCoords[1]+dy)
        unit.desX+=dx
        unit.desY+=dy
        if(unit.name=='CommandCenter'):
            unit.rally_pointX+=dx
            unit.rally_pointY+=dy

def updateMap(data,dx,dy):
    mapAdjustUnits(dx,dy)
    data.trees.update(data)
    rts_classes.player1.inConstruction.update(data)
    rts_classes.player1.buildings.update(data)
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

def initializeMenu(data):
    data.menuButtons=pygame.sprite.Group()
    data.unitIcons=pygame.sprite.Group()

    boxX=data.width*.65
    boxY=data.height*.75+data.height*.013
    iconBuffer=data.width*.025
    iconWidth=45

    data.menuButton1=rts_images.MenuButton1(boxX+iconBuffer*1.25,boxY+iconBuffer)
    data.menuButton4=rts_images.MenuButton4(boxX+iconBuffer*1.25,boxY+iconBuffer+(iconWidth+iconBuffer))
    data.menuButton6=rts_images.MenuButton6(boxX+iconBuffer*1.25+(iconWidth+iconBuffer)*2,boxY+iconBuffer+(iconWidth+iconBuffer))

def updateMenuIcons(data):
    print(rts_classes.player1.menuState)
    if(rts_classes.player1.menuState=='Drone'):
        mB1Image=pygame.image.load(os.path.join('rts_build_icon1.png'))
        data.menuButton1.image=pygame.transform.scale(mB1Image,(45,45))
        mB4Image=pygame.image.load(os.path.join('rts_drone_action_icon.png'))
        data.menuButton4.image=pygame.transform.scale(mB4Image,(45,45))
        mb6Image=pygame.image.load(os.path.join('rts_destroy_icon.png'))
        data.menuButton6.image=pygame.transform.scale(mb6Image,(45,45))
    elif(rts_classes.player1.menuState=='Drone_b1'):
        mB1Image=pygame.image.load(os.path.join('rts_build_command_center_icon.png'))
        data.menuButton1.image=pygame.transform.scale(mB1Image,(45,45))
        mb6Image=pygame.image.load(os.path.join('rts_escape_icon.png'))
        data.menuButton6.image=pygame.transform.scale(mb6Image,(45,45))
    elif(rts_classes.player1.menuState=='CommandCenter'):
        mb1Image=pygame.image.load(os.path.join('rts_build_drone_icon.png'))
        data.menuButton1.image=pygame.transform.scale(mb1Image,(45,45))
        mb4Image=pygame.image.load(os.path.join('rts_rally_point_icon.png'))
        data.menuButton4.image=pygame.transform.scale(mb4Image,(45,45))
        mb6Image=pygame.image.load(os.path.join('rts_destroy_icon.png'))
        data.menuButton6.image=pygame.transform.scale(mb6Image,(45,45))

#building is a 2D list with a True where a building will be built and a false elsewhere
def compileBuildStencil(data,building):
    stencil=[]
    centerRhobusCoord=pos2Coord(data,data.mousePos[0],data.mousePos[1])
    buildingCenterY=len(building)//2
    buildingCenterX=len(building[0])//2
    buildingCenter=(buildingCenterX,buildingCenterY)
    for y in range(len(building)):
        for x in range(len(building[0])):
            newX=centerRhobusCoord[0]-(buildingCenterX-x)
            newY=centerRhobusCoord[1]-(buildingCenterY-y)
            if(building[x][y]):
                if(data.board[newX][newY]!='field'):
                    stencil.append([False,coord2Pos(data,newX,newY,'tile')])
                else:
                    stencil.append([True,coord2Pos(data,newX,newY,'tile')])
            else:
                stencil.append(['empty',coord2Pos(data,newX,newY,'tile')])
                    
    return stencil
    
def placeBuilding(data,building):
    centerRhobusCoord=pos2Coord(data,data.mousePos[0],data.mousePos[1])
    buildingCenterY=len(building)//2
    buildingCenterX=len(building[0])//2
    buildingCenter=(buildingCenterX,buildingCenterY)
    for y in range(len(building)):
        for x in range(len(building[0])):
            if(building[x][y]):
                newX=centerRhobusCoord[0]-(buildingCenterX-x)
                newY=centerRhobusCoord[1]-(buildingCenterY-y)
                data.board[newX][newY]='building'
    return centerRhobusCoord

def drawBuildStencils(display,data):
    if(data.mousePos[1]<data.height*.75):
        for unit in rts_classes.player1.selected:
            if(unit.name=='Drone' and unit.stencil!=None):
                for tile in unit.stencil:
                    if(tile[0]=='empty'):
                        pygame.draw.polygon(display,(217,217,217),tile[1],1)
                    elif(tile[0]):
                        pygame.draw.polygon(display,(153,230,255),tile[1],3)
                    else:
                        pygame.draw.polygon(display,(255,77,77),tile[1],3)

def collectUnitMats():
    for unit in rts_classes.player1.units:
        if(unit.name=='Drone'):
            if(len(pygame.sprite.spritecollide(unit,rts_classes.player1.commandCenters,False))>0):
                unit.dropOffMats()