import pygame,sys
from pygame.locals import *
import rts_helpers
import rts_map_builder
import rts_classes
import rts_images
import rts_menus
import rts_buildings
import rts_startmenu
import random
import math

def initStartMenu(data):
	data.startMenu=True
	data.startMenuState='Start'
	data.startMenuSelect=None
	data.usernameInput=''
	data.singlePlayerTextBoxSelect=None
	data.playButtonHover=False
	data.playButtonPressed=False

def init(data):
	sys.setrecursionlimit(3000)
	data.cells=100
	data.maxCellWidth=100
	data.cellWidth=data.maxCellWidth
	data.zoom=.5
	data.cellWidth=data.maxCellWidth*data.zoom
	data.scrollSpeed=3
	data.cursorX=random.randint(0,data.cells-1)
	data.cursorY=random.randint(0,data.cells-1)
	data.mousePos=(0,0)
	data.gameX=(25*data.cursorY-25*data.cursorX)+(data.width/2)
	data.gameY=-((12.5*(data.cursorY+data.cursorX))-(data.height*.75)/2)
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

def startGame(data):
	data.startMenu=False
	data.localPlayer=rts_classes.Player(data.usernameInput)
	init(data)

def mouseDown(event,data):
	if(data.startMenu==False):
		if(event.pos[1]<data.height*.75):
		    data.cellWidth=data.maxCellWidth*data.zoom
		    if(event.button==1):
		    	for unit in data.localPlayer.selected:
		    		if(unit.name=='CommandCenter' and unit.rallyReset==True):
		    			unit.rally_pointX=event.pos[0]
		    			unit.rally_pointY=event.pos[1]
		    			unit.rallyReset=False
		    			break
		    		if(unit.name=='Drone' and unit.buildState=='Select'):
		    			unit.buildState='Place'
		    	if(data.selectBox1==(None,None)):
		    		data.localPlayer.clearSelected()
		    		data.selectBox1=event.pos
		    	for building in data.localPlayer.inConstruction:
		    		if(building.rect.collidepoint(event.pos)):
		    			data.localPlayer.clearSelected()
		    			data.localPlayer.select(data,building)
		    	for building in data.localPlayer.buildings:
		    		if(building.rect.collidepoint(event.pos)):
		    			data.localPlayer.clearSelected()
		    			data.localPlayer.select(data,building)


		    if(event.button==3):
		    	mouseX=event.pos[0]
		    	mouseY=event.pos[1]
		    	for unit in data.localPlayer.selected:
			    	unit.desX=mouseX
			    	unit.desY=mouseY
			    	unit.rally_pointX=mouseX
			    	unit.rally_pointY=mouseY

		else:
			rts_menus.menuButtonsPressed(event.pos,data)
	else:
		if(data.startMenuState=='Start'):
			data.startMenuState=rts_startmenu.startMenuButtonPressed(data,event.pos)
		elif(data.startMenuState=='Singleplayer'):
			data.singlePlayerTextBoxSelect=rts_startmenu.singlePlayerTextBoxSelect(data,event.pos)
			if(len(data.usernameInput)>0):
				data.playButtonPressed=rts_startmenu.playButtonPressed(data,event.pos)


def mouseUp(event,data):
	if(data.startMenu==False):
	    if(data.selectBox1!=(None,None)):
	   		data.selectBox1=(None,None)
	   		data.selectBox2=[0,0]

def mouseMotion(event,data):
	if(data.startMenu==False):
		if(data.selectBox1!=(None,None)):
			dX,dY=event.rel[0],event.rel[1]
			data.selectBox2[0]+=dX
			data.selectBox2[1]+=dY
		data.mousePos=event.pos
		rts_menus.menuButtonsHover(event.pos,data)
	else:
		if(data.startMenuState=='Start'):
			data.startMenuSelect=rts_startmenu.startMenuButtonHover(data,event.pos)
		elif(data.startMenuState=='Singleplayer'):
			data.playButtonHover=rts_startmenu.playButtonHover(data,event.pos)

