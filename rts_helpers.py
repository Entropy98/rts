import math
import rts_classes
import rts_map_builder
import rts_images
import pygame,sys
from pygame.locals import *
import os

#helper function of print2DList, borrowed from 15-112 class notes
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

#function for printing 2D lists for debugging, borrowed from 15-112 class notes
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

#BROKEN? works well with bottom right corner of rect1
def rectanglesOverlap(x1, y1, w1, h1, x2, y2, w2, h2):
    if(((y2<=y1 and y1<=y2+h2) or (y2<=y1+h1 and y1+h1<=y2+h2))and
        ((x1<=x2 and x2<=x1+w1) or (x2<=x1+w1 and x1+w1<=x2+w2))):
        return True
    return False

#returns the center position of the rhombus at the given coordinate
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

#returns the location of a given unit with the added unit vector towards its destination
def moveUnit(x,y,destX,destY,speed,epsilon=6):
    dx=destX-x
    dy=destY-y
    xDir,yDir=1,1
    if(dx<0):
        xDir=-1
    if(dy<0):
        yDir=-1
    if(dy<epsilon and dy>-epsilon and dx<epsilon and dx>-epsilon):
        return (x,y),None
    elif(dy<epsilon and dy>-epsilon):
        return (x+speed*xDir,y),(xDir,0)
    elif(dx<epsilon and dx>-epsilon):
        return (x,y+speed*yDir),(0,yDir)
    else:
        theta=abs(math.atan(dy/dx))
        i=speed*math.cos(theta)*xDir
        j=speed*math.sin(theta)*yDir
        return (x+i,y+j),(xDir,yDir)

#determines if a unit is allowed to be at it's current position
def legalPosition(data,unit):
    collided=pygame.sprite.spritecollide(unit,data.localPlayer.units,False)
    if(len(collided)>1):
        return False
    if(unit.flying==False):
        collided=pygame.sprite.spritecollide(unit,data.localPlayer.buildings,False)
        if(len(collided)>1):
            return False
        collided=pygame.sprite.spritecollide(unit,data.trees,False)
        if(len(collided)>1):
            return False
        collided=pygame.sprite.spritecollide(unit,data.mines,False)
        if(len(collided)>1):
            return False
    #check if in map
    if(pointRhombusIntersect(unit.rect.center,*data.mapPos)==False):
        return False
    # if(unit.flying==False):
    #     coords=pos2Coord(data,*unit.rect.center)
    #     if(data.board[coords[0]][coords[1]]!='field'):
    #         return False
    return True

#keep units pegged to map as opposed to window
def mapAdjustUnits(data,dx,dy):
    for unit in data.localPlayer.units:
        curCoords=unit.rect.center
        unit.rect.center=(curCoords[0]-dx,curCoords[1]-dy)
        unit.desX-=dx
        unit.desY-=dy
    if(data.startMenuState!='Singleplayer'):
        for ID in data.otherUsers:
            player=data.otherUsers[ID]
            for unit in player.units:
                curCoords=unit.rect.center
                unit.rect.center=(curCoords[0]-dx,curCoords[1]-dy)
                unit.desX-=dx
                unit.desY-=dy
    for building in data.localPlayer.buildings:
        building.rally_pointX-=dx
        building.rally_pointY-=dy

#update all items on the map as it scrolls
def updateMap(data,dx,dy):
    mapAdjustUnits(data,dx,dy)
    data.trees.update(data)
    data.mines.update(data)
    data.localPlayer.inConstruction.update(data)
    data.localPlayer.buildings.update(data)
    if(data.startMenuState!='Singleplayer'):
        for ID in data.otherUsers:
            player=data.otherUsers[ID]
            player.buildings.update(data)
            player.inConstruction.update(data)
    data.mapPos=rts_map_builder.generateMapPos(data)

#function determines if a given point is inside of a rhombus
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

#function takes in a position relative to the window and gives the nearest coordinate on the map
def pos2Coord(data,xPos,yPos):
    for row in range(data.cells):
        for col in range(data.cells):
            if(pointRhombusIntersect((xPos,yPos),*coord2Pos(data,row,col,'tile'))):
                return(row,col)

#change anchor to 'tile' to receive 4 coordinates of tile instead of 2 of center
#function takes in a coordinate on the map and gives the position relative to the window
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

