import pygame,sys
from pygame.locals import *
import rts_classes

def drawMenu(display,data):
	pygame.draw.rect(display,(255,166,77),(0,data.height*.75,data.width,data.height*.25))
	drawMiniMap(display,data)
	drawUnitBox(display,data)
	drawCmdBox(display,data)

def drawMiniMap(display,data):
	pygame.draw.rect(display,(26,26,26),(data.width*.0125,data.height*.75+data.height*.0125,data.width*.225,data.height*.225))

def drawUnitBox(display,data):
	boxX=data.width*.25
	boxY=data.height*.75+data.height*.0125
	iconBuffer=data.width*.0125
	iconWidth=15
	iconHeight=24
	pygame.draw.rect(display,(255,153,51),(boxX,boxY,data.width*.4-data.width*.0125,data.height*.225))
	x=0
	y=0
	#set max for 36 units
	for unit in rts_classes.player1.selected:
		pygame.draw.rect(display,(0,0,0),(boxX+iconBuffer+(iconWidth+iconBuffer)*x,boxY+iconBuffer+(iconHeight+iconBuffer)*y,iconWidth,iconHeight))
		x+=1
		if(x>9):
			x=0
			y+=1

def drawCmdBox(display,data):
	data.menuButtons.empty()
	boxX=data.width*.65
	boxY=data.height*.75+data.height*.013
	iconBuffer=data.width*.025
	iconWidth=45
	pygame.draw.rect(display,(255,179,102),(boxX,boxY,data.width*.35-data.width*.0125,data.height*.225))
	if(rts_classes.player1.menuState=='Drone'):
		data.menuButtons.add(data.menuButton1)
		data.menuButtons.add(data.menuButton4)
		data.menuButtons.add(data.menuButton6)
		# pygame.draw.rect(display,(0,0,0),(boxX+iconBuffer*1.25,boxY+iconBuffer,iconWidth,iconWidth))
		# pygame.draw.rect(display,(0,0,0),(boxX+iconBuffer*1.25+(iconWidth+iconBuffer),boxY+iconBuffer,iconWidth,iconWidth))
		# pygame.draw.rect(display,(0,0,0),(boxX+iconBuffer*1.25+(iconWidth+iconBuffer)*2,boxY+iconBuffer,iconWidth,iconWidth))
		# pygame.draw.rect(display,(0,0,0),(boxX+iconBuffer*1.25+(iconWidth+iconBuffer),boxY+iconBuffer+(iconWidth+iconBuffer),iconWidth,iconWidth))
	data.menuButtons.draw(display)

def menuButtonsPressed(pos,data):
	if(pos[0]>data.width*.68125 and pos[0]<data.width*.68125+45):
		if(pos[1]>data.height*.763 and pos[1]<data.height*.763+45):
			return data.menuButton1.pressed()
	if(pos[0]>data.width*.68125+(data.width*.025+45) and pos[0]<data.width*.68125+45+(data.width*.025+45)):
		if(pos[1]>data.height*.763 and pos[1]<data.height*.763+45):
			return 2
	if(pos[0]>data.width*.68125+(data.width*.025+45)*2 and pos[0]<data.width*.68125+45+(data.width*.025+45)*2):
		if(pos[1]>data.height*.763 and pos[1]<data.height*.763+45):
			return 3
	if(pos[0]>data.width*.68125 and pos[0]<data.width*.68125+45):
		if(pos[1]>data.height*.763+(data.width*.025+45) and pos[1]<data.height*.763+(data.width*.025+45)+45):
			return data.menuButton4.pressed(data)
	if(pos[0]>data.width*.68125+(data.width*.025+45) and pos[0]<data.width*.68125+45+(data.width*.025+45)):
		if(pos[1]>data.height*.763+(data.width*.025+45) and pos[1]<data.height*.763+(data.width*.025+45)+45):
			return 5
	if(pos[0]>data.width*.68125+(data.width*.025+45)*2 and pos[0]<data.width*.68125+45+(data.width*.025+45)*2):
		if(pos[1]>data.height*.763+(data.width*.025+45) and pos[1]<data.height*.763+(data.width*.025+45)+45):
			return data.menuButton6.pressed()