def keyDown(event,data):
	if(data.startMenu==False):
		if(event.key==274):#down
			data.cursorY+=data.scrollSpeed
			data.cursorX+=data.scrollSpeed
			ogGameX=data.gameX
			ogGameY=data.gameY
			data.gameX=(25*data.cursorY-25*data.cursorX)+(data.width/2)
			data.gameY=-((12.5*(data.cursorY+data.cursorX))-(data.height*.75)/2)
			rts_helpers.updateMap(data,ogGameX-data.gameX,ogGameY-data.gameY)
		elif(event.key==273):#up
			data.cursorY-=data.scrollSpeed
			data.cursorX-=data.scrollSpeed
			ogGameX=data.gameX
			ogGameY=data.gameY
			data.gameX=(25*data.cursorY-25*data.cursorX)+(data.width/2)
			data.gameY=-((12.5*(data.cursorY+data.cursorX))-(data.height*.75)/2)
			rts_helpers.updateMap(data,ogGameX-data.gameX,ogGameY-data.gameY)
		elif(event.key==275):#right
			data.cursorX+=data.scrollSpeed
			data.cursorY-=data.scrollSpeed
			ogGameX=data.gameX
			ogGameY=data.gameY
			data.gameX=(25*data.cursorY-25*data.cursorX)+(data.width/2)
			data.gameY=-((12.5*(data.cursorY+data.cursorX))-(data.height*.75)/2)
			rts_helpers.updateMap(data,ogGameX-data.gameX,ogGameY-data.gameY)
		elif(event.key==276):#left
			data.cursorX-=data.scrollSpeed
			data.cursorY+=data.scrollSpeed
			ogGameX=data.gameX
			ogGameY=data.gameY
			data.gameX=(25*data.cursorY-25*data.cursorX)+(data.width/2)
			data.gameY=-((12.5*(data.cursorY+data.cursorX))-(data.height*.75)/2)
			rts_helpers.updateMap(data,ogGameX-data.gameX,ogGameY-data.gameY)
		if(data.cursorX<0):
			data.cursorX=0
			ogGameX=data.gameX
			ogGameY=data.gameY
			data.gameX=(25*data.cursorY-25*data.cursorX)+(data.width/2)
			data.gameY=-((12.5*(data.cursorY+data.cursorX))-(data.height*.75)/2)
			rts_helpers.updateMap(data,ogGameX-data.gameX,ogGameY-data.gameY)
		if(data.cursorY<0):
			data.cursorY=0
			ogGameX=data.gameX
			ogGameY=data.gameY
			data.gameX=(25*data.cursorY-25*data.cursorX)+(data.width/2)
			data.gameY=-((12.5*(data.cursorY+data.cursorX))-(data.height*.75)/2)
			rts_helpers.updateMap(data,ogGameX-data.gameX,ogGameY-data.gameY)
		if(data.cursorX>=data.cells):
			data.cursorX=data.cells-1
			ogGameX=data.gameX
			ogGameY=data.gameY
			data.gameX=(25*data.cursorY-25*data.cursorX)+(data.width/2)
			data.gameY=-((12.5*(data.cursorY+data.cursorX))-(data.height*.75)/2)
			rts_helpers.updateMap(data,ogGameX-data.gameX,ogGameY-data.gameY)
		if(data.cursorY>=data.cells):
			data.cursorY=data.cells-1
			ogGameX=data.gameX
			ogGameY=data.gameY
			data.gameX=(25*data.cursorY-25*data.cursorX)+(data.width/2)
			data.gameY=-((12.5*(data.cursorY+data.cursorX))-(data.height*.75)/2)
			rts_helpers.updateMap(data,ogGameX-data.gameX,ogGameY-data.gameY)

		if(event.unicode=='p'):
			x,y=rts_helpers.getTileCenterCoordinate(data,data.cursorX,data.cursorY)
			data.localPlayer.createDrone(x,y,x,y)
	else:
		if(data.startMenuState=='Singleplayer'):
			if(data.singlePlayerTextBoxSelect==1):
				if(event.unicode.isalnum()):
					data.usernameInput+=event.unicode
				elif(event.key==8 and len(data.usernameInput)>0):
					data.usernameInput=data.usernameInput[:-1]

def keyUp(event,data):
   	pass

def timerFired(data):
	if(data.startMenu==False):
		rts_helpers.buildBuildings(data)
		rts_helpers.createUnits(data)
		rts_helpers.collectUnitMats(data)
		rts_helpers.collectEnergy(data)
		rts_helpers.setPowerCap(data)
		data.localPlayer.units.update(data)
		rts_helpers.inSelectionBox(data)
	else:
		if(data.playButtonPressed):
			startGame(data)


def redrawAll(display, data):
	if(data.startMenu==False):
		rts_map_builder.drawMap(display,data)
		rts_helpers.drawBuildStencils(display,data)
		rts_helpers.drawSelectedRing(display,data)
		rts_buildings.drawBuildings(display,data)
		rts_helpers.drawRallyLine(display,data)
		rts_helpers.drawUnits(display,data)
		rts_helpers.drawSelectBox(display,data)
		#rts_helpers.drawCursor(display,data)
		rts_menus.drawMenu(display,data)
	else:
		rts_startmenu.drawMenu(display,data)

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
	initStartMenu(data)

	# initialize module and display
	pygame.init()
	pygame.font.init()
	display = pygame.display.set_mode((data.width,data.height))
	pygame.display.set_caption('RTS')

	data.font=pygame.font.SysFont('helvetica',14)
	data.menuFont=pygame.font.SysFont('helvetica',30)
	data.titleFont=pygame.font.SysFont('helvetica',40)

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