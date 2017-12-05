import pygame,sys
from pygame.locals import *
import rts_helpers
import rts_map_builder
import rts_classes
import rts_images
import rts_menus
import rts_buildings
import rts_startmenu
import rts_server_commands
from rts_dev_debug import efficiencyCheck
from rts_data import data
import random
import math
import subprocess
import os
import socket
import threading
import ast
import time
from queue import Queue

@efficiencyCheck
def initMultiplayer(data):
	data.clientele = dict()
	data.otherUsers=dict()
	data.localPlayer=rts_classes.Player(data.usernameInput)
	if(data.multiplayerButtonsPressed==1):
		#subprocess.Popen(['cmd','-r',os.path.join('rts_server.py')])
		try:
			rts_server_commands.joinServer(data,data.IPInput)
			data.invalidIP=False
		except:
			data.invalidIP=True
			data.multiplayerButtonsPressed=None
			data.startMenuState='Multiplayer'
		if(data.invalidIP==False):
			data.localPlayer.role='Host'
			threading.Thread(target = rts_server_commands.handleServerMsg, args = (data.server, data.serverMsg)).start()
			msg='newUsername %s \n'%data.usernameInput
			data.server.send(msg.encode())
	elif(data.multiplayerButtonsPressed==2):
		try:
			rts_server_commands.joinServer(data,data.IPInput)
			data.invalidIP=False
		except:
			data.invalidIP=True
			data.multiplayerButtonsPressed=None
			data.startMenuState='Multiplayer'
		if(data.invalidIP==False):
			data.localPlayer.role='Client'
			threading.Thread(target = rts_server_commands.handleServerMsg, args = (data.server, data.serverMsg)).start()
			msg='newUsername %s \n'%data.usernameInput
			data.server.send(msg.encode())

@efficiencyCheck
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
	data.numOfForests=15
	data.forestSize=50
	data.numOfMines=10
	data.trees=pygame.sprite.Group()
	data.mines=pygame.sprite.Group()
	rts_helpers.initializeMenu(data)
	data.selectBox1=(None,None)
	data.selectBox2=[0,0]
	data.mapCoords=((0,0),(0,data.cells-1),(data.cells-1,data.cells-1),(data.cells-1,0))
	data.mapPos=rts_map_builder.generateMapPos(data)
	data.buildStencil=None
	data.board=[]
	data.boardComplete=False
	data.visibleUnits=pygame.sprite.Group()
	data.visibleBuildings=pygame.sprite.Group()
	data.visibleNature=pygame.sprite.Group()
	data.fogOfWar=pygame.Surface([data.width,data.height])
	data.fogOfWar.set_alpha(20)
	data.fogOfWar.fill((0,0,0))
	data.loadingScreenTip=random.choice(['CommandCenter','Marine','Drone','Farm','Generator','Wall','Barracks'])
	data.loadingScreenImage=pygame.sprite.GroupSingle()
	if(data.loadingScreenTip=='CommandCenter'):
		data.loadingScreenImage.add(rts_images.CommandCenterIcon(data.width*.123,0,int(data.width*.75),int(data.width*.75)))
	elif(data.loadingScreenTip=='Marine'):
		data.loadingScreenImage.add(rts_images.MarineIcon(data.width*.123,0,int(data.width*.75),int(data.width*.75)))
	elif(data.loadingScreenTip=='Drone'):
		data.loadingScreenImage.add(rts_images.DroneIcon(data.width*.123,0,int(data.width*.75),int(data.width*.75)))
	elif(data.loadingScreenTip=='Farm'):
		data.loadingScreenImage.add(rts_images.FarmIcon(data.width*.123,0,int(data.width*.75),int(data.width*.75)))
	elif(data.loadingScreenTip=='Generator'):
		data.loadingScreenImage.add(rts_images.GeothermalGeneratorIcon(data.width*.123,0,int(data.width*.75),int(data.width*.75)))
	elif(data.loadingScreenTip=='Wall'):
		data.loadingScreenImage.add(rts_images.WoodWallIcon(data.width*.123,0,int(data.width*.75),int(data.width*.75)))
	elif(data.loadingScreenTip=='BarracksCenter'):
		data.loadingScreenImage.add(rts_images.BarracksCenterIcon(data.width*.123,0,int(data.width*.75),int(data.width*.75)))


