import pygame,sys
from pygame.locals import *
import rts_helpers
import rts_map_builder
import rts_classes
import random

def init(data):
	data.cells=100
	data.maxCellWidth=100
	data.cellWidth=data.maxCellWidth
	data.zoom=.5
	data.cellWidth=data.maxCellWidth*data.zoom
	data.scrollSpeed=40
	data.cursorX=data.cells//2
	data.cursorY=data.cells//2
	data.gameX=data.width//2
	data.gameY=-data.height
	data.numOfForests=50
	data.forestMinSize=50
	data.forestMaxSize=100
	data.board=[]
	for i in range(data.cells):
		newRow=[]
		for j in range(data.cells):
			newRow.append('field')
		data.board.append(newRow)
	rts_map_builder.populateForests(data)
	data.selectBox1=(None,None)
	data.selectBox2=[0,0]

def mouseDown(event,data):
    # if(event.button==5):
    # 	data.zoom-=.1
    # elif(event.button==4):
    # 	data.zoom+=.1
    # if(int(data.zoom*10)<=2):
    # 	data.zoom=.2
    data.cellWidth=data.maxCellWidth*data.zoom
    if(event.button==1):
    	if(data.selectBox1==(None,None)):
    		rts_classes.player1.clearSelected()
    		data.selectBox1=event.pos

def mouseUp(event,data):
    if(data.selectBox1!=(None,None)):
   		data.selectBox1=(None,None)
   		data.selectBox2=[0,0]

def mouseMotion(event,data):
	if(data.selectBox1!=(None,None)):
		dX,dY=event.rel[0],event.rel[1]
		data.selectBox2[0]+=dX
		data.selectBox2[1]+=dY

def keyDown(event,data):
	if(event.key==274):#down
		data.cursorY+=1
	elif(event.key==273):#up
		data.cursorY-=1
	elif(event.key==275):#right
		data.cursorX+=1
	elif(event.key==276):#left
		data.cursorX-=1

	if(event.unicode=='w'):
		data.gameY+=data.scrollSpeed/data.zoom
		for unit in rts_classes.player1.units:
			unit['y']+=data.scrollSpeed/data.zoom
	elif(event.unicode=='s'):
		data.gameY-=data.scrollSpeed/data.zoom
		for unit in rts_classes.player1.units:
			unit['y']-=data.scrollSpeed/data.zoom
	elif(event.unicode=='d'):
		data.gameX-=data.scrollSpeed/data.zoom
		for unit in rts_classes.player1.units:
			unit['x']-=data.scrollSpeed/data.zoom
	elif(event.unicode=='a'):
		data.gameX+=data.scrollSpeed/data.zoom
		for unit in rts_classes.player1.units:
			unit['x']+=data.scrollSpeed/data.zoom

	if(event.unicode=='p'):
		x,y=rts_helpers.getTileCenterCoordinate(data,data.cursorX,data.cursorY)
		rts_classes.player1.createDrone(x,y)

def keyUp(event,data):
   	pass

def inSelectionBox(data):
	if(data.selectBox1!=(None,None)):
		for unit in rts_classes.player1.units:
			#print(rts_helpers.rectanglesOverlap(data.selectBox1[0],data.selectBox1[1],data.selectBox2[0],data.selectBox2[1],unit['x'],unit['y'],unit['hitBoxX'],unit['hitBoxY']))
			if(rts_helpers.rectanglesOverlap(data.selectBox1[0],data.selectBox1[1],data.selectBox2[0],data.selectBox2[1],unit['x'],unit['y'],unit['hitBoxX'],unit['hitBoxY'])):
				rts_classes.player1.select(unit)

def timerFired(data):
    inSelectionBox(data)

