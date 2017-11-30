import pygame,sys
from pygame.locals import *
import rts_classes
import rts_images
import rts_units

def drawMenu(display,data):
	pygame.draw.rect(display,(20,20,20),(0,data.height*.75,data.width,data.height*.25))
	drawMiniMap(display,data)
	drawUnitBox(display,data)
	drawCmdBox(display,data)
	drawResourceBar(display,data)

def drawResourceBar(display,data):
	pygame.draw.rect(display,(20,20,20),(0,0,data.width,data.height*.04))
	nameLabel=data.font.render(data.localPlayer.username,1,(255,255,255))
	display.blit(nameLabel,(15,data.height*.01))
	woodLabel=data.font.render('Wood: '+str(data.localPlayer.wood),1,(255,255,255))
	display.blit(woodLabel,(data.width*.9,data.height*.01))
	metalLabel=data.font.render('Metals: '+str(data.localPlayer.metals),1,(255,255,255))
	display.blit(metalLabel,(data.width*.78,data.height*.01))
	energyLabel=data.font.render('Energy: '+str(int(data.localPlayer.energy))+'J / '+str(data.localPlayer.powerCap)+'J',1,(255,255,255))
	display.blit(energyLabel,(data.width*.6,data.height*.01))
	supplyLabel=data.font.render('Supply:'+str(data.localPlayer.supply)+' / '+str(data.localPlayer.supplyCap),1,(255,255,255))
	display.blit(supplyLabel,(data.width*.48,data.height*.01))

def drawMiniMap(display,data):
	boxX=data.width*.0125
	boxY=data.height*.75+data.height*.0125
	boXWidth=data.width*.225
	boxHeight=data.height*.225
	pygame.draw.rect(display,(35,35,35),(boxX,boxY,boXWidth,boxHeight))
	point1=(boxX,boxY+boxHeight/2)
	point3=(boxX+boXWidth,boxY+boxHeight/2)
	point2=(boxX+boXWidth/2,boxY+boxHeight*.25)
	point0=(boxX+boXWidth/2,boxY+boxHeight*.75)
	pygame.draw.polygon(display,(39,177,135),(point0,point1,point2,point3))
	cellWidth=boXWidth/100
	for x in range(data.cells):
		for y in range(data.cells):
			xCoord=x
			yCoord=y
			miniPoint0=((xCoord*.5*cellWidth - yCoord*.5*cellWidth)+point2[0],\
				(xCoord*.25*cellWidth+yCoord*.25*cellWidth)+point2[1])

			miniPoint1=(((xCoord-1)*.5*cellWidth - yCoord*.5*cellWidth)+point2[0],\
				((xCoord)*.25*cellWidth+(yCoord+1)*.25*cellWidth)+point2[1])

			miniPoint2=((xCoord*.5*cellWidth - yCoord*.5*cellWidth)+point2[0],\
				((xCoord+1)*.25*cellWidth+(yCoord+1)*.25*cellWidth)+point2[1])

			miniPoint3=(((xCoord+1)*.5*cellWidth - yCoord*.5*cellWidth)+point2[0],\
				((xCoord)*.25*cellWidth+(yCoord+1)*.25*cellWidth)+point2[1])
			tileLabel=data.board[x][y]
			if(tileLabel=='forest'):
				pygame.draw.polygon(display,(46,117,76),(miniPoint0,miniPoint1,miniPoint2,miniPoint3))
			elif(tileLabel=='mine'):
				pygame.draw.polygon(display,(7,74,139),(miniPoint0,miniPoint1,miniPoint2,miniPoint3))
			elif(tileLabel=='building'):
				if(data.localPlayer.team=='yellow'):
					pygame.draw.polygon(display,(255,255,0),(miniPoint0,miniPoint1,miniPoint2,miniPoint3))
				elif(data.localPlayer.team=='red'):
					pygame.draw.polygon(display,(255,0,0),(miniPoint0,miniPoint1,miniPoint2,miniPoint3))
				elif(data.localPlayer.team=='green'):
					pygame.draw.polygon(display,(0,255,0),(miniPoint0,miniPoint1,miniPoint2,miniPoint3))
				elif(data.localPlayer.team=='blue'):
					pygame.draw.polygon(display,(0,0,255),(miniPoint0,miniPoint1,miniPoint2,miniPoint3))
			if(x==data.cursorX and y==data.cursorY):
				cursorCenterX=(miniPoint1[0]+miniPoint3[0])/2
				cursorCenterY=(miniPoint0[1]+miniPoint2[1])/2
	pygame.draw.rect(display,(255,255,255),(cursorCenterX-8.1,cursorCenterY-6.075,16.2,12.15),1)