@efficiencyCheck
def startSingleplayerGame(display,data):
	data.startMenu=False
	data.localPlayer=rts_classes.Player(data.usernameInput)
	data.otherUsers=dict()
	data.otherUsers['AI']=rts_classes.Player('AI')
	data.otherUsers['AI'].team='red'
	numOfCommandCenters=random.randint(3,5)
	init(data)
	rts_map_builder.buildMap(display,data)
	for i in range(numOfCommandCenters):
		x=random.randint(5,data.cells-6)
		y=random.randint(5,data.cells-6)
		commandCenter=rts_buildings.CommandCenter(data,x,y,data.otherUsers['AI'].team)
		buildingID=random.randint(1000000,9999999)
		data.otherUsers['AI'].IDs.add(buildingID)
		commandCenter.ID=buildingID
		rts_helpers.placeBuildingAtCoord(data,commandCenter,x,y)
		data.otherUsers['AI'].inConstruction.add(commandCenter)
	x,y=rts_helpers.getTileCenterCoordinate(data,data.cursorX,data.cursorY)
	data.localPlayer.createDrone(data,x,y,x,y)
	data.failStartTime=time.time()
	data.failTime=20*60

@efficiencyCheck
def mouseDown(event,data):
	if(data.startMenu==False):
		if(data.localPlayer.winCondition=='play'):
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
			    	target=None
			    	# for building in data.localPlayer.buildings:
			    	# 	if(building.rect.collidepoint(event.pos)):
	    			# 		target=building
	    			# 		break
			    	# for unit in data.localPlayer.units:
	    			# 	if(unit.rect.collidepoint(event.pos)):
	    			# 		target=unit
	    			# 		break
		    		for ID in data.otherUsers:
		    			player=data.otherUsers[ID]
		    			for building in player.buildings:
		    				if(building.rect.collidepoint(event.pos)):
		    					target=building
		    					break
		    			for unit in player.units:
		    				if(unit.rect.collidepoint(event.pos)):
		    					target=unit
		    					break
			    	for unit in data.localPlayer.selected:
			    		msg=''#transmit change in position and unit ID
				    	unit.desX=mouseX
				    	unit.desY=mouseY
				    	msg+='moveUnit %d %d %d \n'%(unit.rect.center[0]-mouseX,unit.rect.center[1]-mouseY,unit.ID)
				    	unit.rally_pointX=mouseX
				    	unit.rally_pointY=mouseY
				    	unit.target=target
				    	if(target==None):
				    		msg+='newTarget %d None \n'%(unit.ID)
				    	else:
				    		msg+='newTarget %d %d \n'%(unit.ID,target.ID)
				    	if(data.startMenuState!='Singleplayer'):
				    		data.server.send(msg.encode())

			else:
				rts_menus.menuButtonsPressed(event.pos,data)
		else:
			rts_helpers.endButtonPressed(data,event.pos)
	else:
		if(data.startMenuState=='Start'):
			data.startMenuState=rts_startmenu.startMenuButtonPressed(data,event.pos)
		elif(data.startMenuState=='Instructions'):
			if(data.backButton.sprite.rect.collidepoint(event.pos)):
				data.startMenuState='Start'
				data.backButtonHover=False
			rts_startmenu.instructionPageFlip(data,event.pos)
		elif(data.startMenuState=='Singleplayer'):
			data.singlePlayerTextBoxSelect=rts_startmenu.singlePlayerTextBoxSelect(data,event.pos)
			if(len(data.usernameInput)>0):
				data.playButtonPressed=rts_startmenu.playButtonPressed(data,event.pos)
			if(data.backButton.sprite.rect.collidepoint(event.pos)):
				data.startMenuState='Start'
				data.backButtonHover=False
		elif(data.startMenuState=='Multiplayer'):
			data.multiplayerTextBoxSelect=rts_startmenu.multiplayerTextBoxSelect(data,event.pos)
			if(len(data.IPInput)>0 and len(data.usernameInput)>0):
				data.multiplayerButtonsPressed=rts_startmenu.multiplayerButtonsPressed(data,event.pos)
				initMultiplayer(data)
			if(data.backButton.sprite.rect.collidepoint(event.pos)):
				data.startMenuState='Start'
				data.backButtonHover=False
		elif(data.startMenuState=='Lobby'):
			data.localPlayer.team=rts_startmenu.lobbyTeamButtonsPressed(data,event.pos)
			msg=''
			msg+='newTeam %s \n'%data.localPlayer.team
			data.server.send(msg.encode())
			if(data.localPlayer.role=='Host'):
				data.playButtonPressed=rts_startmenu.playButtonPressed(data,event.pos)
				if(data.playButtonPressed==1):
					msg+='startGame %s \n'%'test'
					data.server.send(msg.encode())