def drawGrid(display,data):
	for x in range(data.cells):
		for y in range(data.cells):
			xCoord=x
			yCoord=y
			point0=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
				(xCoord*.25*data.cellWidth+yCoord*.25*data.cellWidth)+data.gameY)

			point1=(((xCoord-1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
				((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

			point2=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
				((xCoord+1)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

			point3=(((xCoord+1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
				((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)
			tileLabel=data.board[x][y]
			if(tileLabel=='forest'):
				pygame.draw.polygon(display,(26,13,0),(point0,point1,point2,point3))
			else:
				pygame.draw.polygon(display,(51,153,51),(point0,point1,point2,point3))

def drawCursor(display,data):
	yCoord=data.cursorY
	xCoord=data.cursorX
	point0=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
		(xCoord*.25*data.cellWidth+yCoord*.25*data.cellWidth)+data.gameY)

	point1=(((xCoord-1)*.5*data.cellWidth - (yCoord)*.5*data.cellWidth)+data.gameX,\
		((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

	point2=((xCoord*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
		((xCoord+1)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)

	point3=(((xCoord+1)*.5*data.cellWidth - yCoord*.5*data.cellWidth)+data.gameX,\
		((xCoord)*.25*data.cellWidth+(yCoord+1)*.25*data.cellWidth)+data.gameY)
	pygame.draw.polygon(display,(153,230,255),(point0,point1,point2,point3),4)
	coordLabel=str(xCoord)+','+str(yCoord)
	fontSize=int(20*data.zoom)
	font=pygame.font.SysFont('Helvetica',fontSize)
	textSurface=font.render(coordLabel,False,(255,255,255))
	display.blit(textSurface,((((point1[0]+point3[0])//2)-fontSize,((point0[1]+point2[1])//2)-.5*fontSize)))

def drawSelectBox(display,data):
	if(data.selectBox1!=(None,None)):
		pygame.draw.rect(display,(153,230,255),(data.selectBox1[0],data.selectBox1[1],data.selectBox2[0],data.selectBox2[1]),1)

def drawSelectedRing(display,data):
	for unit in rts_classes.player1.selected:
		hitBoxX=(unit['hitBoxX']+2)*data.zoom
		hitBoxY=(unit['hitBoxY']+2)*data.zoom
		centerX=unit['x']-hitBoxX//2
		centerY=(unit['y']-hitBoxY//2)+(unit['hitBoxY']//2)*data.zoom
		pygame.draw.ellipse(display,(153,230,255),(centerX,centerY,hitBoxX,hitBoxY),2)

def drawUnits(display,data):
	player=rts_classes.player1
	for unit in player.units:
		hitBoxX=unit['hitBoxX']*data.zoom
		hitBoxY=unit['hitBoxY']*data.zoom
		centerX=unit['x']-hitBoxX//2
		centerY=unit['y']-hitBoxY//2
		pygame.draw.rect(display,(255,255,128),(centerX,centerY,hitBoxX,hitBoxY))


def redrawAll(display, data):
	drawGrid(display,data)
	drawCursor(display,data)
	drawSelectedRing(display,data)
	drawUnits(display,data)
	drawSelectBox(display,data)

def run(width=300, height=300):
	def redrawAllWrapper(display, data):
		display.fill((255,255,255))
		redrawAll(display, data)
		pygame.display.update()  

	def mouseDownWrapper(event, display, data):
		mouseDown(event, data)
		redrawAllWrapper(display, data)

	def mouseUpWrapper(event, display, data):
		mouseUp(event, data)
		redrawAllWrapper(display, data)

	def mouseMotionWrapper(event,display,data):
		mouseMotion(event,data)
		redrawAllWrapper(display,data)

	def keyDownWrapper(event, display, data):
		keyDown(event,data)
		redrawAllWrapper(display, data)

	def keyUpWrapper(event, display, data):
		keyUp(event,data)
		redrawAllWrapper(display, data)

	def quit():
		pygame.quit()
		sys.exit()

	def timerFiredWrapper(display, data):
		timerFired(data)
		redrawAllWrapper(display, data)
		data.fpsClock.tick(data.fps)

	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.fps=30 #frames per second
	data.fpsClock=pygame.time.Clock()
	init(data)

	# initialize module and display
	pygame.init()
	pygame.font.init()
	display = pygame.display.set_mode((data.width,data.height))
	pygame.display.set_caption('RTS')

	#main loop
	while(True):
		for event in pygame.event.get():
			if(event.type==QUIT):
				quit()
			if(event.type==KEYDOWN):
				keyDownWrapper(event,display,data)
			if(event.type==KEYUP):
				keyUpWrapper(event,display,data)
			if(event.type==MOUSEBUTTONDOWN):
				mouseDownWrapper(event,display,data)
			if(event.type==MOUSEBUTTONUP):
				mouseUpWrapper(event,display,data)
			if(event.type==MOUSEMOTION):
				mouseMotionWrapper(event,display,data)
		timerFiredWrapper(display,data)

run(600,600)