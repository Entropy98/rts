import pygame,sys
from pygame.locals import *
import rts_helpers
import rts_map_builder
import rts_classes
import rts_images
import rts_menus
import random

def init(data):
	sys.setrecursionlimit(3000)
	data.cells=100
	data.maxCellWidth=100
	data.cellWidth=data.maxCellWidth
	data.zoom=.5
	data.cellWidth=data.maxCellWidth*data.zoom
	data.scrollSpeed=40
	data.cursorX=data.cells//2
	data.cursorY=data.cells//2
	data.mousePos=(0,0)
	data.gameX=data.width//2
	data.gameY=-1.75* data.height
	data.numOfForests=25
	data.forestSize=100
	data.numOfMines=10
	data.trees=pygame.sprite.Group()
	data.mines=pygame.sprite.Group()
	data.board=[]
	for i in range(data.cells):
		newRow=[]
		for j in range(data.cells):
			newRow.append('field')
		data.board.append(newRow)
	print('Planting Trees...')
	rts_map_builder.populateForests(data)
	rts_map_builder.populateMines(data)
	rts_helpers.initializeMenu(data)
	data.selectBox1=(None,None)
	data.selectBox2=[0,0]
	data.mapCoords=((0,0),(0,data.cells-1),(data.cells-1,data.cells-1),(data.cells-1,0))
	data.mapPos=rts_map_builder.generateMapPos(data)
	data.buildStencil=None

def mouseDown(event,data):
	if(event.pos[1]<data.height*.75):
	    data.cellWidth=data.maxCellWidth*data.zoom
	    if(event.button==1):
	    	for unit in rts_classes.player1.selected:
	    		if(unit.name=='CommandCenter' and unit.rallyReset==True):
	    			unit.rally_pointX=event.pos[0]
	    			unit.rally_pointY=event.pos[1]
	    			unit.rallyReset=False
	    			break
	    		if(unit.name=='Drone' and unit.buildState=='Select'):
	    			unit.buildState='Place'
	    	if(data.selectBox1==(None,None)):
	    		rts_classes.player1.clearSelected()
	    		data.selectBox1=event.pos
	    	for building in rts_classes.player1.inConstruction:
	    		if(building.rect.collidepoint(event.pos)):
	    			rts_classes.player1.clearSelected()
	    			rts_classes.player1.select(data,building)
	    	for building in rts_classes.player1.buildings:
	    		if(building.rect.collidepoint(event.pos)):
	    			rts_classes.player1.clearSelected()
	    			rts_classes.player1.select(data,building)


	    if(event.button==3):
	    	mouseX=event.pos[0]
	    	mouseY=event.pos[1]
	    	for unit in rts_classes.player1.selected:
		    	unit.desX=mouseX
		    	unit.desY=mouseY
		    	unit.rally_pointX=mouseX
		    	unit.rally_pointY=mouseY

	else:
		rts_menus.menuButtonsPressed(event.pos,data)


def mouseUp(event,data):
    if(data.selectBox1!=(None,None)):
   		data.selectBox1=(None,None)
   		data.selectBox2=[0,0]

def mouseMotion(event,data):
	if(data.selectBox1!=(None,None)):
		dX,dY=event.rel[0],event.rel[1]
		data.selectBox2[0]+=dX
		data.selectBox2[1]+=dY
	data.mousePos=event.pos
	rts_menus.menuButtonsHover(event.pos,data)