@efficiencyCheck
def mouseUp(event,data):
	if(data.startMenu==False):
	    if(data.selectBox1!=(None,None)):
	   		data.selectBox1=(None,None)
	   		data.selectBox2=[0,0]

@efficiencyCheck
def mouseMotion(event,data):
	if(data.startMenu==False):
		if(data.localPlayer.winCondition=='play'):
			if(data.selectBox1!=(None,None)):
				dX,dY=event.rel[0],event.rel[1]
				data.selectBox2[0]+=dX
				data.selectBox2[1]+=dY
			data.mousePos=event.pos
			rts_menus.menuButtonsHover(event.pos,data)
	else:
		if(data.startMenuState=='Start'):
			data.startMenuSelect=rts_startmenu.startMenuButtonHover(data,event.pos)
		elif(data.startMenuState=='Lobby' and data.localPlayer.role=='Host'):
			data.playButtonHover=rts_startmenu.playButtonHover(data,event.pos)
		elif(data.startMenuState=='Singleplayer'):
			data.playButtonHover=rts_startmenu.playButtonHover(data,event.pos)
			if(data.backButton.sprite.rect.collidepoint(event.pos)):
				data.backButtonHover=True
			else:
				data.backButtonHover=False
		elif(data.startMenuState=='Multiplayer'):
			data.multiplayerButtonHover=rts_startmenu.multiplayerButtonsHover(data,event.pos)
			if(data.backButton.sprite.rect.collidepoint(event.pos)):
				data.backButtonHover=True
			else:
				data.backButtonHover=False

@efficiencyCheck
def keyDown(event,data):
	if(data.startMenu==False):
		if(data.localPlayer.winCondition=='play'):
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

		###############Dev Commands##################

		if(event.unicode=='p'):
			x,y=rts_helpers.getTileCenterCoordinate(data,data.cursorX,data.cursorY)
			data.localPlayer.createMilitia(data,x,y,x,y)
		elif(event.unicode=='`'):
			rts_helpers.printEfficiencyResults(data)
		elif(event.unicode=='w'):
			data.localPlayer.winCondition='win'
	else:
		if(data.startMenuState=='Singleplayer' or data.startMenuState=='Multiplayer'):
			if(event.key==9):
				if(data.multiplayerTextBoxSelect==None):
					data.multiplayerTextBoxSelect=1
				else:
					data.multiplayerTextBoxSelect+=1
					if(data.multiplayerTextBoxSelect>2):
						data.multiplayerTextBoxSelect=1
			if(data.singlePlayerTextBoxSelect==1 or data.multiplayerTextBoxSelect==1):
				if(event.unicode.isalnum()):
					data.usernameInput+=event.unicode
				elif(event.key==8 and len(data.usernameInput)>0):
					data.usernameInput=data.usernameInput[:-1]
			if(data.multiplayerTextBoxSelect==2):
				if(event.unicode.isdigit() or event.unicode=='.'):
					data.IPInput+=event.unicode
				elif(event.key==8 and len(data.IPInput)>0):
					data.IPInput=data.IPInput[:-1]

@efficiencyCheck
def keyUp(event,data):
   	pass

