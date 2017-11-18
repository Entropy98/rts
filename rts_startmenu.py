import pygame

def drawMenu(display,data):
	pygame.draw.rect(display,(255,153,51),(0,0,data.width,data.height))
	nameLabel=data.titleFont.render('',1,(20,20,20))
	#pygame.draw.line(display,(0,0,0),(data.width/2,0),(data.width/2,data.height))
	if(data.startMenuState=='Start'):
		nameLabel=data.titleFont.render('[Name TBD]',1,(20,20,20))
		if(data.startMenuSelect==1):
			pygame.draw.rect(display,(255,199,148),(data.width/2-100,data.height*.35,200,40))	
		pygame.draw.rect(display,(20,20,20),(data.width/2-100,data.height*.35,200,40),3)
		singplayerLabel=data.menuFont.render('Singleplayer',1,(20,20,20))
		display.blit(singplayerLabel,(data.width/2-70,data.height*.35))
		if(data.startMenuSelect==2):
			pygame.draw.rect(display,(255,199,148),(data.width/2-100,data.height*.43,200,40))	
		pygame.draw.rect(display,(20,20,20),(data.width/2-100,data.height*.43,200,40),3)
		multiplayerLabel=data.menuFont.render('Multiplayer',1,(20,20,20))
		display.blit(multiplayerLabel,(data.width/2-60,data.height*.43))
	elif(data.startMenuState=='Singleplayer'):
		nameLabel=data.titleFont.render('Singleplayer',1,(20,20,20))
		usernameLabel=data.menuFont.render('Username: ',1,(20,20,20))
		display.blit(usernameLabel,(data.width*.2,data.height*.35))
		pygame.draw.rect(display,(242,242,242),(data.width*.41,data.height*.35,200,40))
		pygame.draw.rect(display,(20,20,20),(data.width*.41,data.height*.35,200,40),1)
		if(data.singlePlayerTextBoxSelect==1):
			textBox1Text=data.menuFont.render(data.usernameInput+'_',1,(20,20,20))
		else:
			textBox1Text=data.menuFont.render(data.usernameInput,1,(20,20,20))
		display.blit(textBox1Text,(data.width*.41+5,data.height*.35))
		playLabel=data.menuFont.render('Start Game',1,(20,20,20))
		if(data.playButtonHover):
			pygame.draw.rect(display,(255,199,148),(data.width/2-80,data.height*.8,160,40))
		pygame.draw.rect(display,(20,20,20),(data.width/2-80,data.height*.8,160,40),3)
		display.blit(playLabel,(data.width/2-63,data.height*.8))
	display.blit(nameLabel,(data.width/2-100,data.height*.15))

def startMenuButtonHover(data,pos):
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.35 and pos[1]<data.height*.35+40):
			return 1
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.43 and pos[1]<data.height*.43+40):
			return 2

def startMenuButtonPressed(data,pos):
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.35 and pos[1]<data.height*.35+40):
			return 'Singleplayer'
	if(pos[0]>data.width/2-100 and pos[0]<data.width/2+100):
		if(pos[1]>data.height*.43 and pos[1]<data.height*.43+40):
			return 'Multiplayer'
	return data.startMenuState

def singlePlayerTextBoxSelect(data,pos):
	if(pos[0]>data.width*.41 and pos[0]<data.width*.41+200):
		if(pos[1]>data.height*.35 and pos[1]<data.height*.35+40):
			return 1

def playButtonHover(data,pos):
	if(pos[0]>data.width/2-80 and pos[0]<data.width/2+80):
		if(pos[1]>data.height*.8 and pos[1]<data.height*.8+40):
			return True
	return False

def playButtonPressed(data,pos):
	if(pos[0]>data.width/2-80 and pos[0]<data.width/2+80):
		if(pos[1]>data.height*.8 and pos[1]<data.height*.8+40):
			return True
	return False