def drawUnitBox(display,data):
	data.unitIcons.empty()
	boxX=data.width*.25
	boxY=data.height*.75+data.height*.0125
	iconBuffer=data.width*.0125
	iconWidth=15
	iconHeight=24
	pygame.draw.rect(display,(35,35,35),(boxX,boxY,data.width*.4-data.width*.0125,data.height*.225))
	x=0
	y=0
	if(data.localPlayer.menuHover==None):
		if(len(data.localPlayer.selected)>1):
			#set max for 36 units
			for unit in data.localPlayer.selected:
				if(unit.name=='Drone'):
					data.unitIcons.add(rts_images.DroneIcon(boxX+iconBuffer+(iconWidth+iconBuffer)*x,boxY+iconBuffer+(iconHeight+iconBuffer)*y,iconWidth,iconHeight))
				elif(unit.name=='CommandCenter' or unit.name=='CommandCenterX'):
					data.unitIcons.add(rts_images.CommandCenterIcon(boxX+iconBuffer+(iconWidth+iconBuffer)*x,boxY+iconBuffer+(iconHeight+iconBuffer)*y,iconWidth,iconHeight))
				elif(unit.name=='GeothermalGenerator' or unit.name=='GeothermalGeneratorX'):
					data.unitIcons.add(rts_images.GeothermalGeneratorIcon(boxX+iconBuffer+(iconWidth+iconBuffer)*x,boxY+iconBuffer+(iconHeight+iconBuffer)*y,iconWidth,iconHeight))
				elif(unit.name=='Farm' or unit.name=='FarmX'):
					data.unitIcons.add(rts_images.FarmIcon(boxX+iconBuffer+(iconWidth+iconBuffer)*x,boxY+iconBuffer+(iconHeight+iconBuffer)*y,iconWidth,iconHeight))
				elif(unit.name=='WoodWall' or unit.name=='WoodWallX'):
					data.unitIcons.add(rts_images.WoodWallIcon(boxX+iconBuffer+(iconWidth+iconBuffer)*x,boxY+iconBuffer+(iconHeight+iconBuffer)*y,iconWidth,iconHeight))
				else:
					pygame.draw.rect(display,(0,0,0),(boxX+iconBuffer+(iconWidth+iconBuffer)*x,boxY+iconBuffer+(iconHeight+iconBuffer)*y,iconWidth,iconHeight))
				x+=1
				if(x>9):
					x=0
					y+=1
		elif(len(data.localPlayer.selected)==1):
			for unit in data.localPlayer.selected:
				if(unit.name=='Drone'):
					nameLabel=data.font.render(unit.name,1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.1,data.height*.77))
					woodLabel=data.font.render('Wood: '+str(unit.wood)+'/'+str(unit.woodCapacity),1,(153,230,255))
					display.blit(woodLabel,(boxX+iconBuffer,data.height*.8))
					metalLabel=data.font.render('Metals: '+str(unit.metals)+'/'+str(unit.metalCapacity),1,(153,230,255))
					display.blit(metalLabel,(boxX+iconBuffer,data.height*.83))
				if(unit.name=='Militia'):
					nameLabel=data.font.render(unit.name,1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.1,data.height*.77))
				elif(unit.name=='CommandCenterX'):
					nameLabel=data.font.render('Command Center',1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.15,data.height*.77))
					constructionLabel=data.font.render('Build Progress: '+str(int(unit.buildTimeLeft))+'/'+str(unit.buildTime),1,(153,230,255))
					display.blit(constructionLabel,(boxX+iconBuffer,data.height*.8))
				elif(unit.name=='CommandCenter'):
					nameLabel=data.font.render('Command Center',1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.15,data.height*.77))
					energyLabel=data.font.render('Energy Produced: '+str(int(unit.energyProduced))+'J',1,(153,230,255))
					display.blit(energyLabel,(boxX+iconBuffer,data.height*.8))
					queueIconBuffer=data.width*.01
					queueIconWidth=50
					queueIconHeight=50
					if(len(unit.buildQueue)>0 and unit.buildQueue[0]=='Drone'):
						data.unitIcons.add(rts_images.DroneIcon(boxX+queueIconBuffer,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					else:
						data.unitIcons.add(rts_images.QueueIcon1(boxX+queueIconBuffer,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					if(len(unit.buildQueue)>1 and unit.buildQueue[1]=='Drone'):
						data.unitIcons.add(rts_images.DroneIcon(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer),boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					else:
						data.unitIcons.add(rts_images.QueueIcon2(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer),boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					if(len(unit.buildQueue)>2 and unit.buildQueue[2]=='Drone'):
						data.unitIcons.add(rts_images.DroneIcon(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer)*2,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					else:
						data.unitIcons.add(rts_images.QueueIcon3(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer)*2,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					if(len(unit.buildQueue)>3 and unit.buildQueue[3]=='Drone'):
						data.unitIcons.add(rts_images.DroneIcon(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer)*3,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					else:
						data.unitIcons.add(rts_images.QueueIcon4(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer)*3,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					if(unit.createStartTime!=0):
						pygame.draw.rect(display,(91,91,91),(boxX+data.width*.015,data.height*.84,data.width*.4-data.width*.045,data.height*.01))
						loadbarWidth=(data.width*.4-data.width*.045)*(unit.createTimeLeft/rts_units.Drone.getBuildTime())
						if(loadbarWidth>data.width*.4-data.width*.045):
							loadbarWidth=data.width*.4-data.width*.045
						pygame.draw.rect(display,(153,230,255),(boxX+data.width*.015,data.height*.841,loadbarWidth,data.height*.005))
				elif(unit.name=='BarracksX'):
					nameLabel=data.font.render('Barracks',1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.15,data.height*.77))
					constructionLabel=data.font.render('Build Progress: '+str(int(unit.buildTimeLeft))+'/'+str(unit.buildTime),1,(153,230,255))
					display.blit(constructionLabel,(boxX+iconBuffer,data.height*.8))
				elif(unit.name=='Barracks'):
					nameLabel=data.font.render('Barracks',1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.15,data.height*.77))
					queueIconBuffer=data.width*.01
					queueIconWidth=50
					queueIconHeight=50
					if(len(unit.buildQueue)>0 and unit.buildQueue[0]=='Militia'):
						data.unitIcons.add(rts_images.DroneIcon(boxX+queueIconBuffer,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					else:
						data.unitIcons.add(rts_images.QueueIcon1(boxX+queueIconBuffer,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					if(len(unit.buildQueue)>1 and unit.buildQueue[1]=='Militia'):
						data.unitIcons.add(rts_images.DroneIcon(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer),boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					else:
						data.unitIcons.add(rts_images.QueueIcon2(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer),boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					if(len(unit.buildQueue)>2 and unit.buildQueue[2]=='Militia'):
						data.unitIcons.add(rts_images.DroneIcon(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer)*2,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					else:
						data.unitIcons.add(rts_images.QueueIcon3(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer)*2,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					if(len(unit.buildQueue)>3 and unit.buildQueue[3]=='Militia'):
						data.unitIcons.add(rts_images.DroneIcon(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer)*3,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					else:
						data.unitIcons.add(rts_images.QueueIcon4(boxX+queueIconBuffer+(queueIconWidth+queueIconBuffer)*3,boxY+queueIconBuffer+(queueIconHeight+queueIconBuffer),queueIconWidth,queueIconHeight))
					if(unit.createStartTime!=0):
						pygame.draw.rect(display,(91,91,91),(boxX+data.width*.015,data.height*.84,data.width*.4-data.width*.045,data.height*.01))
						loadbarWidth=(data.width*.4-data.width*.045)*(unit.createTimeLeft/rts_units.Militia.getBuildTime())
						if(loadbarWidth>data.width*.4-data.width*.045):
							loadbarWidth=data.width*.4-data.width*.045
						pygame.draw.rect(display,(153,230,255),(boxX+data.width*.015,data.height*.841,loadbarWidth,data.height*.005))
				elif(unit.name=='GeothermalGeneratorX'):
					nameLabel=data.font.render('GeothermalGenerator',1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.15,data.height*.77))
					constructionLabel=data.font.render('Build Progress: '+str(int(unit.buildTimeLeft))+'/'+str(unit.buildTime),1,(153,230,255))
					display.blit(constructionLabel,(boxX+iconBuffer,data.height*.8))
				elif(unit.name=='GeothermalGenerator'):
					nameLabel=data.font.render('GeothermalGenerator',1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.15,data.height*.77))
					energyLabel=data.font.render('Energy Produced: '+str(int(unit.energyProduced))+'J',1,(153,230,255))
					display.blit(energyLabel,(boxX+iconBuffer,data.height*.8))
				elif(unit.name=='FarmX'):
					nameLabel=data.font.render('Farm',1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.15,data.height*.77))
					constructionLabel=data.font.render('Build Progress: '+str(int(unit.buildTimeLeft))+'/'+str(unit.buildTime),1,(153,230,255))
					display.blit(constructionLabel,(boxX+iconBuffer,data.height*.8))
				elif(unit.name=='Farm'):
					nameLabel=data.font.render('Farm',1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.15,data.height*.77))
				elif(unit.name=='WoodWallX'):
					nameLabel=data.font.render('Wood Wall',1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.15,data.height*.77))
					constructionLabel=data.font.render('Build Progress: '+str(int(unit.buildTimeLeft))+'/'+str(unit.buildTime),1,(153,230,255))
					display.blit(constructionLabel,(boxX+iconBuffer,data.height*.8))
				elif(unit.name=='WoodWall'):
					nameLabel=data.font.render('Wood Wall',1,(153,230,255))
					display.blit(nameLabel,(data.width//2-data.width*.15,data.height*.77))
		data.unitIcons.draw(display)
	elif(data.localPlayer.menuHover=='Drone_b1'):
		nameLabel=data.font.render('Build Civilian Structures',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel=data.font.render('Menu for Building Non-Military Structures',1,(153,230,255))
		display.blit(descLabel,(boxX+iconBuffer,data.height*.8))
	elif(data.localPlayer.menuHover=='Drone_b2'):
		nameLabel=data.font.render('Build Military Structures',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel=data.font.render('Menu for Building Military Structures',1,(153,230,255))
		display.blit(descLabel,(boxX+iconBuffer,data.height*.8))
	elif(data.localPlayer.menuHover=='CommandCenter'):
		nameLabel=data.font.render('Build Command Center',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Primary Civilian Building Used for Building',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))
		descLabel2=data.font.render('Drones and Collecting Resources. Contains',1,(153,230,255))
		display.blit(descLabel2,(boxX+iconBuffer,data.height*.83))
		descLabel3=data.font.render('Small Generator and Mid Sized Battery',1,(153,230,255))
		display.blit(descLabel3,(boxX+iconBuffer,data.height*.86))
		descLabel5=data.font.render('Produces: .01J  Stores: 100J',1,(153,230,255))
		display.blit(descLabel5,(boxX+iconBuffer,data.height*.9))
		descLabel5=data.font.render('Wood Cost: 300  Metals Cost: 200',1,(153,230,255))
		display.blit(descLabel5,(boxX+iconBuffer,data.height*.94))
	elif(data.localPlayer.menuHover=='GeothermalGenerator'):
		nameLabel=data.font.render('Build Geothermal Generator',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Basic Energy Building',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))
		descLabel2=data.font.render('Provides: .05J  Stores: 5J',1,(153,230,255))
		display.blit(descLabel2,(boxX+iconBuffer,data.height*.84))
		descLabel3=data.font.render('Wood Cost: 0  Metals Cost: 100',1,(153,230,255))
		display.blit(descLabel3,(boxX+iconBuffer,data.height*.88))
		descLabel4=data.font.render('[Requires Command Center]',1,(153,230,255))
		display.blit(descLabel4,(boxX+iconBuffer,data.height*.92))
	elif(data.localPlayer.menuHover=='WoodWall'):
		nameLabel=data.font.render('Build Wood Wall',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Basic Wall',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))
		descLabel2=data.font.render('Wood Cost: 20 Metals Cost: 0',1,(153,230,255))
		display.blit(descLabel2,(boxX+iconBuffer,data.height*.84))
		descLabel3=data.font.render('[Requires Barracks]',1,(153,230,255))
		display.blit(descLabel3,(boxX+iconBuffer,data.height*.88))
	elif(data.localPlayer.menuHover=='Farm'):
		nameLabel=data.font.render('Build Farm',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Increases supply for biological units',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))
		descLabel2=data.font.render('Wood Cost: 150  Metals Cost: 0',1,(153,230,255))
		display.blit(descLabel2,(boxX+iconBuffer,data.height*.84))
		descLabel3=data.font.render('[Requires Command Center]',1,(153,230,255))
		display.blit(descLabel3,(boxX+iconBuffer,data.height*.88))
	elif(data.localPlayer.menuHover=='Barracks'):
		nameLabel=data.font.render('Build Barracks',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Builds Basic Infantry Units',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))
		descLabel2=data.font.render('Wood Cost: 200  Metals Cost: 100',1,(153,230,255))
		display.blit(descLabel2,(boxX+iconBuffer,data.height*.84))
		descLabel3=data.font.render('[Requires Farm]',1,(153,230,255))
		display.blit(descLabel3,(boxX+iconBuffer,data.height*.88))
	elif(data.localPlayer.menuHover=='Build_Drone'):
		nameLabel=data.font.render('Build Drone',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Worker Unit',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))
		descLabel2=data.font.render('Wood Cost: 0  Metals Cost: 30  Energy Cost: 50',1,(153,230,255))
		display.blit(descLabel2,(boxX+iconBuffer,data.height*.84))
	elif(data.localPlayer.menuHover=='Train_Militia'):
		nameLabel=data.font.render('Train Militia',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Standard Infantry Unit',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))
		descLabel2=data.font.render('Wood Cost: 0  Metals Cost: 50  Energy Cost: 10',1,(153,230,255))
		display.blit(descLabel2,(boxX+iconBuffer,data.height*.84))
	elif(data.localPlayer.menuHover=='Drone_Action'):
		nameLabel=data.font.render('Harvest',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Commands Drone to Harvest Wood or Metals',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))
		descLabel2=data.font.render('it is Interacting with',1,(153,230,255))
		display.blit(descLabel2,(boxX+iconBuffer,data.height*.83))
	elif(data.localPlayer.menuHover=='Rally_Point'):
		nameLabel=data.font.render('Set Rally Point',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Click Button and then Click Elsewhere to',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))
		descLabel2=data.font.render("Reset Building's Rally Point",1,(153,230,255))
		display.blit(descLabel2,(boxX+iconBuffer,data.height*.83))
	elif(data.localPlayer.menuHover=='Destroy'):
		nameLabel=data.font.render('Destroy',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Destroys Selected Units and Structures',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))
	elif(data.localPlayer.menuHover=='Escape'):
		nameLabel=data.font.render('Escape',1,(153,230,255))
		display.blit(nameLabel,(data.width//2-data.width*.2,data.height*.77))
		descLabel1=data.font.render('Returns to Previous Menu',1,(153,230,255))
		display.blit(descLabel1,(boxX+iconBuffer,data.height*.8))


def drawCmdBox(display,data):
	data.menuButtons.empty()
	boxX=data.width*.65
	boxY=data.height*.75+data.height*.013
	iconBuffer=data.width*.025
	iconWidth=45
	pygame.draw.rect(display,(35,35,35),(boxX,boxY,data.width*.35-data.width*.0125,data.height*.225))
	if(data.localPlayer.menuState=='Drone'):
		data.menuButtons.add(data.menuButton1)
		data.menuButtons.add(data.menuButton2)
		data.menuButtons.add(data.menuButton4)
		data.menuButtons.add(data.menuButton6)
	elif(data.localPlayer.menuState=='Drone_b1'):
		data.menuButtons.add(data.menuButton1)
		data.menuButtons.add(data.menuButton2)
		data.menuButtons.add(data.menuButton3)
		data.menuButtons.add(data.menuButton6)
	elif(data.localPlayer.menuState=='Drone_b2'):
		data.menuButtons.add(data.menuButton1)
		data.menuButtons.add(data.menuButton2)
		data.menuButtons.add(data.menuButton6)
	elif(data.localPlayer.menuState=='CommandCenter'):
		data.menuButtons.add(data.menuButton1)
		data.menuButtons.add(data.menuButton4)
		data.menuButtons.add(data.menuButton6)
	elif(data.localPlayer.menuState=='Barracks'):
		data.menuButtons.add(data.menuButton1)
		data.menuButtons.add(data.menuButton4)
		data.menuButtons.add(data.menuButton6)
	data.menuButtons.draw(display)

def menuButtonsPressed(pos,data):
	if(pos[0]>data.width*.68125 and pos[0]<data.width*.68125+45):
		if(pos[1]>data.height*.763 and pos[1]<data.height*.763+45):
			return data.menuButton1.pressed(data)
	if(pos[0]>data.width*.68125+(data.width*.025+45) and pos[0]<data.width*.68125+45+(data.width*.025+45)):
		if(pos[1]>data.height*.763 and pos[1]<data.height*.763+45):
			return data.menuButton2.pressed(data)
	if(pos[0]>data.width*.68125+(data.width*.025+45)*2 and pos[0]<data.width*.68125+45+(data.width*.025+45)*2):
		if(pos[1]>data.height*.763 and pos[1]<data.height*.763+45):
			return data.menuButton3.pressed(data)
	if(pos[0]>data.width*.68125 and pos[0]<data.width*.68125+45):
		if(pos[1]>data.height*.763+(data.width*.025+45) and pos[1]<data.height*.763+(data.width*.025+45)+45):
			return data.menuButton4.pressed(data)
	if(pos[0]>data.width*.68125+(data.width*.025+45) and pos[0]<data.width*.68125+45+(data.width*.025+45)):
		if(pos[1]>data.height*.763+(data.width*.025+45) and pos[1]<data.height*.763+(data.width*.025+45)+45):
			return 5
	if(pos[0]>data.width*.68125+(data.width*.025+45)*2 and pos[0]<data.width*.68125+45+(data.width*.025+45)*2):
		if(pos[1]>data.height*.763+(data.width*.025+45) and pos[1]<data.height*.763+(data.width*.025+45)+45):
			return data.menuButton6.pressed(data)

def menuButtonsHover(pos,data):
	if(pos[0]>data.width*.68125 and pos[0]<data.width*.68125+45):
		if(pos[1]>data.height*.763 and pos[1]<data.height*.763+45):
			return data.menuButton1.hover(data)
	if(pos[0]>data.width*.68125+(data.width*.025+45) and pos[0]<data.width*.68125+45+(data.width*.025+45)):
		if(pos[1]>data.height*.763 and pos[1]<data.height*.763+45):
			return data.menuButton2.hover(data)
	if(pos[0]>data.width*.68125+(data.width*.025+45)*2 and pos[0]<data.width*.68125+45+(data.width*.025+45)*2):
		if(pos[1]>data.height*.763 and pos[1]<data.height*.763+45):
			return data.menuButton3.hover(data)
	if(pos[0]>data.width*.68125 and pos[0]<data.width*.68125+45):
		if(pos[1]>data.height*.763+(data.width*.025+45) and pos[1]<data.height*.763+(data.width*.025+45)+45):
			return data.menuButton4.hover(data)
	if(pos[0]>data.width*.68125+(data.width*.025+45) and pos[0]<data.width*.68125+45+(data.width*.025+45)):
		if(pos[1]>data.height*.763+(data.width*.025+45) and pos[1]<data.height*.763+(data.width*.025+45)+45):
			return 5
	if(pos[0]>data.width*.68125+(data.width*.025+45)*2 and pos[0]<data.width*.68125+45+(data.width*.025+45)*2):
		if(pos[1]>data.height*.763+(data.width*.025+45) and pos[1]<data.height*.763+(data.width*.025+45)+45):
			return data.menuButton6.hover(data)
	else:
		data.localPlayer.menuHover=None