@efficiencyCheck
def timerFired(display,data):
	rts_server_commands.interpServerCommands(data)
	if(data.startMenu==False):
		rts_helpers.buildBuildings(data)
		rts_helpers.createUnits(data)
		rts_helpers.collectUnitMats(data)
		rts_helpers.collectEnergy(data)
		rts_helpers.setPowerCap(data)
		rts_helpers.setSupplyCap(data)
		rts_helpers.calcSupply(data)
		data.localPlayer.units.update(data)
		for ID in data.otherUsers:
			player=data.otherUsers[ID]
			player.units.update(data)
		rts_helpers.inSelectionBox(data)
		rts_helpers.checkWinConditions(data)
	else:
		if(data.playButtonPressed):
			if(data.startMenuState=='Singleplayer'):
				startSingleplayerGame(display,data)
			else:
				if(data.localPlayer.role=='Host'):
					init(data)
					rts_map_builder.buildMap(display,data)
					boardmsg=str(data.board)
					boardmsg=boardmsg.replace(' ','')
					msg='board %s \n'%boardmsg
					data.server.send(msg.encode())
					data.startMenu=False
					x,y=rts_helpers.getTileCenterCoordinate(data,data.cursorX,data.cursorY)
					data.localPlayer.createDrone(data,x,y,x,y)
				else:
					if(data.startMenuState=='Lobby'):
						init(data)
						data.startMenuState='syncMap'
						for i in range(data.cells):
							newRow=[]
							for j in range(data.cells):
								newRow.append('field')
							data.board.append(newRow)
					if(data.boardComplete):
						data.board=rts_helpers.eval2DListOfStrings(data.board)
						rts_map_builder.drawLoadBar(display,data,'Compiling Tree Sprites...',0)
						rts_map_builder.compileTreeSprites(display,data)
						rts_map_builder.compileMineSprites(display,data)
						data.startMenu=False
						x,y=rts_helpers.getTileCenterCoordinate(data,data.cursorX,data.cursorY)
						data.localPlayer.createDrone(data,x,y,x,y)



@efficiencyCheck
def redrawAll(display, data):
	if(data.startMenu==False):
		rts_map_builder.drawMap(display,data)
		rts_helpers.drawBuildStencils(display,data)
		rts_helpers.drawSelectedRing(display,data)
		rts_buildings.drawBuildings(display,data)
		rts_helpers.drawRallyLine(display,data)
		rts_helpers.drawUnits(display,data)
		rts_helpers.drawHealthBars(display,data)
		rts_helpers.drawSelectBox(display,data)
		#rts_helpers.drawCursor(display,data)
		if(data.localPlayer.winCondition=='play'):
			data.fogOfWar.fill((0,0,0))
			rts_helpers.drawVisibility(data,data.fogOfWar)
			display.blit(data.fogOfWar,(0,0))
			rts_menus.drawMenu(display,data)
		else:
			rts_helpers.drawEndScreen(display,data)
	else:
		rts_startmenu.drawMenu(display,data)

def run(width=300, height=300,serverMsg=None,server=None):
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
		timerFired(display,data)
		redrawAllWrapper(display, data)
		data.fpsClock.tick(data.fps)

	# Set up data and call init
	data.runStartTime=time.time()
	data.multiplayerButtonsPressed=None
	data.serverMsg=serverMsg
	data.server=server
	data.width = width
	data.height = height
	data.fps=30 #frames per second
	data.fpsClock=pygame.time.Clock()
	data.functions=dict()
	rts_helpers.initStartMenu(data)

	# initialize module and display
	pygame.init()
	pygame.font.init()
	display = pygame.display.set_mode((data.width,data.height))
	pygame.display.set_caption('Second Earth')

	data.font=pygame.font.SysFont('helvetica',14)
	data.menuFont=pygame.font.SysFont('helvetica',30)
	data.titleFont=pygame.font.SysFont('helvetica',40)

	#initialize Images
	rts_images.loadImages(data)

	
	#main loop
	while(True):
		#if(data.multiplayerButtonsPressed!=None and data.startMenuState=='Multiplayer'):

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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverMsg = Queue(100)
run(600,600,serverMsg,server)