#initializes the button locations in the command menu at the bottom left
def initializeMenu(data):
    data.menuButtons=pygame.sprite.Group()
    data.unitIcons=pygame.sprite.Group()

    boxX=data.width*.65
    boxY=data.height*.75+data.height*.013
    iconBuffer=data.width*.025
    iconWidth=45

    data.menuButton1=rts_images.MenuButton1(boxX+iconBuffer*1.25,boxY+iconBuffer)
    data.menuButton2=rts_images.MenuButton2(boxX+iconBuffer*1.25+(iconWidth+iconBuffer),boxY+iconBuffer)
    data.menuButton3=rts_images.MenuButton3(boxX+iconBuffer*1.25+(iconWidth+iconBuffer)*2,boxY+iconBuffer)
    data.menuButton4=rts_images.MenuButton4(boxX+iconBuffer*1.25,boxY+iconBuffer+(iconWidth+iconBuffer))
    data.menuButton6=rts_images.MenuButton6(boxX+iconBuffer*1.25+(iconWidth+iconBuffer)*2,boxY+iconBuffer+(iconWidth+iconBuffer))

#updates the icons for the different menu buttons between menues
def updateMenuIcons(data):
    if(data.localPlayer.menuState=='Drone'):
        mB1Image=pygame.image.load(os.path.join('rts_build_icon1.png'))
        data.menuButton1.image=pygame.transform.scale(mB1Image,(45,45))
        mB2Image=pygame.image.load(os.path.join('rts_build_military_structures_icon.png'))
        data.menuButton2.image=pygame.transform.scale(mB2Image,(45,45))
        mB4Image=pygame.image.load(os.path.join('rts_drone_action_icon.png'))
        data.menuButton4.image=pygame.transform.scale(mB4Image,(45,45))
        mb6Image=pygame.image.load(os.path.join('rts_destroy_icon.png'))
        data.menuButton6.image=pygame.transform.scale(mb6Image,(45,45))
    elif(data.localPlayer.menuState=='Drone_b1'):
        mB1Image=pygame.image.load(os.path.join('rts_build_command_center_icon.png'))
        data.menuButton1.image=pygame.transform.scale(mB1Image,(45,45))
        mB2Image=pygame.image.load(os.path.join('rts_build_geothermal_generator_icon.png'))
        data.menuButton2.image=pygame.transform.scale(mB2Image,(45,45))
        mB3Image=pygame.image.load(os.path.join('rts_build_farm_icon.png'))
        data.menuButton3.image=pygame.transform.scale(mB3Image,(45,45))
        mb6Image=pygame.image.load(os.path.join('rts_escape_icon.png'))
        data.menuButton6.image=pygame.transform.scale(mb6Image,(45,45))
    elif(data.localPlayer.menuState=='Drone_b2'):
        mB1Image=pygame.image.load(os.path.join('rts_queue_icon1.png'))
        data.menuButton1.image=pygame.transform.scale(mB1Image,(45,45))
        mB2Image=pygame.image.load(os.path.join('rts_build_wood_wall_icon.png'))
        data.menuButton2.image=pygame.transform.scale(mB2Image,(45,45))
        mb6Image=pygame.image.load(os.path.join('rts_escape_icon.png'))
        data.menuButton6.image=pygame.transform.scale(mb6Image,(45,45))
    elif(data.localPlayer.menuState=='CommandCenter'):
        mb1Image=pygame.image.load(os.path.join('rts_build_drone_icon.png'))
        data.menuButton1.image=pygame.transform.scale(mb1Image,(45,45))
        mb4Image=pygame.image.load(os.path.join('rts_rally_point_icon.png'))
        data.menuButton4.image=pygame.transform.scale(mb4Image,(45,45))
        mb6Image=pygame.image.load(os.path.join('rts_destroy_icon.png'))
        data.menuButton6.image=pygame.transform.scale(mb6Image,(45,45))
    elif(data.localPlayer.menuState=='Barracks'):
        mb1Image=pygame.image.load(os.path.join('rts_queue_icon1.png'))
        data.menuButton1.image=pygame.transform.scale(mb1Image,(45,45))
        mb4Image=pygame.image.load(os.path.join('rts_rally_point_icon.png'))
        data.menuButton4.image=pygame.transform.scale(mb4Image,(45,45))
        mb6Image=pygame.image.load(os.path.join('rts_destroy_icon.png'))
        data.menuButton6.image=pygame.transform.scale(mb6Image,(45,45))

#building is a 2D list with a True where a building will be built and a false elsewhere
#stencils have a 1 tile outline to allow proper line ups with other structures
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
            if(building[y][x]):
                if(data.board[newX][newY]!='field'):
                    stencil.append([False,coord2Pos(data,newX,newY,'tile')])
                else:
                    stencil.append([True,coord2Pos(data,newX,newY,'tile')])
            else:
                stencil.append(['empty',coord2Pos(data,newX,newY,'tile')])
                    
    return stencil
    