def keyDown(event,data):
	if(event.key==274):#down
		data.cursorY+=1
	elif(event.key==273):#up
		data.cursorY-=1
	elif(event.key==275):#right
		data.cursorX+=1
	elif(event.key==276):#left
		data.cursorX-=1
	if(data.cursorX<0):
		data.cursorX=0
	if(data.cursorY<0):
		data.cursorY=0
	if(data.cursorX>=data.cells):
		data.cursorX=data.cells-1
	if(data.cursorY>=data.cells):
		data.cursorY=data.cells-1

	if(event.unicode=='w'):
		data.gameY+=data.scrollSpeed/data.zoom
		rts_helpers.updateMap(data,0,data.scrollSpeed/data.zoom)
	elif(event.unicode=='s'):
		data.gameY-=data.scrollSpeed/data.zoom
		rts_helpers.updateMap(data,0,-data.scrollSpeed/data.zoom)
	elif(event.unicode=='d'):
		data.gameX-=data.scrollSpeed/data.zoom
		rts_helpers.updateMap(data,-data.scrollSpeed/data.zoom,0)
	elif(event.unicode=='a'):
		data.gameX+=data.scrollSpeed/data.zoom
		rts_helpers.updateMap(data,data.scrollSpeed/data.zoom,0)


	if(event.unicode=='p'):
		x,y=rts_helpers.getTileCenterCoordinate(data,data.cursorX,data.cursorY)
		rts_classes.player1.createDrone(x,y,x,y)

def keyUp(event,data):
   	pass

def inSelectionBox(data):
	if(data.selectBox1!=(None,None)):
		for unit in rts_classes.player1.units:
			if(rts_helpers.rectanglesOverlap(data.selectBox1[0],data.selectBox1[1],data.selectBox2[0],data.selectBox2[1],\
				unit.rect.left,unit.rect.top,unit.rect.width,unit.rect.height)):
				rts_classes.player1.select(data,unit)

def timerFired(data):
	rts_helpers.buildBuildings(data)
	rts_helpers.createUnits()
	rts_helpers.collectUnitMats()
	rts_helpers.collectEnergy()
	rts_helpers.setPowerCap()
	rts_classes.player1.units.update(data)
	inSelectionBox(data)

def drawMap(display,data):
	rts_images.displayMap(display,data,data.gameX-2500,data.gameY)
	data.mines.draw(display)
	data.trees.draw(display)

def drawCursor(display,data):
	coords=rts_helpers.coord2Pos(data,data.cursorX,data.cursorY,'tile')
	point0,point1,point2,point3=coords[0],coords[1],coords[2],coords[3]
	pygame.draw.polygon(display,(153,230,255),(point0,point1,point2,point3),4)
	coordLabel=str(data.cursorX)+','+str(data.cursorY)
	coordLabel=str(data.board[data.cursorX][data.cursorY])
	fontSize=int(20*data.zoom)
	font=pygame.font.SysFont('Helvetica',fontSize)
	textSurface=font.render(coordLabel,False,(255,255,255))
	display.blit(textSurface,((((point1[0]+point3[0])//2)-fontSize,((point0[1]+point2[1])//2)-.5*fontSize)))

def drawSelectBox(display,data):
	if(data.selectBox1!=(None,None)):
		pygame.draw.rect(display,(153,230,255),(data.selectBox1[0],data.selectBox1[1],data.selectBox2[0],data.selectBox2[1]),1)

def drawSelectedRing(display,data):
	for unit in rts_classes.player1.selected:
		pygame.draw.ellipse(display,(153,230,255),(unit.rect.left-2,unit.rect.top+2,unit.rect.width+4,unit.rect.height+4),2)

def drawUnits(display,data):
	player=rts_classes.player1
	player.units.draw(display)

def drawBuildings(display,data):
	rts_classes.player1.inConstruction.draw(display)
	rts_classes.player1.buildings.draw(display)


def redrawAll(display, data):
	drawMap(display,data)
	rts_helpers.drawBuildStencils(display,data)
	drawSelectedRing(display,data)
	drawBuildings(display,data)
	rts_helpers.drawRallyLine(display,data)
	drawUnits(display,data)
	drawSelectBox(display,data)
	drawCursor(display,data)
	rts_menus.drawMenu(display,data)

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

	data.font=pygame.font.SysFont('helvetic',15)

	#initialize Images
	rts_images.loadImages(data)

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