#plades building at highlighted stencil location
def placeBuilding(data,building):
    centerRhobusCoord=pos2Coord(data,data.mousePos[0],data.mousePos[1])
    buildingCenterY=len(building)//2
    buildingCenterX=len(building[0])//2
    buildingCenter=(buildingCenterX,buildingCenterY)
    for y in range(len(building)):
        for x in range(len(building[0])):
            if(building[y][x]):
                newX=centerRhobusCoord[0]-(buildingCenterX-x)
                newY=centerRhobusCoord[1]-(buildingCenterY-y)
                data.board[newX][newY]='building'
    return centerRhobusCoord

#draws stencil for building around cursor position
def drawBuildStencils(display,data):
    if(data.mousePos[1]<data.height*.75):
        for unit in data.localPlayer.selected:
            if(unit.name=='Drone' and unit.stencil!=None):
                for tile in unit.stencil:
                    if(tile[0]=='empty'):
                        pygame.draw.polygon(display,(217,217,217),tile[1],1)
                    elif(tile[0]):
                        pygame.draw.polygon(display,(153,230,255),tile[1],3)
                    else:
                        pygame.draw.polygon(display,(255,77,77),tile[1],3)

#collect all materials dropped off by drones and store them in player
def collectUnitMats(data):
    for unit in data.localPlayer.units:
        if(unit.name=='Drone'):
            if(len(pygame.sprite.spritecollide(unit,data.localPlayer.commandCenters,False))>0):
                unit.dropOffMats(data)

#progress in building buildings being builts
def buildBuildings(data):
    for building in data.localPlayer.inConstruction:
        building.build(data)
    if(data.startMenuState!='Singleplayer'):
        for ID in data.otherUsers:
            player=data.otherUsers[ID]
            for building in player.inConstruction:
                building.build(data)

#draw line which units built by this building will follow
def drawRallyLine(display,data):
    for building in data.localPlayer.selected:
        if(building.name=='CommandCenter' or building.name=='Barracks'):
            pygame.draw.line(display,(153,230,255),(building.rect.center),(building.rally_pointX,building.rally_pointY))

#progress units being created by buildings
def createUnits(data):
    for building in data.localPlayer.buildings:
        if(building.name=='CommandCenter'):
            if(len(building.buildQueue)>0):
                if(building.buildQueue[0]=='Drone'):
                    building.createDrone(data)
        elif(building.name=='Barracks'):
            if(len(building.buildQueue)>0):
                if(building.buildQueue[0]=='Militia'):
                    building.createMilitia(data)
    if(data.startMenuState!='Singleplayer'):
        for ID in data.otherUsers:
            player=data.otherUsers[ID]
            for building in player.buildings:
                if(building.name=='CommandCenter'):
                    if(len(building.buildQueue)>0):
                        if(building.buildQueue[0]=='Drone'):
                            building.createDrone(data)
                elif(building.name=='Barracks'):
                    if(len(building.buildQueue)>0):
                        if(building.buildQueue[0]=='Militia'):
                            building.createMilitia(data)

#collect energy from all structures which produce it
def collectEnergy(data):
    for building in data.localPlayer.buildings:
        data.localPlayer.energy+=building.energy
        building.energyProduced+=building.energy
    if(data.localPlayer.energy>=data.localPlayer.powerCap):
        data.localPlayer.energy=data.localPlayer.powerCap

#calculate dynamic energy cap based on energy storing buildings
def setPowerCap(data):
    TotalBattery=0
    for building in data.localPlayer.buildings:
        TotalBattery+=building.battery
    data.localPlayer.powerCap=TotalBattery

#calulate dynamic supply cap based on energy stored in buildings
def setSupplyCap(data):
    supply=0
    for building in data.localPlayer.buildings:
        if(building.name=='Farm'):
            supply+=building.supply
    data.localPlayer.supplyCap=supply

#determines if units are to be selected
def inSelectionBox(data):
    if(data.selectBox1!=(None,None)):
        for unit in data.localPlayer.units:
            if(rectanglesOverlap(data.selectBox1[0],data.selectBox1[1],data.selectBox2[0],data.selectBox2[1],\
                unit.rect.left,unit.rect.top,unit.rect.width,unit.rect.height)):
                data.localPlayer.select(data,unit)

#primarily for debugging purposes but shows tile type and binds center of screen
def drawCursor(display,data):
    coords=coord2Pos(data,data.cursorX,data.cursorY,'tile')
    point0,point1,point2,point3=coords[0],coords[1],coords[2],coords[3]
    pygame.draw.polygon(display,(153,230,255),(point0,point1,point2,point3),4)
    coordLabel=str(data.cursorX)+','+str(data.cursorY)
    coordLabel=str(data.board[data.cursorX][data.cursorY])
    fontSize=int(20*data.zoom)
    font=pygame.font.SysFont('Helvetica',fontSize)
    textSurface=font.render(coordLabel,False,(255,255,255))
    display.blit(textSurface,((((point1[0]+point3[0])//2)-fontSize,((point0[1]+point2[1])//2)-.5*fontSize)))

#draw box players use to select their units
def drawSelectBox(display,data):
    if(data.selectBox1!=(None,None)):
        pygame.draw.rect(display,(153,230,255),(data.selectBox1[0],data.selectBox1[1],data.selectBox2[0],data.selectBox2[1]),1)

#highlight units to indicate that they are selected
def drawSelectedRing(display,data):
    for unit in data.localPlayer.selected:
        pygame.draw.ellipse(display,(153,230,255),(unit.rect.left-2,unit.rect.top+2,unit.rect.width+4,unit.rect.height+4),2)

#draw all units from all players
def drawUnits(display,data):
    data.localPlayer.units.draw(display)
    if(data.startMenuState!='Singleplayer'):
        for ID in data.otherUsers:
            player=data.otherUsers[ID]
            player.units.draw(display)

#determine if buildings can be built whether it be resources or previously built infrastructure
def buildReqsMet(data,building):
    if(data.localPlayer.wood>=building.woodCost and data.localPlayer.metals>=building.metalCost):
        numOfReqs=len(building.prereqs)
        reqsMet=set()
        for built in data.localPlayer.buildings:
            for req in building.prereqs:
                if(built.name in building.prereqs):
                    reqsMet.add(built.name)
        if(numOfReqs>len(reqsMet)):
            return False
        return True
    return False

#draw health bars for units and buildings depending on whether or not they have full health
def drawHealthBars(display,data):
    healthBarHeight=10
    #draws black line every 15 health
    for unit in data.localPlayer.units:
        if(unit.health<unit.maxHealth):
            pygame.draw.rect(display,(255,0,0),(unit.rect.center[0]-unit.maxHealth//6,unit.rect.y-healthBarHeight,unit.maxHealth//3,healthBarHeight))
            pygame.draw.rect(display,(0,255,0),(unit.rect.center[0]-unit.maxHealth//6,unit.rect.y-healthBarHeight,(unit.maxHealth//3)*(unit.health/unit.maxHealth),healthBarHeight))
            pygame.draw.rect(display,(0,0,0),(unit.rect.center[0]-unit.maxHealth//6,unit.rect.y-healthBarHeight,unit.maxHealth//3,healthBarHeight),1)
            for i in range(unit.maxHealth//15):
                pygame.draw.line(display,(0,0,0),(unit.rect.center[0]-unit.maxHealth//6+((unit.maxHealth//3)//(unit.maxHealth//15))*(i+1),unit.rect.y-healthBarHeight),\
                    (unit.rect.center[0]-unit.maxHealth//6+((unit.maxHealth//3)//(unit.maxHealth//15))*(i+1),unit.rect.y),1)
    #draws black line every 100 health
    for building in data.localPlayer.buildings:
        if(building.health<building.maxHealth):
            pygame.draw.rect(display,(255,0,0),(building.rect.x,building.rect.y- healthBarHeight,building.rect.width,healthBarHeight))
            pygame.draw.rect(display,(0,255,0),(building.rect.x,building.rect.y- healthBarHeight,building.rect.width*(building.health/building.maxHealth),healthBarHeight))
            pygame.draw.rect(display,(0,0,0),(building.rect.x,building.rect.y- healthBarHeight,building.rect.width,healthBarHeight),1)
            for i in range(building.maxHealth//100):
                pygame.draw.line(display,(0,0,0),(building.rect.x+building.rect.width//(building.maxHealth//100)*(i+1),building.rect.y-healthBarHeight),\
                    (building.rect.x+building.rect.width//(building.maxHealth//100)*(i+1),building.rect.y),1)
    if(data.startMenuState!='Singleplayer'):
        for ID in data.otherUsers:
            player=data.otherUsers[ID]
            for unit in player.units:
                if(unit.health<unit.maxHealth):
                    pygame.draw.rect(display,(255,0,0),(unit.rect.center[0]-unit.maxHealth//6,unit.rect.y-healthBarHeight,unit.maxHealth//3,healthBarHeight))
                    pygame.draw.rect(display,(0,255,0),(unit.rect.center[0]-unit.maxHealth//6,unit.rect.y-healthBarHeight,(unit.maxHealth//3)*(unit.health/unit.maxHealth),healthBarHeight))
                    pygame.draw.rect(display,(0,0,0),(unit.rect.center[0]-unit.maxHealth//6,unit.rect.y-healthBarHeight,unit.maxHealth//3,healthBarHeight),1)
                    for i in range(unit.maxHealth//15):
                        pygame.draw.line(display,(0,0,0),(unit.rect.center[0]-unit.maxHealth//6+((unit.maxHealth//3)//(unit.maxHealth//15))*(i+1),unit.rect.y-healthBarHeight),\
                            (unit.rect.center[0]-unit.maxHealth//6+((unit.maxHealth//3)//(unit.maxHealth//15))*(i+1),unit.rect.y),1)
            #draws black line every 100 health
            for building in player.buildings:
                if(building.health<building.maxHealth):
                    pygame.draw.rect(display,(255,0,0),(building.rect.x,building.rect.y- healthBarHeight,building.rect.width,healthBarHeight))
                    pygame.draw.rect(display,(0,255,0),(building.rect.x,building.rect.y- healthBarHeight,building.rect.width*(building.health/building.maxHealth),healthBarHeight))
                    pygame.draw.rect(display,(0,0,0),(building.rect.x,building.rect.y- healthBarHeight,building.rect.width,healthBarHeight),1)
                    for i in range(building.maxHealth//100):
                        pygame.draw.line(display,(0,0,0),(building.rect.x+building.rect.width//(building.maxHealth//100)*(i+1),building.rect.y-healthBarHeight),\
                            (building.rect.x+building.rect.width//(building.maxHealth//100)*(i+1),building.rect.y),1)

#special eval used for interpretting 2D list. normal eval works but does not handle string abnormalities like spaces
def eval2DListOfStrings(s):
    newList=[]
    for i in range(len(s)):
        if(s[i]=='['):
            if(s[i+1]!='['):
                newList.append([])
        elif(s[i]=="'" or s[i]=='"'):
            if(s[i+1]!=',' and  s[i+1]!=']'):
                newList[-1].append('')
        elif(s[i].isalnum()):
            newList[-1][-1]+=s[i]
    return newList

#check all units in game for their unique ID to determine which is being called
def findUnitByID(data,ID):
    for unit in data.localPlayer.units:
        if(unit.ID==ID):
            return unit
    for building in data.localPlayer.buildings:
        if(building.ID==ID):
            return building
    for ID in data.otherUsers:
        player=data.otherUsers[ID]
        for unit in player.units:
            if(unit.ID==ID):
                return unit
        for building in player.buildings:
            if(building.ID==ID):
                return building

def checkWinConditions(data):
    msg=''
    if(len(data.localPlayer.units)==0 and len(data.localPlayer.buildings)==0):
        data.localPlayer.winCondition='defeat'
        msg+='winCondition defeat \n'

    defeatedPlayers=0
    for ID in data.otherUsers:
        player=data.otherUsers[ID]
        if(player.winCondition=='defeat'):
            defeatedPlayers+=1
        elif(player.winCondition=='win'):
            msg+='winCondition defeat \n'
    if(defeatedPlayers>=len(data.otherUsers)):
        msg+='winCondition win \n'
        data.localPlayer.winCondition='win'
    if(data.localPlayer.winCondition=='play'):
        data.server.send(msg.encode())

def drawEndScreen(display,data):
    if(data.localPlayer.winCondition=='win'):
        endMessage=data.titleFont.render('VICTORY',1,(0,0,255))
    else:
        endMessage=data.titleFont.render('DEFEAT',1,(255,0,0))
    display.blit(endMessage,(data.width*.4,data.height*.3))
    homeButtonLabel=data.menuFont.render('RETURN',1,(153,230,255))
    pygame.draw.rect(display,(20,20,20),(data.width*.4,data.height*.6,data.width*.2,40))
    pygame.draw.rect(display,(153,230,255),(data.width*.4,data.height*.6,data.width*.2,40),3)
    display.blit(homeButtonLabel,(data.width*.42,data.height*.6))